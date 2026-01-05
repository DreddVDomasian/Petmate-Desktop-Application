import os
import sys
from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSettings, QTimer, QThread, pyqtSignal
import resources_rc
from PyQt6.QtGui import QPixmap, QIcon
from toast import Toast
from shadowEffects import create_card_shadow
from Desktop_Application.Backend.api_client import desktop_login, send_otp, verify_otp_and_reset_password
from api_worker import APIWorker
import requests
from config_loader import API_BASE_URL


# Worker thread for OTP sending to prevent UI freezing
class OTPSendWorker(QThread):
    finished = pyqtSignal(bool, object)  # success, response

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        try:
            success, response = send_otp(self.email)
            self.finished.emit(success, response)
        except Exception as e:
            self.finished.emit(False, {'error': str(e)})


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui-files/LoginCard.ui", self)

        # Setup UI
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply shadows
        self.apply_shadows()

        # Initialize page
        self.LoginStackedWidget.setCurrentIndex(0)

        # Connect signals
        self.loginBtn.clicked.connect(self.attempt_login)
        self.closeLoginBtn.clicked.connect(self.close_app)
        self.closeBtn.clicked.connect(self.close_app)
        self.forgotpassBtn.clicked.connect(lambda: self.navigate_login(1))
        self.backToLogin.clicked.connect(lambda: self.navigate_login(0))

        # OTP functionality
        self.otpFrame.setVisible(False)
        self.sendOtpBtn.clicked.connect(self.send_otp_request)
        self.proceedBtn.clicked.connect(self.verify_otp)
        self.submitNewPass.clicked.connect(self.reset_password)

        # OTP timer - removed timer functionality
        self.otp_timer = QTimer()
        self.otp_timer.timeout.connect(self.update_otp_timer)
        self.otp_time_remaining = 0

        # Remove the timer label if it exists in UI
        if hasattr(self, 'otpTimerLabel'):
            self.otpTimerLabel.setVisible(False)

        # Load saved credentials if "Stay Signed In" was checked
        self.load_saved_credentials()

        # Store email for OTP flow
        self.otp_email = ""
        self.otp_code = ""  # Store OTP for verification

        # Worker thread
        self.otp_worker = None

        self.password_toggle()
    def password_toggle(self):
        self.setup_password_toggle(self.loginPassword,self.loginShowPass)
        self.setup_password_toggle(self.newPass,self.loginShowPass_2)
        self.setup_password_toggle(self.confirmPass,self.loginShowPass_3)

    def setup_password_toggle(self, line_edit, tool_button, icon_show="Icons/eye.png", icon_hide="Icons/hide.png"):

        # Store toggle state inside the button so it's reusable
        tool_button.password_visible = False

        def toggle():
            if tool_button.password_visible:
                line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                tool_button.setIcon(QIcon(icon_show))
            else:
                line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                tool_button.setIcon(QIcon(icon_hide))

            tool_button.password_visible = not tool_button.password_visible

        tool_button.clicked.connect(toggle)

    def navigate_login(self, index):
        self.LoginStackedWidget.setCurrentIndex(index)
        if index == 1:  # Forgot password page
            self.clear_otp_fields()

    def clear_otp_fields(self):
        """Clear OTP fields when navigating"""
        self.emailOtpEdit.clear()
        self.otpEdit.clear()
        self.newPass.clear()
        self.confirmPass.clear()
        self.otpFrame.setVisible(False)
        self.emailOtp.setVisible(True)
        self.otp_timer.stop()
        self.sendOtpBtn.setEnabled(True)
        self.sendOtpBtn.setText("Send OTP")
        self.otp_email = ""
        self.otp_code = ""



    def send_otp_request(self):
        """Send OTP to user's email"""
        email = self.emailOtpEdit.text().strip()

        if not email:
            toast = Toast(parent=self, message="Please enter your email address", icon_path="Icons/warning.png",duration=2000)
            toast.show_toast()
            return

        # Show loading state - force UI update
        self.sendOtpBtn.setText("Sending...")
        self.sendOtpBtn.setEnabled(False)
        self.sendOtpBtn.repaint()  # Force immediate UI update
        QApplication.processEvents()  # Process pending events to update UI

        # Store email for later use
        self.otp_email = email

        # Start worker thread to prevent UI freezing
        self.otp_worker = OTPSendWorker(email)
        self.otp_worker.finished.connect(self.on_otp_sent)
        self.otp_worker.start()

    def on_otp_sent(self, success, response):
        """Handle OTP sending completion"""
        if success:
            self.otpFrame.setVisible(True)
            self.emailOtp.setVisible(False)

            # Removed timer functionality
            if hasattr(self, 'otpTimerLabel'):
                self.otpTimerLabel.setText("OTP sent successfully!")

            toast = Toast(parent=self, message="OTP sent successfully! Check your email.", icon_path="Icons/check.png",duration=2000)
            toast.show_toast()
            self.sendOtpBtn.setText("Send OTP")
            self.sendOtpBtn.setEnabled(True)
        else:
            toast = Toast(parent=self, message="Failed to send OTP.", icon_path="Icons/warning.png",duration=2000)
            toast.show_toast()
            self.sendOtpBtn.setText("Send OTP")
            self.sendOtpBtn.setEnabled(True)

    def update_otp_timer(self):
        """Update OTP timer display - kept for compatibility but disabled"""
        pass

    def verify_otp(self):
        """Verify OTP and proceed to password reset"""
        otp = self.otpEdit.text().strip()

        if not otp:
            toast = Toast(parent=self, message="Please enter the OTP.", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        if not self.otp_email:
            toast = Toast(parent=self, message="Email not found. Please restart the process.",
                          icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        # Show loading state
        self.proceedBtn.setText("Verifying...")
        self.proceedBtn.setEnabled(False)
        self.proceedBtn.repaint()  # Force UI update
        QApplication.processEvents()  # Process pending events

        try:
            # Call API to verify OTP first
            success, response = verify_otp_and_reset_password(
                self.otp_email, otp, None  # Send None for password to just verify OTP
            )

            if success:
                # OTP is valid, store it and proceed to password reset
                self.otp_code = otp
                toast = Toast(parent=self, message="OTP verified successfully!", icon_path="Icons/check.png",
                              duration=2000)
                toast.show_toast()
                self.LoginStackedWidget.setCurrentIndex(2)  # Go to new password page
                self.otp_timer.stop()
            else:
                error_msg = response.get('error', 'Invalid OTP')
                toast = Toast(parent=self, message=error_msg, icon_path="Icons/warning.png", duration=2000)
                toast.show_toast()

            self.proceedBtn.setText("Proceed")
            self.proceedBtn.setEnabled(True)

        except Exception as e:
            toast = Toast(parent=self, message="Error verifying OTP", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            self.proceedBtn.setText("Proceed")
            self.proceedBtn.setEnabled(True)

    def reset_password(self):
        """Reset password after OTP has been verified"""
        new_password = self.newPass.text().strip()
        confirm_password = self.confirmPass.text().strip()

        if not all([new_password, confirm_password]):
            toast = Toast(parent=self, message="Please fill all fields", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        if new_password != confirm_password:
            toast = Toast(parent=self, message="Passwords do not match", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        if len(new_password) < 6:
            toast = Toast(parent=self, message="Password must be at least 6 characters long",
                          icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        # Show loading state
        self.submitNewPass.setText("Resetting...")
        self.submitNewPass.setEnabled(False)
        self.submitNewPass.repaint()  # Force UI update
        QApplication.processEvents()  # Process pending events

        try:
            # Call the API to reset password with the verified OTP
            success, response = verify_otp_and_reset_password(
                self.otp_email, self.otp_code, new_password
            )

            if success:
                toast = Toast(parent=self, message="Password reset successfully!", icon_path="Icons/check.png",
                              duration=2000)
                toast.show_toast()
                # Return to login page
                self.navigate_login(0)
                self.clear_otp_fields()
            else:
                error_msg = response.get('error', 'Failed to reset password')
                toast = Toast(parent=self, message=error_msg, icon_path="Icons/warning.png", duration=2000)
                toast.show_toast()

            self.submitNewPass.setText("Reset Password")
            self.submitNewPass.setEnabled(True)

        except Exception as e:
            toast = Toast(parent=self, message="Error resetting password", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            self.submitNewPass.setText("Reset Password")
            self.submitNewPass.setEnabled(True)

    def apply_shadows(self):
        # Your existing shadow code...
        self.userIcon.setGraphicsEffect(create_card_shadow())
        self.passwordIcon.setGraphicsEffect(create_card_shadow())
        self.emailOtpIcon.setGraphicsEffect(create_card_shadow())
        self.otpIcon.setGraphicsEffect(create_card_shadow())
        self.newPassIcon.setGraphicsEffect(create_card_shadow())
        self.confirmPassIcon.setGraphicsEffect(create_card_shadow())

        self.togglePassFrame.setGraphicsEffect(create_card_shadow())
        self.togglePassFrame_2.setGraphicsEffect(create_card_shadow())
        self.togglePassFrame_3.setGraphicsEffect(create_card_shadow())

        self.loginUserName.setGraphicsEffect(create_card_shadow())
        self.loginPassword.setGraphicsEffect(create_card_shadow())
        self.emailOtpEdit.setGraphicsEffect(create_card_shadow())
        self.otpEdit.setGraphicsEffect(create_card_shadow())
        self.newPass.setGraphicsEffect(create_card_shadow())
        self.confirmPass.setGraphicsEffect(create_card_shadow())

        self.loginFrame.setGraphicsEffect(create_card_shadow())

        self.loginBtn.setGraphicsEffect(create_card_shadow())
        self.sendOtpBtn.setGraphicsEffect(create_card_shadow())
        self.proceedBtn.setGraphicsEffect(create_card_shadow())
        self.submitNewPass.setGraphicsEffect(create_card_shadow())
        self.welcome.setGraphicsEffect(create_card_shadow())
        self.label_5.setGraphicsEffect(create_card_shadow())
        self.label_7.setGraphicsEffect(create_card_shadow())
        self.label_11.setGraphicsEffect(create_card_shadow())

    def load_saved_credentials(self):
        settings = QSettings("PetMate", "DesktopApp")
        stay_signed_in = settings.value("stay_signed_in", False, type=bool)

        if stay_signed_in:
            username = settings.value("username", "")
            self.loginUserName.setText(username)
            self.staySignedIn.setChecked(True)

    def attempt_login(self):
        username = self.loginUserName.text().strip()
        password = self.loginPassword.text().strip()
        stay_signed_in = self.staySignedIn.isChecked()

        if not username or not password:
            toast = Toast(parent=self, message="Please enter both username and password", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            return

        # Show loading state
        self.loginBtn.setText("Logging in...")
        self.loginBtn.setEnabled(False)
        self.loginBtn.repaint()  # Force UI update
        QApplication.processEvents()  # Process pending events

        # Start API call in background thread
        self.login_worker = APIWorker(
            'POST',
            f"{API_BASE_URL}/api/desktop-login/",
            {'username': username, 'password': password},
            timeout=10
        )
        self.login_worker.finished.connect(self.on_login_finished)
        self.login_worker.error.connect(self.on_login_error)
        self.login_worker.start()

    def on_login_finished(self, success, response):
        """Handle login response from API worker"""
        stay_signed_in = self.staySignedIn.isChecked()
        if success:
            # Save credentials if "Stay Signed In" is checked
            if stay_signed_in:
                settings = QSettings("PetMate", "DesktopApp")
                settings.setValue("username", self.loginUserName.text())
                settings.setValue("stay_signed_in", True)
            else:
                # Clear any saved credentials
                settings = QSettings("PetMate", "DesktopApp")
                settings.remove("username")
                settings.setValue("stay_signed_in", False)

            # Store user data and check if first-time setup is needed
            self.user_data = response.get('user')
            self.accept()  # Login successful
        else:
            toast = Toast(parent=self, message="Username or password not found", icon_path="Icons/warning.png", duration=2000)
            toast.show_toast()
            self.loginBtn.setText("Login")
            self.loginBtn.setEnabled(True)

    def on_login_error(self, error_msg):
        """Handle login error"""
        toast = Toast(parent=self, message=error_msg, icon_path="Icons/warning.png", duration=2000)
        toast.show_toast()
        self.loginBtn.setText("Login")
        self.loginBtn.setEnabled(True)

    def close_app(self):
        self.reject()  # Close the application
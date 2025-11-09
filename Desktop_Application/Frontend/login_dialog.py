import os
import sys
from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSettings, QTimer
import resources_rc
from PyQt6.QtGui import QPixmap
from shadowEffects import create_card_shadow
from Desktop_Application.Backend.api_client import desktop_login, send_otp, verify_otp_and_reset_password
import requests
from config_loader import API_BASE_URL


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
            self.show_error("Please enter your email address")
            return

        # Show loading state
        self.sendOtpBtn.setText("Sending...")
        self.sendOtpBtn.setEnabled(False)

        try:
            # Call the API to send OTP
            success, response = send_otp(email)

            if success:
                self.otp_email = email
                self.otpFrame.setVisible(True)
                self.emailOtp.setVisible(False)

                # Removed timer functionality
                if hasattr(self, 'otpTimerLabel'):
                    self.otpTimerLabel.setText("OTP sent successfully!")

                self.show_success("OTP sent successfully! Check your email.")
                self.sendOtpBtn.setText("Send OTP")
                self.sendOtpBtn.setEnabled(True)
            else:
                self.show_error(response.get('error', 'Failed to send OTP'))
                self.sendOtpBtn.setText("Send OTP")
                self.sendOtpBtn.setEnabled(True)

        except Exception as e:
            self.show_error(f"Error sending OTP: {str(e)}")
            self.sendOtpBtn.setText("Send OTP")
            self.sendOtpBtn.setEnabled(True)

    def update_otp_timer(self):
        """Update OTP timer display - kept for compatibility but disabled"""
        pass

    def verify_otp(self):
        """Verify OTP and proceed to password reset"""
        otp = self.otpEdit.text().strip()

        if not otp:
            self.show_error("Please enter the OTP")
            return

        if not self.otp_email:
            self.show_error("Email not found. Please restart the process.")
            return

        # Show loading state
        self.proceedBtn.setText("Verifying...")
        self.proceedBtn.setEnabled(False)

        try:
            # Store OTP for later verification during password reset
            self.otp_code = otp

            # For now, proceed directly to password reset page
            # The actual OTP verification will happen during password reset
            self.LoginStackedWidget.setCurrentIndex(2)  # Go to new password page
            self.proceedBtn.setText("Proceed")
            self.proceedBtn.setEnabled(True)
            self.otp_timer.stop()

        except Exception as e:
            self.show_error(f"Error verifying OTP: {str(e)}")
            self.proceedBtn.setText("Proceed")
            self.proceedBtn.setEnabled(True)

    def reset_password(self):
        """Reset password with OTP verification"""
        new_password = self.newPass.text().strip()
        confirm_password = self.confirmPass.text().strip()
        otp = self.otp_code  # Use the stored OTP

        if not all([new_password, confirm_password, otp]):
            self.show_error("Please fill all fields")
            return

        if new_password != confirm_password:
            self.show_error("Passwords do not match")
            return

        if len(new_password) < 6:
            self.show_error("Password must be at least 6 characters long")
            return

        # Show loading state
        self.submitNewPass.setText("Resetting...")
        self.submitNewPass.setEnabled(False)

        try:
            # Call the API to verify OTP and reset password
            success, response = verify_otp_and_reset_password(
                self.otp_email, otp, new_password
            )

            if success:
                self.show_success("Password reset successfully!")
                # Return to login page
                self.navigate_login(0)
                self.clear_otp_fields()
            else:
                error_msg = response.get('error', 'Failed to reset password')
                self.show_error(f"Password reset failed: {error_msg}")
                self.submitNewPass.setText("Reset Password")
                self.submitNewPass.setEnabled(True)

        except Exception as e:
            self.show_error(f"Error resetting password: {str(e)}")
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
            self.show_error("Please enter both username and password")
            return

        # Show loading state
        self.loginBtn.setText("Logging in...")
        self.loginBtn.setEnabled(False)

        # Attempt login via API
        success, response = desktop_login(username, password)

        if success:
            # Save credentials if "Stay Signed In" is checked
            if stay_signed_in:
                settings = QSettings("PetMate", "DesktopApp")
                settings.setValue("username", username)
                settings.setValue("stay_signed_in", True)
            else:
                # Clear any saved credentials
                settings = QSettings("PetMate", "DesktopApp")
                settings.remove("username")
                settings.setValue("stay_signed_in", False)

            # Store user data and check if first-time setup is needed
            self.user_data = response['user']
            self.accept()  # Login successful
        else:
            self.show_error(response.get('error', 'Login failed'))
            self.loginBtn.setText("Login")
            self.loginBtn.setEnabled(True)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

    def close_app(self):
        self.reject()  # Close the application
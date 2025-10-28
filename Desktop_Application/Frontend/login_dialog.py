
import os
import sys
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSettings
import resources_rc
from PyQt6.QtGui import QPixmap
from shadowEffects import create_card_shadow
from Desktop_Application.Backend.api_client import desktop_login


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui-files/LoginCard.ui", self)

        # Setup UI
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply shadows
        self.apply_shadows()

        # Connect signals
        self.loginBtn.clicked.connect(self.attempt_login)
        self.closeLoginBtn.clicked.connect(self.close_app)

        # Load saved credentials if "Stay Signed In" was checked
        self.load_saved_credentials()

    def apply_shadows(self):
        self.loginFrame.setGraphicsEffect(create_card_shadow())
        self.loginBtn.setGraphicsEffect(create_card_shadow())


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
        QMessageBox.warning(self, "Login Failed", message)

    def close_app(self):
        self.reject()  # Close the application
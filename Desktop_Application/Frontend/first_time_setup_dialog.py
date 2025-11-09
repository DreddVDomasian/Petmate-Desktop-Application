
import os
import sys
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
from shadowEffects import create_card_shadow
import resources_rc
from Desktop_Application.Backend.api_client import first_time_setup


class FirstTimeSetupDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        uic.loadUi("ui-files/firstTime-setup.ui", self)
        self.close.clicked.connect(self.close_app)
        self.user_data = user_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply shadows
        self.firstLoginFrame.setGraphicsEffect(create_card_shadow())
        self.completeSetupBtn.setGraphicsEffect(create_card_shadow())
        self.label_9.setGraphicsEffect(create_card_shadow())

        # Pre-fill username (can be changed)
        self.username.setText(self.user_data['username'])

        # Connect signals
        self.completeSetupBtn.clicked.connect(self.complete_setup)

    def complete_setup(self):
        # Get all inputs
        full_name = self.fullName.text().strip()
        email = self.email.text().strip()
        phone = self.PhoneNum.text().strip()
        username = self.username.text().strip()
        new_password = self.newPassword.text().strip()
        confirm_password = self.confirmPassword.text().strip()

        # Validation
        if not all([full_name, email, username, new_password, confirm_password]):
            self.show_error("Please fill in all required fields")
            return

        if new_password != confirm_password:
            self.show_error("Passwords do not match")
            return

        if len(new_password) < 6:
            self.show_error("Password must be at least 6 characters")
            return

        # Show loading state
        self.completeSetupBtn.setText("Setting up...")
        self.completeSetupBtn.setEnabled(False)

        # Call first-time setup API
        success, response = first_time_setup(
            user_id=self.user_data['id'],
            full_name=full_name,
            email=email,
            phone=phone,
            username=username,
            new_password=new_password
        )

        if success:
            self.user_data = response['user']
            self.accept()  # Setup completed successfully
        else:
            self.show_error(response.get('error', 'Setup failed'))
            self.completeSetupBtn.setText("Complete Setup")
            self.completeSetupBtn.setEnabled(True)

    def show_error(self, message):
        QMessageBox.warning(self, "Setup Failed", message)
    def close_app(self):
        self.reject()  # Close the application
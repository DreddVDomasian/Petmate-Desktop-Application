
import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit
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
        self.password_toggle()

    def password_toggle(self):
        self.setup_password_toggle(self.newPassword, self.loginShowPass)
        self.setup_password_toggle(self.confirmPassword, self.loginShowPass_2)

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
    def setup_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply shadows
        self.firstLoginFrame.setGraphicsEffect(create_card_shadow())
        self.completeSetupBtn.setGraphicsEffect(create_card_shadow())
        self.label_9.setGraphicsEffect(create_card_shadow())

        self.fullName.setGraphicsEffect(create_card_shadow())
        self.username.setGraphicsEffect(create_card_shadow())
        self.email.setGraphicsEffect(create_card_shadow())
        self.PhoneNum.setGraphicsEffect(create_card_shadow())
        self.newPassword.setGraphicsEffect(create_card_shadow())
        self.confirmPassword.setGraphicsEffect(create_card_shadow())

        self.fullnameIcon.setGraphicsEffect(create_card_shadow())
        self.usernameIcon.setGraphicsEffect(create_card_shadow())
        self.emailIcon.setGraphicsEffect(create_card_shadow())
        self.phoneNumIcon.setGraphicsEffect(create_card_shadow())
        self.newPassIcon.setGraphicsEffect(create_card_shadow())
        self.confirmpassIcon.setGraphicsEffect(create_card_shadow())


        self.togglePassFrame.setGraphicsEffect(create_card_shadow())
        self.togglePassFrame_2.setGraphicsEffect(create_card_shadow())

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
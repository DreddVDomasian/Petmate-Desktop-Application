
import sys
import os

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication, QDialog
from app import MainUI
from login_dialog import LoginDialog
from first_time_setup_dialog import FirstTimeSetupDialog
from PyQt6.QtCore import QSettings


def load_fonts():
    """Load custom fonts for the application"""
    try:
        # Get the directory where main.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "font", "Montserrat", "Montserrat-VariableFont_wght.ttf")

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                print("✅ Font loaded successfully")
            else:
                print("❌ Failed to load font")
        else:
            print(f"❌ Font file not found at: {font_path}")
    except Exception as e:
        print(f"❌ Error loading font: {e}")

def main():
    app = QApplication(sys.argv)
    load_fonts()
    # Check if user should stay signed in
    settings = QSettings("PetMate", "DesktopApp")
    stay_signed_in = settings.value("stay_signed_in", False, type=bool)

    user_data = None

    # Show login dialog if not staying signed in
    if not stay_signed_in:
        login_dialog = LoginDialog()
        if login_dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)  # User canceled login
        user_data = login_dialog.user_data

    # Check if first-time setup is required
    if user_data and user_data.get('force_password_change', False):
        setup_dialog = FirstTimeSetupDialog(user_data)
        if setup_dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)  # User canceled setup
        user_data = setup_dialog.user_data

    # Now show the main application
    main_window = MainUI()
    main_window.current_user = user_data  # Store user data in main window

    # Add logout functionality
    def handle_logout():
        """Handle logout by showing login dialog again"""
        # Clear saved credentials
        settings = QSettings("PetMate", "DesktopApp")
        settings.remove("username")
        settings.setValue("stay_signed_in", False)

        # Close main window
        main_window.close()

        # Show login dialog again
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = login_dialog.user_data
            # Check if first-time setup needed
            if user_data and user_data.get('force_password_change', False):
                setup_dialog = FirstTimeSetupDialog(user_data)
                if setup_dialog.exec() != QDialog.DialogCode.Accepted:
                    app.quit()
                    return
                user_data = setup_dialog.user_data

            # Update main window with new user
            main_window.current_user = user_data
            main_window.show()
        else:
            app.quit()

    # Connect logout button (you'll need to add this to your Home.ui)
    if hasattr(main_window, 'logoutBtn'):
        main_window.logoutBtn.clicked.connect(handle_logout)

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
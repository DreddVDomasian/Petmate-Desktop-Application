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
                print("Font loaded successfully")
            else:
                print("❌ Failed to load font")
        else:
            print(f"❌ Font file not found at: {font_path}")
    except Exception as e:
        print(f"❌ Error loading font: {e}")

def main():
    app = QApplication(sys.argv)
    load_fonts()

    while True:
        # Check if user should stay signed in
        settings = QSettings("PetMate", "DesktopApp")
        stay_signed_in = settings.value("stay_signed_in", False, type=bool)

        user_data = None
        if stay_signed_in:
            # Try to get user data from settings
            user_data = settings.value("user_data")
            if not user_data:
                # No saved user data, show login
                stay_signed_in = False
                settings.setValue("stay_signed_in", False)

        # Show login dialog if not staying signed in
        if not stay_signed_in:
            login_dialog = LoginDialog()
            result = login_dialog.exec()

            if result != QDialog.DialogCode.Accepted:
                break  # User wants to quit completely

            user_data = login_dialog.user_data

            # Save user data if "Stay Signed In" is checked
            if login_dialog.staySignedIn.isChecked():
                settings.setValue("user_data", user_data)
                settings.setValue("stay_signed_in", True)

        # Check if first-time setup is required
        if user_data and user_data.get('force_password_change', False):
            setup_dialog = FirstTimeSetupDialog(user_data)
            if setup_dialog.exec() != QDialog.DialogCode.Accepted:
                continue  # Restart login process
            user_data = setup_dialog.user_data
            # Update saved user data if staying signed in
            if stay_signed_in:
                settings.setValue("user_data", user_data)

        # Create main window
        main_window = MainUI(user_data=user_data)

        # Add a flag to track logout
        main_window._user_logged_out = False

        def handle_logout():
            """Handle logout by clearing credentials and marking for restart"""
            # Clear saved credentials
            settings = QSettings("PetMate", "DesktopApp")
            settings.remove("username")
            settings.setValue("stay_signed_in", False)
            settings.remove("user_data")

            # Mark that user explicitly logged out
            main_window._user_logged_out = True

            # Close main window to return to login loop
            main_window.close()

        main_window.handle_logout = handle_logout

        # Connect logout button
        if hasattr(main_window, 'logoutBtn'):
            main_window.logoutBtn.clicked.connect(handle_logout)

        main_window.show()
        app.exec()  # This will block until main window is closed

        # After main window closes, check if we should restart
        # Only restart if user explicitly logged out
        if hasattr(main_window, '_user_logged_out') and main_window._user_logged_out:
            continue  # Restart login process
        else:
            break  # Exit completely (X button was pressed)

    sys.exit(0)


if __name__ == "__main__":
    main()
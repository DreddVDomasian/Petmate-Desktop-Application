import sys
import os

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication, QDialog
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

    # Ensure relative paths like ui-files/ and Icons/ still work when packaged.
    # For PyInstaller onedir builds, keeping cwd at the exe directory avoids missing UI/assets.
    try:
        if getattr(sys, 'frozen', False):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        pass

    # Ensure project root is on sys.path so absolute imports like
    # `Desktop_Application.Backend...` work even when running this file directly.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Show a startup loading modal and keep it visible until the first window
    # (login or main UI) is actually shown.
    startup_overlay = None
    try:
        from PyQt6.QtCore import Qt, QTimer
        from loading_overlay import LoadingOverlay

        startup_overlay = LoadingOverlay(
            None,
            message="Starting PetMate...",
            submessage="Loading application",
            indeterminate=False
        )
        startup_overlay.setWindowFlags(
            startup_overlay.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )
        startup_overlay.set_progress(5)
        startup_overlay.show()
        app.processEvents()

        def _set_startup_progress(value: int, title: str = None, subtitle: str = None):
            if startup_overlay is None:
                return
            if title is not None or subtitle is not None:
                startup_overlay.set_message(title or "Starting PetMate...", subtitle)
            startup_overlay.set_indeterminate(False)
            startup_overlay.set_progress(value)
            app.processEvents()

        _set_startup_progress(10, "Starting PetMate...", "Loading modules")

        # Deferred imports so the overlay can paint before heavy initialization
        from login_dialog import LoginDialog
        from first_time_setup_dialog import FirstTimeSetupDialog
        from app import MainUI

        _set_startup_progress(35, "Starting PetMate...", "Preparing login")
    except Exception:
        # If anything goes wrong during early startup, ensure the overlay closes
        if startup_overlay is not None:
            startup_overlay.hide()
            startup_overlay.deleteLater()
            app.processEvents()
        raise

    def _hide_startup_overlay():
        nonlocal startup_overlay
        if startup_overlay is None:
            return

        # Finish the bar before hiding
        try:
            startup_overlay.set_indeterminate(False)
            startup_overlay.set_progress(100)
            app.processEvents()
        except Exception:
            pass
        startup_overlay.hide()
        startup_overlay.deleteLater()
        startup_overlay = None

    while True:
        # Check if user should stay signed in
        settings = QSettings("PetMate", "DesktopApp")
        stay_signed_in = settings.value("stay_signed_in", False, type=bool)

        # If the user just logged in this cycle, we delay persisting "stay signed in"
        # until after first-time setup is completed.
        stay_signed_in_requested = False

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
            # Make sure the login dialog is on screen before hiding the startup overlay
            login_dialog = LoginDialog()
            try:
                if startup_overlay is not None:
                    startup_overlay.set_message("Starting PetMate...", "Opening login")
                    startup_overlay.set_progress(55)
                    app.processEvents()
            except Exception:
                pass
            login_dialog.show()
            app.processEvents()
            QTimer.singleShot(0, _hide_startup_overlay)
            result = login_dialog.exec()

            if result != QDialog.DialogCode.Accepted:
                break  # User wants to quit completely

            user_data = login_dialog.user_data

            stay_signed_in_requested = bool(login_dialog.staySignedIn.isChecked())

        # Check if first-time setup is required
        if user_data and user_data.get('force_password_change', False):
            setup_dialog = FirstTimeSetupDialog(user_data)
            if setup_dialog.exec() != QDialog.DialogCode.Accepted:
                # User closed/cancelled setup. Clear "stay signed in" so we don't loop.
                settings = QSettings("PetMate", "DesktopApp")
                settings.remove("username")
                settings.setValue("stay_signed_in", False)
                settings.remove("user_data")
                continue  # Restart login process
            user_data = setup_dialog.user_data

            # Persist stay-signed-in only after setup is complete.
            if stay_signed_in or stay_signed_in_requested:
                settings.setValue("user_data", user_data)
                settings.setValue("stay_signed_in", True)

        # If no first-time setup is needed, persist stay-signed-in right after login.
        if user_data and (stay_signed_in_requested and not user_data.get('force_password_change', False)):
            settings.setValue("user_data", user_data)
            settings.setValue("stay_signed_in", True)

        # Create main window (can be slow); keep overlay visible until shown
        if startup_overlay is None:
            # If we already hid it (e.g., after login), show a brief one again
            try:
                from PyQt6.QtCore import Qt
                from loading_overlay import LoadingOverlay

                startup_overlay = LoadingOverlay(
                    None,
                    message="Opening PetMate...",
                    submessage="Preparing dashboard",
                    indeterminate=False
                )
                startup_overlay.setWindowFlags(
                    startup_overlay.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
                )
                startup_overlay.set_progress(60)
                startup_overlay.show()
                app.processEvents()
            except Exception:
                startup_overlay = None

        try:
            if startup_overlay is not None:
                startup_overlay.set_message("Opening PetMate...", "Building dashboard")
                startup_overlay.set_progress(70)
                app.processEvents()
        except Exception:
            pass

        def _dashboard_progress(value: int, title: str = None, subtitle: str = None):
            if startup_overlay is None:
                return
            try:
                if title is not None or subtitle is not None:
                    startup_overlay.set_message(title or "Opening PetMate...", subtitle)
                startup_overlay.set_indeterminate(False)
                startup_overlay.set_progress(value)
                app.processEvents()
            except Exception:
                pass

        main_window = MainUI(user_data=user_data, startup_progress=_dashboard_progress)

        try:
            if startup_overlay is not None:
                startup_overlay.set_message("Opening PetMate...", "Finalizing")
                startup_overlay.set_progress(95)
                app.processEvents()
        except Exception:
            pass

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
        app.processEvents()
        QTimer.singleShot(0, _hide_startup_overlay)
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
from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtCore import Qt
from PyQt6 import uic
import os
import sys
from Desktop_Application.Frontend.app import resource_path


class LoadingOverlay(QFrame):  # Changed from QWidget to QFrame!
    def __init__(self, parent=None, message="Loading...", submessage=None, indeterminate=True):
        super().__init__(parent)

        # Always initialize _indeterminate before any UI logic
        self._indeterminate = None

        # Load your UI file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "ui-files", "loading_overlay.ui")

        print(f"DEBUG: Loading UI from: {ui_path}")
        print(f"DEBUG: UI file exists: {os.path.exists(ui_path)}")

        try:
            uic.loadUi(resource_path("ui-files/loading_overlay.ui"), self)
            print("✅ UI loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading UI: {e}")
            # Fallback to manual creation
            self._create_fallback_ui(message=message, submessage=submessage)
            return

        # Make it frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Update messages
        self.set_message(message, submessage)

        self.set_indeterminate(indeterminate)

        # Don't center in __init__ - wait for showEvent

    def _create_fallback_ui(self, message="Loading...", submessage=None):
        """Create UI manually if loading fails"""
        print("DEBUG: Creating fallback UI")
        from PyQt6.QtWidgets import QVBoxLayout, QLabel, QProgressBar

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        self.loadingText = QLabel(message or "Loading...")
        self.loadingText.setStyleSheet("""
            font: 81 16pt "Montserrat ExtraBold";
            color: #333;
            qproperty-alignment: AlignCenter;
        """)
        layout.addWidget(self.loadingText)

        self.loadingSubtext = QLabel(submessage or "Please wait")
        self.loadingSubtext.setStyleSheet("""
            font: 57 12pt "Montserrat Medium";
            color: #666;
            qproperty-alignment: AlignCenter;
        """)
        layout.addWidget(self.loadingSubtext)

        self.progressBar = QProgressBar()
        # Default to indeterminate; callers can switch to determinate via set_indeterminate(False)
        self.progressBar.setRange(0, 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background-color: #F8F8F8;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #78B3CE;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progressBar)

        # Always initialize _indeterminate in fallback UI as well
        self._indeterminate = None

        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QFrame {
                background-color: rgb(254, 254, 254);
                border-radius: 15px;
                border: 2px solid #78B3CE;
            }
        """)

    def showEvent(self, event):
        """Override show event to center on MainContent"""
        super().showEvent(event)

        # Use timer to ensure widget is fully shown before centering
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self.center_on_maincontent)

    def center_on_maincontent(self):
        """Center the overlay on the MainContent widget"""
        try:
            print("DEBUG: Centering on MainContent...")

            # Get the MainContent widget
            maincontent = None
            if self.parent() and hasattr(self.parent(), 'MainContent'):
                maincontent = self.parent().MainContent
                print(f"DEBUG: Found MainContent: {maincontent}")

            if maincontent:
                # Get MainContent's geometry
                mc_geometry = maincontent.geometry()
                print(f"DEBUG: MainContent geometry: {mc_geometry}")

                # Get MainContent's center
                center_x = mc_geometry.x() + (mc_geometry.width() // 2)
                center_y = mc_geometry.y() + (mc_geometry.height() // 2)

                # Calculate overlay position
                x = center_x - (self.width() // 2)
                y = center_y - (self.height() // 2)

                print(f"DEBUG: Moving overlay to ({x}, {y})")
                self.move(x, y)

                # Ensure it's on top
                self.raise_()

            else:
                print("DEBUG: MainContent not found, centering on parent")
                self.center_on_parent()

        except Exception as e:
            print(f"DEBUG: Error centering: {e}")
            self.center_on_parent()

    def center_on_parent(self):
        """Fallback: center on parent widget"""
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            print(f"DEBUG: Fallback position: ({x}, {y})")
            self.move(x, y)
            return

        # Startup / no-parent case: center on the primary screen
        try:
            from PyQt6.QtWidgets import QApplication

            screen = QApplication.primaryScreen()
            if screen:
                rect = screen.availableGeometry()
                x = rect.x() + (rect.width() - self.width()) // 2
                y = rect.y() + (rect.height() - self.height()) // 2
                print(f"DEBUG: Screen fallback position: ({x}, {y})")
                self.move(x, y)
        except Exception as e:
            print(f"DEBUG: Screen centering failed: {e}")

    def set_message(self, message, submessage=None):
        """Update the loading message"""
        if hasattr(self, 'loadingText'):
            self.loadingText.setText(message)
        if submessage and hasattr(self, 'loadingSubtext'):
            self.loadingSubtext.setText(submessage)

    def set_indeterminate(self, indeterminate: bool):
        """Toggle progress bar indeterminate/determinate mode."""
        if not hasattr(self, 'progressBar'):
            self._indeterminate = indeterminate
            return

        if self._indeterminate == indeterminate:
            return

        self._indeterminate = indeterminate
        if indeterminate:
            self.progressBar.setRange(0, 0)
        else:
            self.progressBar.setRange(0, 100)
            # Ensure it starts from 0 unless already set
            try:
                if self.progressBar.value() < 0 or self.progressBar.value() > 100:
                    self.progressBar.setValue(0)
            except Exception:
                self.progressBar.setValue(0)

    def set_progress(self, value: int):
        """Set determinate progress (0-100). No-op if indeterminate."""
        if not hasattr(self, 'progressBar'):
            return
        if self._indeterminate:
            return
        value = max(0, min(100, int(value)))
        self.progressBar.setValue(value)
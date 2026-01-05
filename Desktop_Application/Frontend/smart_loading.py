"""
Smart Loading Modal Manager - Auto-show loading for slow API calls
Prevents UI freezing by showing loading indicators during network operations
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from loading_overlay import LoadingOverlay
import time


class SmartLoadingManager:
    """
    Automatically shows loading modals for slow API calls
    
    Features:
    - Auto-show after 500ms (prevents flashing for fast requests)
    - Configurable messages
    - Easy integration with async_helper
    - Graceful dismissal
    
    Usage:
        manager = SmartLoadingManager(main_window)
        
        manager.start("Loading patients...")
        # Make API call
        manager.stop()
    """
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.loading_modal = None
        self.show_timer = QTimer()
        self.show_timer.setSingleShot(True)
        self.show_timer.timeout.connect(self._show_modal)
        self.start_time = None
        self.min_display_time = 500  # Minimum 500ms display
        
    def start(self, title="Loading...", subtitle=None, show_delay=500):
        """
        Start loading indicator
        
        Args:
            title: Main message
            subtitle: Secondary message
            show_delay: Delay before showing (500ms prevents flashing)
        """
        self.start_time = time.time()
        self._title = title
        self._subtitle = subtitle
        
        # Only show after delay (prevents flashing for fast requests)
        self.show_timer.start(show_delay)
    
    def stop(self):
        """Stop loading indicator"""
        self.show_timer.stop()
        
        # Ensure minimum display time
        elapsed = (time.time() - self.start_time) * 1000 if self.start_time else 0
        remaining = max(0, self.min_display_time - int(elapsed))
        
        if remaining > 0:
            QTimer.singleShot(remaining, self._hide_modal)
        else:
            self._hide_modal()
    
    def _show_modal(self):
        """Internal: Show the loading modal"""
        if not self.loading_modal:
            self.loading_modal = LoadingOverlay(
                self.parent,
                message=self._title,
                submessage=self._subtitle
            )
        
        self.loading_modal.set_message(self._title, self._subtitle)
        self.loading_modal.show()
    
    def _hide_modal(self):
        """Internal: Hide the loading modal"""
        if self.loading_modal:
            self.loading_modal.hide()


class ProgressiveLoadingModal(QFrame):
    """
    Enhanced loading modal with progress tracking
    Shows estimated time remaining
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(254, 254, 254, 250);
                border-radius: 15px;
                border: 2px solid #78B3CE;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        self.title_label = QLabel("Processing...")
        self.title_label.setFont(QFont("Montserrat", 14, QFont.Weight.ExtraBold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #333;")
        layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Please wait...")
        self.subtitle_label.setFont(QFont("Montserrat", 11, QFont.Weight.Medium))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #666;")
        layout.addWidget(self.subtitle_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
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
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Montserrat", 10, QFont.Weight.Normal))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #999;")
        layout.addWidget(self.status_label)
        
        self.setFixedSize(450, 220)
        self.start_time = None
    
    def start(self, title, subtitle=None):
        """Start loading"""
        self.title_label.setText(title)
        if subtitle:
            self.subtitle_label.setText(subtitle)
        self.status_label.setText("Processing...")
        self.start_time = time.time()
        self.show()
        self.center_on_parent()
    
    def update_status(self, status_text):
        """Update status text"""
        self.status_label.setText(status_text)
    
    def stop(self):
        """Stop loading"""
        self.hide()
    
    def center_on_parent(self):
        """Center on parent window"""
        if self.parent():
            parent_rect = self.parent().rect()
            self.move(
                parent_rect.center().x() - self.width() // 2,
                parent_rect.center().y() - self.height() // 2
            )


class BatchOperationLoader:
    """
    For operations that process multiple items
    Shows progress and item count
    """
    
    def __init__(self, parent, total_items):
        self.parent = parent
        self.total_items = total_items
        self.processed_items = 0
        
        self.modal = QFrame(parent)
        self.modal.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.modal.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.modal.setStyleSheet("""
            QFrame {
                background-color: rgba(254, 254, 254, 250);
                border-radius: 15px;
                border: 2px solid #78B3CE;
            }
        """)
        
        layout = QVBoxLayout(self.modal)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        self.title_label = QLabel("Processing...")
        self.title_label.setFont(QFont("Montserrat", 14, QFont.Weight.ExtraBold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #333;")
        layout.addWidget(self.title_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, total_items)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
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
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Montserrat", 11, QFont.Weight.Medium))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
        self.modal.setFixedSize(450, 200)
    
    def start(self, title):
        """Start batch operation"""
        self.title_label.setText(title)
        self.processed_items = 0
        self.progress_bar.setValue(0)
        self._update_status()
        
        if self.parent():
            parent_rect = self.parent().rect()
            self.modal.move(
                parent_rect.center().x() - self.modal.width() // 2,
                parent_rect.center().y() - self.modal.height() // 2
            )
        
        self.modal.show()
    
    def update(self, increment=1):
        """Update progress"""
        self.processed_items += increment
        self.progress_bar.setValue(self.processed_items)
        self._update_status()
    
    def _update_status(self):
        """Update status text"""
        percent = int((self.processed_items / self.total_items) * 100) if self.total_items > 0 else 0
        self.status_label.setText(f"{self.processed_items}/{self.total_items} ({percent}%)")
    
    def stop(self):
        """Stop and hide"""
        self.modal.hide()

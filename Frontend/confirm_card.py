from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class ConfirmCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ConfirmDialog.ui", self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # Optional: self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def show_card(self):
        if self.parent():
            parent_widget = self.parent()
            # Center sa parent
            x = (parent_widget.width() - self.width()) // 2
            y = (parent_widget.height() - self.height()) // 2
            self.move(x, y)

        # Fade in animation
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.anim = anim  # Keep reference para di ma-garbage collect

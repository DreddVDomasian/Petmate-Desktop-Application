from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from  shadowEffects import *
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QRect

class ReminderPopup(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("reminderPopUp.ui", self)  # load your reminder popup UI

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.remidersChecklists.setGraphicsEffect(create_card_shadow())

        self.DoneBtn.clicked.connect(self.done_reminder)
        if parent:
            parent.installEventFilter(self)

    def show_reminder(self):
        if self.parent():
            parent_widget = self.parent()
            # Center on parent
            x = (parent_widget.width() - self.width()) // 2
            y = (parent_widget.height() - self.height()) // 2
            self.move(x, y)

        # Fade in
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.anim = anim  # keep reference

    def eventFilter(self, obj, event):
        if obj == self.parent():
            if self.isVisible():
                if event.type() == event.Type.MouseButtonPress:
                    if not self.geometry().contains(event.pos()):
                        self.done_reminder()
                        return True
                elif event.type() == event.Type.Resize:
                    x = (obj.width() - self.width()) // 2
                    y = (obj.height() - self.height()) // 2
                    self.move(x, y)
        return super().eventFilter(obj, event)

    def done_reminder(self):
        self.hide()


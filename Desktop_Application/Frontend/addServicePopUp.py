import os
import sys

# ETO ANG SAGGOT
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)      # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate,QTimer
from  shadowEffects import *
from input_styles import *
from toast import Toast
from config_loader import API_BASE_URL
import requests

class AddServicePopUp(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/addService.ui", self)
        self.setGraphicsEffect(create_card_shadow())
        self.serviceDescription.setGraphicsEffect(create_card_shadow())
        self.serviceNameLineEdit.setGraphicsEffect(create_card_shadow())
        self.addServiceBtn.setGraphicsEffect(create_card_shadow())
        self.cancelAddServiceBtn.setGraphicsEffect(create_card_shadow())


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
    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)
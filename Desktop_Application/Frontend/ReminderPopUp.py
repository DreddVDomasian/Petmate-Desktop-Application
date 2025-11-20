import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget,QLabel
from  shadowEffects import *
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QRect, QTimer
from config_loader import API_BASE_URL

class ReminderPopup(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/reminderPopUp.ui", self)  # load your reminder popup UI
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.remidersChecklists.setGraphicsEffect(create_card_shadow())

        self.reminderLayout = self.reminderScrollAreaContents.layout()
        self.reminderLayout.setSpacing(10)
        self.reminderLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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

        if self.main_window and hasattr(self.main_window, "selected_pet_id"):
            self.load_reminder(self.main_window.selected_pet_id)
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

    def load_reminder(self, pet_id):
        response = requests.get(f"{API_BASE_URL}/api/reminders/?pet_id={pet_id}")
        if response.status_code == 200:
            reminders = response.json()

        else:
            reminders = []

        while self.reminderLayout.count():
            child = self.reminderLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if reminders:
            pet_name = reminders[0].get("pet_name", "")
            self.reminderForLabel.setText(f"REMINDERS FOR {pet_name.upper()}")

        for reminder in reminders:
            card = uic.loadUi("ui-files/reminderCard.ui")
            card.typeReq.setText(reminder["type"])
            card.dateReq.setText(self.main_window.format_date(reminder["date"]))
            if not reminder["time"] or reminder["time"] == "null":
                layout = card.layout()
                layout.removeWidget(card.timeOptional)
                card.timeOptional.deleteLater()  # deletes widget so no space is reserved
            else:
                card.timeOptional.setText(reminder["time"])
            card.serviceOptional.setText(reminder["service"])

            reminder_id = reminder["id"]
            reminder_type = reminder["type"].lower()  # "appointment" or "service"
            card.markAsDone.clicked.connect(lambda _, rid=reminder_id, rtype=reminder_type: self.complete_reminder(rid, rtype))

            card.setGraphicsEffect(create_card_shadow())
            self.reminderLayout.insertWidget(0, card)

    def complete_reminder(self, reminder_id, reminder_type):
        url = ""
        if reminder_type == "appointment":
            url = f"{API_BASE_URL}/api/walkIn/{reminder_id}/"
        elif reminder_type == "service return":
            url = f"{API_BASE_URL}/api/services/{reminder_id}/"

        if not url:
            return

        response = requests.patch(url, json={"status": "completed"})
        if response.status_code in [200, 202]:
            print("Reminder marked as completed")

            # Refresh pet profile UI without navigation
            if self.main_window:
                self.main_window.refresh_current_pet_profile()

            # Delay UI refresh to avoid deleting active widgets mid-callback
            QTimer.singleShot(100, lambda: self._safe_refresh())
        else:
            print("Failed:", response.text)

    def _safe_refresh(self):
        """Safely reload reminders and services after completion"""
        self.load_reminder(self.main_window.selected_pet_id)
        self.main_window.load_scheduled_services()
        self.main_window.appointmentCard.load_appointments(1)

        # ✅ ADD THIS: Reload the services for the current pet
        if hasattr(self.main_window, 'selected_pet_id') and self.main_window.selected_pet_id:
            self.main_window.load_services_for_pet(self.main_window.selected_pet_id)
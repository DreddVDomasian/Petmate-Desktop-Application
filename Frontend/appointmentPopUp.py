import os
import sys

# ETO ANG SAGGOT
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget,QCompleter,QLabel,QComboBox
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate
from input_styles import *
from  shadowEffects import *
from toast import Toast
from Backend.petInfoSys.api_client import add_new_appointment
from datetime import datetime
import requests

class AddAppointmentCard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window  # keep reference
        uic.loadUi("addAppointmentCard.ui", self)
        #pending layout
        self.pendingLayout = self.main_window.walkInScrollAreaWidgetContents.layout()
        self.pendingLayout.setSpacing(10)
        self.pendingLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # completed layout
        self.completedLayout = self.main_window.completedScrollAreaWidgetContents.layout()
        self.completedLayout.setSpacing(10)
        self.completedLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # overdue layout
        self.overdueLayout = self.main_window.overdueScrollAreaWidgetContents.layout()
        self.overdueLayout.setSpacing(10)
        self.overdueLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # cancelled layout
        self.cancelledLayout = self.main_window.cancelledScrollAreaWidgetContents.layout()
        self.cancelledLayout.setSpacing(10)
        self.cancelledLayout.setAlignment(Qt.AlignmentFlag.AlignTop)



        #Web Appointment
        self.pendingWebLayout = self.main_window.scrollAreaWebAppPending.layout()
        self.pendingWebLayout.setSpacing(10)
        self.pendingWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Accepted layout
        self.acceptedWebLayout = self.main_window.scrollAreaWebAppAccepted.layout()
        self.acceptedWebLayout.setSpacing(10)
        self.acceptedWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # declined layout
        self.declinedWebLayout = self.main_window.scrollAreaWebAppDecined.layout()
        self.declinedWebLayout.setSpacing(10)
        self.declinedWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.addPopUPFrame.setGraphicsEffect(create_card_shadow())
        self.cancelAddAppointment.setGraphicsEffect(create_card_shadow())
        self.addAppointmentBtn.setGraphicsEffect(create_card_shadow())

        self.selectPatientPopUp.currentIndexChanged.connect(self.on_patient_selected)
        # shaadow
        self.setup_input_shadow()

        self.popUpDateEdit.setDate(QDate.currentDate())
        self.popUpDateEdit.mousePressEvent = lambda event: self.on_date_field_clicked(self.popUpDateEdit)

        self.setup_comboboxes()

        # submit data
        self.addAppointmentBtn.clicked.connect(self.submit_appointment_data)

        # load data
        self.load_walkInAppointments()
        self.web_Appointment()

        self.main_window.websiteBtn.clicked.connect(lambda: self.web_Appointment())

        if parent:
            parent.installEventFilter(self)

    def setup_input_shadow(self):
        for comboBox in self.addPopUPFrame.findChildren(QComboBox):
            comboBox.setGraphicsEffect(create_card_shadow())

        self.popUpDateEdit.setGraphicsEffect(create_card_shadow())
        self.timeEdit.setGraphicsEffect(create_card_shadow())

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

    def load_patients_to_combobox(self):
        response = requests.get("http://127.0.0.1:8000/api/patients/")
        if response.status_code == 200:
            patients = response.json()
            self.selectPatientPopUp.clear()
            self.selectPatientPopUp.addItem("", None)
            for patient in patients:
                parts = [patient['firstName'], patient.get('middleName'), patient['lastName']]
                full_name = " ".join(p for p in parts if p)
                self.selectPatientPopUp.addItem(full_name, patient['id'])

            self.set_dynamic_completer(self.selectPatientPopUp)
        else:
            print("Failed to load patients")

    def on_patient_selected(self, index):
        patient_id = self.selectPatientPopUp.itemData(index)
        if not patient_id:
            self.selectPetPopUp.clear()
            return

        url = f"http://127.0.0.1:8000/api/pets/?owner_id={patient_id}"
        response = requests.get(url)
        if response.status_code == 200:
            pets = response.json()
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            for pet in pets:
                self.selectPetPopUp.addItem(pet['petName'], pet['id'])

            self.set_dynamic_completer(self.selectPetPopUp)
        else:
            print("Failed to load pets")

    def on_date_field_clicked(self, dateEdit):
        if self.main_window:
            self.main_window.show_custom_calendar(dateEdit)

    def setup_comboboxes(self):
        self.selectPetPopUp, self.selectPatientPopUp
        self.load_patients_to_combobox()
        combo_boxes = [self.selectPatientPopUp,self.selectPetPopUp]
        placeholders = ["Select Patient", "Select Pet"]
        for cb, text in zip(combo_boxes, placeholders):
            cb.setEditable(True)
            cb.lineEdit().setReadOnly(False)
            cb.lineEdit().setPlaceholderText(text)
            cb.lineEdit().setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_dynamic_completer(self, comboBox):
        completer = QCompleter(comboBox.model())
        completer.setCompletionColumn(0)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        completer.popup().setStyleSheet(completer_popup_style)
        comboBox.setCompleter(completer)

    def submit_appointment_data(self):
        # get values from UI
        patient_index = self.selectPatientPopUp.currentIndex()
        patient_id = self.selectPatientPopUp.itemData(patient_index)

        pet_index = self.selectPetPopUp.currentIndex()
        pet_id = self.selectPetPopUp.itemData(pet_index)

        date = self.popUpDateEdit.date().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("HH:mm:ss")
        service_name = self.serviceTypeComboBox.currentText()

        # basic validation
        missing = []
        if not patient_id:
            missing.append("Patient")
        if not date:
            missing.append("Date")
        if not time:
            missing.append("Time")
        if not service_name:
            missing.append("Service")

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self.main_window, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # build data
        appointment_data = {
            "owner": patient_id,
            "pet": pet_id,
            "date": date,
            "prefTime": time,
            "service_name": service_name,  # include service
            # add notes or other fields if you have
        }

        # send data to backend
        if add_new_appointment(appointment_data):
            toast = Toast(self.main_window, "Appointment added!", icon_path="Icons/check.png")
            toast.show_toast()
            self.close()
            self.load_walkInAppointments()
        else:
            toast = Toast(self.main_window, "Failed to add appointment!", icon_path="Icons/warning.png")
            toast.show_toast()

    def load_walkInAppointments(self):
        response = requests.get("http://127.0.0.1:8000/api/walkIn/")
        if response.status_code == 200:
            walkInAppointments = response.json()
        else:
            walkInAppointments = []

        # 🧹 clear all layouts before adding new cards
        for layout in [self.pendingLayout, self.completedLayout, self.overdueLayout, self.cancelledLayout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()


        for appt in walkInAppointments:
            card = uic.loadUi("appointmentCard.ui")
            card.ownerName.setText(appt["owner_full_name"].title())
            card.petNameApp.setText(appt["petName"].capitalize())
            card.serviceApp.setText(appt["service_name"].capitalize())
            card.appDate.setText(self.main_window.format_date(appt.get("date")))

            time_str = appt.get("prefTime")
            if time_str:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
                formatted_time = time_obj.strftime("%I:%M %p").lstrip("0")
                card.preferredTime.setText(formatted_time)
            else:
                card.preferredTime.setText("N/A")

            card.setGraphicsEffect(create_card_shadow())

            # 👉 decide which layout
            status = appt.get("status", "pending")
            appt_date = datetime.strptime(appt["date"], "%Y-%m-%d").date()

            if status == "completed":
                card.deleteButton.hide()
                self.completedLayout.addWidget(card)
            elif status == "cancelled":
                card.deleteButton.hide()
                self.cancelledLayout.addWidget(card)
            elif status == "pending":
                self.pendingLayout.addWidget(card)
            elif status == "overdue":
                self.overdueLayout.addWidget(card)

            appointment_id = appt["id"]
            card.deleteButton.clicked.connect(lambda _, a_id=appointment_id: self.cancelled_appointment(a_id))
            card.mousePressEvent = lambda event, pid=appt["pet"]: self.open_pet_from_appointment(pid)

        for layout in [self.pendingLayout, self.completedLayout, self.overdueLayout, self.cancelledLayout]:
            if layout.count() == 0:
                self.add_empty_label(layout)

    def web_Appointment(self):
        response = requests.get("http://127.0.0.1:8000/api/appointments/")
        if response.status_code == 200:
            data = response.json()
            # handle both cases safely
            if isinstance(data, dict) and "appointments" in data:
                appointments = data["appointments"]
            else:
                appointments = data
        else:
            appointments = []

        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        for appoint in appointments:
            card = uic.loadUi("webAppointmentCard.ui")
            card.ownerName.setText(appoint["client_name"].title())
            raw_datetime = appoint.get("appointment_datetime", "")
            # Split into date and time parts
            parts = raw_datetime.split(" ", 1)  # ["2025-09-18", "9:00 AM"]
            date_only = parts[0]
            time_only = parts[1] if len(parts) > 1 else ""
            # Format the date
            formatted_date = self.main_window.format_date(date_only)
            #date + time
            dateAndTime = f"{formatted_date}   {time_only}"

            card.DateTime.setText(dateAndTime)

            card.setGraphicsEffect(create_card_shadow())
            status = appoint.get("status", "pending")

            if status == "pending":
                self.pendingWebLayout.addWidget(card)
            elif status == "accepted":
                self.acceptedWebLayout.addWidget(card)
            elif status == "declined":
                self.declinedWebLayout.addWidget(card)

            webAppointment_id = appoint["id"]
            card.ReviewButton.clicked.connect(lambda: self.main_window.stackedWidget.setCurrentIndex(7))
        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            if layout.count() == 0:
                self.add_empty_label(layout)

    def open_appointment(self, webAppointment_id):
        response = requests.get(f"http://127.0.0.1:8000/api/appointments/{webAppointment_id}/")
        if response.status_code == 200:
            data = response.json()

    def cancelled_appointment(self,appointment_id):
        self.main_window.confirmCard.confirmationMessage.setText("Are you sure you want to cancel \nthis appointment?")
        self.main_window.confirmCard.show_card()
        def clicked_yes():
            url = f"http://127.0.0.1:8000/api/walkIn/{appointment_id}/"
            if url:
                response = requests.patch(url, json={"status": "cancelled"})
                if response.status_code in [200, 202]:
                    print("Reminder marked as cancelled")
                    self.main_window.appointmentCard.load_walkInAppointments()
                else:
                    print("Failed:", response.text)
            self.main_window.confirmCard.hide()
        def clicked_no():
            self.main_window.confirmCard.hide()

        self.main_window.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.main_window.confirmCard.noButton.clicked.connect(clicked_no)

    def add_empty_label(self, layout, message="EMPTY"):
        empty_label = QLabel(message)
        empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
        layout.addStretch()
        layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

    def open_pet_from_appointment(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/")
        if response.status_code == 200:
            pet = response.json()
            self.main_window.show_pet_profile(pet)



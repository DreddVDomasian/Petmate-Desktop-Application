from PyQt6 import uic
from PyQt6.QtWidgets import QWidget,QCompleter,QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate
from input_styles import *
from  shadowEffects import *
from toast import Toast
from Backend.api_client import add_new_appointment
from datetime import datetime
import requests

class AddAppointmentCard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window  # keep reference
        uic.loadUi("addAppointmentCard.ui", self)

        self.walkInAppointmentListLayout = self.main_window.walkInScrollAreaWidgetContents.layout()
        self.walkInAppointmentListLayout.setSpacing(10)
        self.walkInAppointmentListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.addPopUPFrame.setGraphicsEffect(create_card_shadow())
        self.cancelAddAppointment.setGraphicsEffect(create_card_shadow())
        self.addAppointmentBtn.setGraphicsEffect(create_card_shadow())

        self.selectPatientPopUp.currentIndexChanged.connect(self.on_patient_selected)

        self.popUpDateEdit.setDate(QDate.currentDate())
        self.popUpDateEdit.mousePressEvent = lambda event: self.on_date_field_clicked(self.popUpDateEdit)

        self.setup_comboboxes()

        # submit data
        self.addAppointmentBtn.clicked.connect(self.submit_appointment_data)

        # load data
        self.load_walkInAppointments()

        if parent:
            parent.installEventFilter(self)
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
                full_name = f"{patient['firstName']} {patient['lastName']}"
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

        # basic validation
        missing = []
        if not patient_id:
            missing.append("Patient")
        if not date:
            missing.append("Date")
        if not time:
            missing.append("Time")

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
            walkInAppointment = response.json()

        else:
            walkInAppointment = []

        # 🧹 Clear existing items before adding new ones
        while self.walkInAppointmentListLayout.count():
            child = self.walkInAppointmentListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not walkInAppointment:
            empty_label = QLabel("NO RECORDS")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            self.walkInAppointmentListLayout.addStretch()
            self.walkInAppointmentListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.walkInAppointmentListLayout.addStretch()
            return

        for walkInAppointments in walkInAppointment:
            card = uic.loadUi("appointmentCard.ui")
            card.ownerName.setText(walkInAppointments["owner_full_name"])
            card.petNameApp.setText(walkInAppointments["petName"])
            date = self.main_window.format_date(walkInAppointments.get("date"))
            card.appDate.setText(date)

            time_str = walkInAppointments.get("prefTime")
            if time_str:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
                formatted_time = time_obj.strftime("%I:%M %p").lstrip("0")
                card.preferredTime.setText(formatted_time)
            else:
                card.preferredTime.setText("N/A")

            shadow = create_card_shadow()
            card.setGraphicsEffect(shadow)

            # 🔑 Make card clickable → go to pet profile
            pet_id = walkInAppointments.get("pet")
            card.mousePressEvent = lambda event, pid=pet_id: self.open_pet_from_appointment(pid)

            self.walkInAppointmentListLayout.insertWidget(0, card)

    def open_pet_from_appointment(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/")
        if response.status_code == 200:
            pet = response.json()
            self.main_window.show_pet_profile(pet)  # Reuse your existing function

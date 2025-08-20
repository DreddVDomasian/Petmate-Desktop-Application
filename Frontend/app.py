from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QWidget,QComboBox,QButtonGroup,QMessageBox,QDateEdit, QCompleter,QCalendarWidget,QToolButton,QTextEdit
from PyQt6 import uic
from PyQt6.QtCore import Qt,QDate,QPoint
import resources_rc
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QIcon, QAction,QColor
from uiLogic import UIHandler
from input_styles import *
from toast import Toast
from Backend.api_client import add_new_patient, add_new_pet, add_new_service
from confirm_card import ConfirmCard
from  appointmentPopUp import AddAppointmentCard
from functools import partial
from datetime import datetime
from shadowEffects import *
from delete import Delete
from updateFunction import Update
import requests
import webbrowser
import os
import sys



class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("Home.ui", self)
        #to delete.py
        self.deleteFunction = Delete(self)
        self.updateFunction = Update(self)
        self.setup_calendar()
        self.setup_comboboxes()
        self.setup_layouts()
        self.setup_buttons()
        self.setup_service_tab()
        self.setup_dates()
        self.setup_confirm_card()
        self.setup_add_appintmentPopUp()
        self.setup_pet_buttons()

        # Initial page and data
        self.selected_patient_id = None
        self.selected_service_id = None
        self.stackedWidget.setCurrentIndex(0)
        self.set_current_month_in_combobox()
        self.load_patients()
        self.load_scheduled_services()
        self.setup_shadow()
        self.setup_all_back_buttons()

        self.monthComboBox.currentTextChanged.connect(self.load_scheduled_services)

        #page history
        self.page_history = []  # stores (index, params)
        self.current_page_index = 0
        self.current_params = {}
        self.update_back_button_visibility()

    def setup_calendar(self):
        self.customCalendar = uic.loadUi("customCalendar.ui")
        self.customCalendar.setParent(None)
        self.customCalendar.setWindowFlags(Qt.WindowType.Popup)
        self.calendarWidget = self.customCalendar.findChild(QCalendarWidget, "calendarWidget")
        self.calendarWidget.clicked.connect(self.set_date_from_calendar)
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.setStyleSheet(QframeStyle)

    def setup_comboboxes(self):
        self.ui_handler = UIHandler(self.provinceComboBox, self.cityComboBox, self.barangayComboBox)
        self.ui_handler.load_provinces()
        combo_boxes = [self.provinceComboBox, self.cityComboBox, self.barangayComboBox]
        placeholders = ["Select Province", "Select City", "Select Barangay"]
        for cb, text in zip(combo_boxes, placeholders):
            cb.setEditable(True)
            cb.lineEdit().setReadOnly(False)
            cb.lineEdit().setPlaceholderText(text)
            cb.lineEdit().setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_layouts(self):
        # patient list layout
        self.patientListLayout = self.scrollAreaWidgetContents.layout()
        self.patientListLayout.setSpacing(10)
        self.patientListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # service list layout
        self.serviceListLayout = self.serviceHistoryScrollPage.layout()
        self.serviceListLayout.setSpacing(10)
        self.serviceListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # pet cards grid layout
        self.gridLayout_6.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gridLayout_6.addWidget(self.addPetButton, 0, 0)  # fixed add pet button
        #scheduled services
        self.scheduled_serviceLayout = self.scheduledReturnScrollPage.layout()
        self.scheduled_serviceLayout.setSpacing(10)
        self.scheduled_serviceLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setup_buttons(self):
        # page navigation
        nav = [
            (self.homeBtn, 0), (self.addPatientBtn, 1), (self.petRecordsBtn, 2),
            (self.appointmentBtn, 3), (self.schedVaxBtn, 4)
        ]
        self.navBtnGroup = QButtonGroup(self)
        self.navBtnGroup.setExclusive(True)
        for btn, index in nav:
            btn.setCheckable(True)
            self.navBtnGroup.addButton(btn)
            btn.clicked.connect(lambda _, i=index: self.navigate_to_page(i))

        self.homeBtn.setChecked(True)

        self.page_to_nav_button = {
            0: self.homeBtn,
            1: self.addPatientBtn,
            2: self.petRecordsBtn,
            3: self.appointmentBtn,
            4: self.schedVaxBtn,
            # Profile and Pet Profile pages should highlight Pet Records
            5: self.petRecordsBtn,
            8: self.petRecordsBtn
        }

        # send data
        self.confirmButton.clicked.connect(self.submit_data)
        self.petConfirmButton.clicked.connect(self.submit_pet_data)
        self.addServiceBtn.clicked.connect(self.submit_service_data)


        # add appointment
        for tb in [self.toolButton_2, self.toolButton_3]:
            tb.clicked.connect(lambda: self.open_addAppointment())
        self.addWalkinButton.mousePressEvent = lambda event: self.open_addAppointment()

        # toggle walk-in/website
        self.walkInBtn.setCheckable(True)
        self.websiteBtn.setCheckable(True)
        self.walkInBtn.clicked.connect(lambda: self.addWalkinButton.setVisible(True))
        self.websiteBtn.clicked.connect(lambda: self.addWalkinButton.setVisible(False))
        self.walkInOrWeb.setCurrentIndex(0)
        self.sourceBtnGroup = QButtonGroup(self)
        self.sourceBtnGroup.setExclusive(True)
        for btn in [self.walkInBtn, self.websiteBtn]:
            self.sourceBtnGroup.addButton(btn)
        self.walkInBtn.setChecked(True)
        self.walkInBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(0))
        self.websiteBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(1))

        self.pendingBtn.setCheckable(True)
        self.completedBtn.setCheckable(True)
        self.statusStackedWidget.setCurrentIndex(0)
        self.statusBtnGroup = QButtonGroup(self)
        for btn in [self.pendingBtn, self.completedBtn]:
            self.statusBtnGroup.addButton(btn)
        self.pendingBtn.setChecked(True)
        self.pendingBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(0))
        self.completedBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(1))



        #print btn
        self.printBtn.clicked.connect(self.handlePrintButton)

        # cancel
        self.backBtn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(0))
        self.cancelButton.clicked.connect(lambda: self.navigate_to_page(2))
        #update buttons
        self.updateBasicInfo.hide()
        self.cancelButton.hide()
        self.petUpdateButton.hide()
        self.updateServiceBtn.hide()

    def setup_service_tab(self):
        # toggle service history / add new
        self.addNewServiceBtn.setCheckable(True)
        self.serviceHistoryBtn.setCheckable(True)
        self.serviceHistoryStackedWidget.setCurrentIndex(0)
        self.sourceBtnGroup = QButtonGroup(self)
        self.sourceBtnGroup.setExclusive(True)
        for btn in [self.addNewServiceBtn, self.serviceHistoryBtn]:
            self.sourceBtnGroup.addButton(btn)
        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryBtn.clicked.connect(lambda: self.service_stackedWidget(0))
        self.addNewServiceBtn.clicked.connect(lambda: self.serviceHistoryStackedWidget.setCurrentIndex(1))

    def service_stackedWidget(self,index):
        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryStackedWidget.setCurrentIndex(index)
        self.addNewServiceBtn.setText("Add New service")
        self.clearInputs()
        self.addServiceBtn.show()
        self.updateServiceBtn.hide()

    def setup_dates(self):
        self.activeDateEdit = None
        self.dateEdit.mousePressEvent = lambda event: self.show_custom_calendar(self.dateEdit)
        self.returnDateEdit.mousePressEvent = lambda event: self.show_custom_calendar(self.returnDateEdit)
        self.dateEdit.setDate(QDate.currentDate())

        # return date checkbox
        self.returnDatePlaceholder.setReadOnly(True)
        self.returnDateEdit.hide()
        self.returnCheckBox.toggled.connect(self.toggle_return_date)

    def setup_confirm_card(self):
        self.confirmCard = ConfirmCard(self.findChild(QWidget, "MainContent"))
        self.confirmCard.hide()
        self.confirmCard.yesButton.clicked.connect(self.deleteFunction.really_delete)
        self.confirmCard.noButton.clicked.connect(self.deleteFunction.cancel_delete)
        self.patientToDelete = None

        # delete buttons sa profile patient/pet
        self.profileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_patient)
        self.petProfileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_pet)

    def clearInputs(self):
        # clear fields
        self.firstNameEdit.clear()
        self.lastNameEdit.clear()
        self.phoneNumberEdit.clear()
        self.detailedAddressEdit.clear()
        self.emailEdit.clear()
        self.emergencyNoEdit.clear()

        # Reset combo boxes to first index
        self.provinceComboBox.setCurrentIndex(0)
        self.cityComboBox.setCurrentIndex(0)
        self.barangayComboBox.setCurrentIndex(0)

        # clear service inputs
        self.serviceTypeComboBox.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.returnDateEdit.setDate(QDate.currentDate())
        self.addNoteLineEdit.clear()
        self.returnCheckBox.setChecked(False)
        self.returnDateEdit.hide()
        self.returnDatePlaceholder.show()

        #clear pet info
        self.petName.clear()
        self.petColor.clear()
        self.breed.clear()
        self.age.clear()
        self.speciesComboBox.setCurrentIndex(0)
        self.petSexComboBox.setCurrentIndex(0)

    def setup_add_appintmentPopUp(self):
        self.appointmentCard = AddAppointmentCard(
            parent=self.findChild(QWidget, "MainContent"),
            main_window=self  # pass the MainUI instance
        )
        self.appointmentCard.hide()
        self.appointmentCard.closePopUpBtn.clicked.connect(self.cancel_appointment)
        self.appointmentCard.cancelAddAppointment.clicked.connect(self.cancel_appointment)

    def cancel_appointment(self):
        self.appointmentCard.hide()

    def open_addAppointment(self):
        self.appointmentCard.load_patients_to_combobox()
        self.appointmentCard.show_card()

    def setup_pet_buttons(self):
        self.profileStackedWidget.setCurrentIndex(0)
        for btn in [self.addpetQtoolBtn, self.plusSignBtn]:
            btn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(1))
            btn.clicked.connect(lambda: self.clearInputs())
            btn.clicked.connect(lambda: self.petUpdateButton.hide())
            btn.clicked.connect(lambda: self.petConfirmButton.show())
        self.addPetButton.mousePressEvent = lambda event: self.profileStackedWidget.setCurrentIndex(1)
        self.addPetButton.mousePressEvent = lambda event: self.clearInputs()
        self.addPetButton.mousePressEvent = lambda event: self.petUpdateButton.hide()
        self.addPetButton.mousePressEvent = lambda event: self.petConfirmButton.show()



    def setup_shadow(self):
        self.ProfileCard.setGraphicsEffect(create_card_shadow())
        self.petProfileCard.setGraphicsEffect(create_card_shadow())

    def set_current_month_in_combobox(self):
        current_month = datetime.now().strftime("%B")
        index = self.monthComboBox.findText(current_month)
        if index >= 0:
            self.monthComboBox.setCurrentIndex(index)

    # check/uncheck return date
    def toggle_return_date(self, checked):
        if checked:
            self.returnDateEdit.show()
            min_date = self.dateEdit.date().addDays(1)
            today_plus_1 = QDate.currentDate().addDays(1)
            # piliin ang mas malayo sa dalawa
            default_date = min_date if min_date > today_plus_1 else today_plus_1
            self.returnDateEdit.setDate(default_date)
            self.returnDatePlaceholder.hide()
        else:
            self.returnDateEdit.hide()
            self.returnDatePlaceholder.show()

    def setup_all_back_buttons(self):
        self.all_back_buttons = [
            self.homeBackBtn,
            self.addPatientBackBtn,
            self.RecordsBackBtn,
            self.appointmentBackBtn,
            self.ReturnBackBtn,
            self.profileBackbutton,
            self.petProfileBackBtn
        ]
        for btn in self.all_back_buttons:
            btn.clicked.connect(self.go_back)

    def update_back_button_visibility(self):
        visible = bool(self.page_history)
        for btn in self.all_back_buttons:
            btn.setVisible(visible)

    def navigate_to_page(self, index, is_update=False, **kwargs):
        # Save current page & parameters
        self.page_history.append((self.current_page_index, self.current_params))


        self.current_page_index = index
        self.current_params = kwargs

        self.update_back_button_visibility()
        self.stackedWidget.setCurrentIndex(index)
        self.profileStackedWidget.setCurrentIndex(0)
        if index in self.page_to_nav_button:
            self.page_to_nav_button[index].setChecked(True)
        # Your existing Add Patient logic
        if index == 1:
            if is_update:
                self.updateBasicInfo.show()
                self.cancelButton.show()
                self.confirmButton.hide()
            else:
                self.clearInputs()
                self.updateBasicInfo.hide()
                self.cancelButton.hide()
                self.confirmButton.show()

    def go_back(self):
        if self.page_history:
            index, params = self.page_history.pop()

            self.current_page_index = index
            self.current_params = params
            self.update_back_button_visibility()
            self.stackedWidget.setCurrentIndex(index)
            if index in self.page_to_nav_button:
                self.page_to_nav_button[index].setChecked(True)

            # Load page data if needed
            if index == 5 and "owner_id" in params:
                self.load_pets_for_owner(params["owner_id"])
            elif index == 8 and "pet_id" in params:
                self.load_services_for_pet(params["pet_id"])

    def collect_and_validate_fields(self, required_fields):
        missing = []

        def apply_style(widget, error=False):
            is_combobox = isinstance(widget, QComboBox)
            if error:
                if is_combobox:
                    widget.setStyleSheet(error_combobox_style)
                else:
                    widget.setStyleSheet(error_style)
            else:
                if is_combobox:
                    widget.setStyleSheet(default_combobox_style)
                else:
                    widget.setStyleSheet(default_style)

        def is_valid_combobox_input(combo):
            text = combo.currentText()
            for i in range(combo.count()):
                if combo.itemText(i).strip().lower() == text.strip().lower():
                    return True
            return False

        data = {}
        for name, widget in required_fields.items():
            if isinstance(widget, QComboBox):
                if widget.currentIndex() == 0 or not is_valid_combobox_input(widget):
                    apply_style(widget, error=True)
                    missing.append(name)
                else:
                    apply_style(widget, error=False)
                    data[name] = widget.currentText()
            else:
                text = widget.text()
                if not text.strip():
                    apply_style(widget, error=True)
                    missing.append(name)
                else:
                    apply_style(widget, error=False)
                    data[name] = text.strip()

        return data, missing

    def submit_data(self):
        required_fields = {
            "firstName": self.firstNameEdit,
            "lastName": self.lastNameEdit,
            "phoneNumber": self.phoneNumberEdit,
            "province": self.provinceComboBox,
            "city": self.cityComboBox,
            "barangay": self.barangayComboBox,
            "detailedAddress": self.detailedAddressEdit,
            "email": self.emailEdit,
            "emergencyNumber": self.emergencyNoEdit
        }

        data, missing = self.collect_and_validate_fields(required_fields)

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # proceed to save patient
        if add_new_patient(data):
            self.navigate_to_page(2)
            self.load_patients()

            self.clearInputs()

            # Reset styles to default
            for widget in required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

            toast = Toast(self,icon_path="Icons/check.png")
            toast.show_toast()


        else:
            toast = Toast(self, "Failed to add patient!", icon_path="Icons/warning.png")
            toast.show_toast()

    def submit_pet_data(self):
        required_fields = {
            "petName": self.petName,
            "petColor": self.petColor,
            "breed": self.breed,
            "species": self.speciesComboBox,
            "age":self.age,
            "sex": self.petSexComboBox
        }

        data, missing = self.collect_and_validate_fields(required_fields)

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # Add owner_id sa data
        data["owner_id"] = self.selected_patient_id

        # Call your API: e.g. add_new_pet(data)
        if add_new_pet(data):
            self.profileStackedWidget.setCurrentIndex(0)
            self.load_pets_for_owner(self.selected_patient_id)

            self.clearInputs()
            for widget in required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

            toast = Toast(self, icon_path="Icons/check.png")
            toast.show_toast()


        else:
            toast = Toast(self, "Failed to add pet!", icon_path="Icons/warning.png")
            toast.show_toast()

    def submit_service_data(self):
        service_type = self.serviceTypeComboBox.currentText().strip()
        date = self.dateEdit.date().toString("yyyy-MM-dd")

        if self.returnCheckBox.isChecked():
            return_date = self.returnDateEdit.date().toString("yyyy-MM-dd")
        else:
            return_date = None

        notes = self.addNoteLineEdit.toPlainText().strip()

        required_fields = {
            "service_type": self.serviceTypeComboBox
        }

        # Basic validation lang para sa service type
        data, missing = self.collect_and_validate_fields(required_fields)

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        if not self.selected_patient_id or not self.selected_pet_id:
            toast = Toast(self, "No selected owner or pet!", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # Prepare data to send
        service_data = {
            "owner": self.selected_patient_id,
            "pet": self.selected_pet_id,
            "service_type": service_type,
            "date": date,
            "return_date": return_date,
            "notes": notes
        }

        if add_new_service(service_data):
            toast = Toast(self, "Service added!", icon_path="Icons/check.png")
            toast.show_toast()

            self.serviceHistoryBtn.setChecked(True)
            self.serviceHistoryStackedWidget.setCurrentIndex(0)
            self.load_services_for_pet(self.selected_pet_id)
            self.load_scheduled_services()
            # Clear fields or reset
            self.clearInputs()

        else:
            toast = Toast(self, "Failed to add service!", icon_path="Icons/warning.png")
            toast.show_toast()

    def cancelBtn(self):
        self.profileStackedWidget.setCurrentIndex(0)
        self.petName.clear()
        self.petColor.clear()
        self.breed.clear()
        self.age.clear()
        self.speciesComboBox.setCurrentIndex(0)
        self.petSexComboBox.setCurrentIndex(0)

    def load_patients(self):
        response = requests.get("http://127.0.0.1:8000/api/patients/")
        if response.status_code == 200:
            patients = response.json()

        else:
            patients = []

        # 🧹 Clear existing items before adding new ones
        while self.patientListLayout.count():
            child = self.patientListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not patients:
            empty_label = QLabel("NO RECORDS")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            self.patientListLayout.addStretch()
            self.patientListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.patientListLayout.addStretch()
            return

        for patient in patients:
            card = uic.loadUi("PatientCard.ui")
            card.nameLabel.setText(f"{patient['firstName']} {patient['lastName']}")
            card.emailLabel.setText(patient['email'])

            # Connect delete button
            card.deleteButton.clicked.connect(lambda _, p_id=patient['id']: self.deleteFunction.set_delete_target("patient", p_id))
            card.editBtn.clicked.connect(lambda _, p_id=patient['id']: self.updateFunction.update_patient_info(p_id))
            # Connect the card click to open profile
            def make_handler(patient, self):
                def handler(event):
                    self.show_patient_profile(patient)

                return handler

            card.mousePressEvent = make_handler(patient, self)

            card.setGraphicsEffect(create_card_shadow())
            self.patientListLayout.insertWidget(0, card)

    def load_pets_for_owner(self, owner_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/?owner_id={owner_id}")
        pets = response.json() if response.status_code == 200 else []

        # clear pet cards lang, wag galawin addPetButton
        while self.gridLayout_6.count() > 1:
            item = self.gridLayout_6.takeAt(1)  # skip first item (addPetButton)
            if item and item.widget():
                item.widget().deleteLater()

        container_width = self.scrollAreaWidgetContents.width()
        card_width = 401
        spacing = 10
        max_cols = max(1, (container_width + spacing) // (card_width + spacing))

        row = 0
        col = 1  # start at col=1, col=0 is your addPetButton

        for pet in pets:
            pet_card = uic.loadUi("petRecordCard.ui")
            pet_card.petNameCard.setText(pet["petName"].upper())

            #Dynamic icon by species
            species = pet.get("species", "").lower()
            if species == "dog":
                icon_path = "Icons/dog.png"
            elif species == "cat":
                icon_path = "Icons/catIcon.png"
            else:
                icon_path = "Icons/otherSpecies.png"

            pet_card.petCardIcon.setPixmap(QPixmap(icon_path))
            pet_card.petCardIcon.setScaledContents(True)

            pet_card.mousePressEvent = lambda event, p=pet: self.show_pet_profile(p)
            pet_card.setGraphicsEffect(create_card_shadow())

            self.gridLayout_6.addWidget(pet_card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def load_services_for_pet(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/services/?pet_id={pet_id}")
        services = response.json() if response.status_code == 200 else []

        header = self.findChild(QWidget, "serviceTableHeader")


        # Clear existing service cards
        while self.serviceListLayout.count():
            item = self.serviceListLayout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        if not services:
            header.setVisible(False)
            empty_label = QLabel("EMPTY")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            self.serviceListLayout.addStretch()
            self.serviceListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.serviceListLayout.addStretch()
            return

        else:
            header.setVisible(True)

        for service in services:
            service_card = uic.loadUi("serviceCard.ui")

            # Always cast to str to avoid None crashing
            service_type = str(service.get("service_type", "N/A"))
            done_on = self.format_date(service.get("date")) or "N/A"
            return_date = self.format_date(service.get("return_date"))
            notes = str(service.get("notes"))
            # Fill data
            service_card.findChild(QLabel, "serviceLabel").setText(service_type)
            service_card.findChild(QLabel, "doneOnLabel").setText(done_on)
            return_label = service_card.findChild(QLabel, "returnDateLabel")
            return_label.setText(f"{return_date}" if return_date else "       None")

            note_label = service_card.findChild(QTextEdit, "noteLabel")
            note_label.setPlainText(f"{notes}" if notes else "No Notes")

            upper_frame = service_card.findChild(QWidget, "upperFrame")
            lower_frame = service_card.findChild(QWidget, "lowerFrame")
            lower_frame.setVisible(False)

            # Find buttons safely
            open_btn = service_card.findChild(QToolButton, "OpenNoteBtn")
            close_btn = service_card.findChild(QToolButton, "closeNotesBtn")

            service_card.serviceDeleteBtn.clicked.connect(lambda _, service_id=service['id']: self.deleteFunction.set_delete_target("service", service_id))
            service_card.updateServiceCardBtn.clicked.connect(lambda _, service_id=service["id"]: self.updateFunction.update_service_info(service_id))
            # Connect buttons safely
            if open_btn and close_btn and lower_frame:
                open_btn.setVisible(True)
                close_btn.setVisible(False)

                open_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, True,upper_frame))
                close_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, False,upper_frame))

            self.serviceListLayout.addWidget(service_card)

    def load_scheduled_services(self):
        response = requests.get("http://127.0.0.1:8000/api/scheduled-services/")
        if response.status_code == 200:
            scheduled_services = response.json()
        else:
            scheduled_services = []

        # get selected month from combobox
        selected_month = self.monthComboBox.currentText()  # e.g., 'August'

        # filter by return_date month
        filtered_services = []
        for service in scheduled_services:
            return_date_str = service.get("return_date")  # e.g., '2025-08-05'
            if return_date_str:
                try:
                    date_obj = datetime.strptime(return_date_str, "%Y-%m-%d")
                    month_name = date_obj.strftime("%B")  # 'August'
                    if month_name == selected_month:
                        filtered_services.append(service)
                except ValueError:
                    pass  # skip invalid date

        # clear old cards
        while self.scheduled_serviceLayout.count():
            child = self.scheduled_serviceLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # show empty message if no records
        if not filtered_services:
            empty_label = QLabel("EMPTY")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            self.scheduled_serviceLayout.addStretch()
            self.scheduled_serviceLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.scheduled_serviceLayout.addStretch()
            return

        # create cards
        for service in filtered_services:
            card = uic.loadUi("schedCard.ui")
            card.ReturnNameLabel.setText(service['owner_full_name'])
            card.ReturnServiceLabel.setText(service['service_type'])
            return_date = self.format_date(service.get("return_date"))
            card.ReturnDateCardLabel.setText(return_date)
            card.setGraphicsEffect(create_card_shadow())

            self.scheduled_serviceLayout.insertWidget(0,card)

    def format_date(self, raw):
        if raw:
            try:
                dt = datetime.strptime(raw, "%Y-%m-%d")
                return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
            except Exception:
                return raw
        return None

    def toggle_note(self, frame, open_btn, close_btn, show, upper_frame=None):
        frame.setVisible(show)
        open_btn.setVisible(not show)
        close_btn.setVisible(show)
        if upper_frame:
            if show:
                # remove bottom radius para magmukhang dikit sa lower_frame
                upper_frame.setStyleSheet(upper_Frame_Noborrad)
            else:
                # ibalik original radius
                upper_frame.setStyleSheet(upper_Frame_borrad)

    def show_patient_profile(self, patient):
        full_name = f"{patient['firstName']} {patient['lastName']}"
        self.profileNameLabel.setText(full_name)
        self.profileEmailLabel.setText(patient['email'])

        # Combine address parts
        address = f"{patient['barangay']}, {patient['city']}, {patient['province']}"
        contactNumbers = f"{patient['phoneNumber']}  / {patient['emergencyNumber']}"
        self.addressLabel.setText(address)
        self.detailedAddressLabel.setText(patient['detailedAddress'])
        self.phoneLabel.setText(contactNumbers)

        self.selected_patient_id = patient['id']
        self.profileEditBtn.clicked.connect(lambda: self.updateFunction.update_patient_info(self.selected_patient_id))
        self.load_pets_for_owner(self.selected_patient_id)
        # Navigate to the profile page
        self.navigate_to_page(5, owner_id=patient['id'])

    def show_pet_profile(self, pet):
        # Fill labels with pet data
        setPetName = f"NAME: {pet['petName']} "
        self.petProfileNameLabel.setText(setPetName.upper())
        setPetColor = f"COLOR: {pet['petColor']} "
        self.petColorLabel.setText(setPetColor.upper())
        setPetBreed = f"BREED: {pet['breed']} "
        self.breedLabel.setText(setPetBreed.upper())
        setPetSpecies = f"SPECIES: {pet['species']} "
        self.speciesLabel.setText(setPetSpecies.upper())
        setPetSex = f"SEX: {pet['sex']} "
        self.petSexLabel.setText(setPetSex.upper())
        age = f"AGE: {pet['age']} "
        self.petAgeLabel.setText(age)

        species = pet.get("species", "").lower()
        if species == "dog":
            icon_path = "Icons/dog.png"
        elif species == "cat":
            icon_path = "Icons/catIcon.png"
        else:
            icon_path = "Icons/otherSpecies.png"

        self.petProfileIcon.setPixmap(QPixmap(icon_path))


        # Keep track of which pet is selected
        self.selected_pet_id = pet["id"]
        self.petProfileEditBtn.clicked.connect(lambda: self.updateFunction.update_pet_info(self.selected_pet_id))
        # Navigate to pet profile page (adjust index if needed)
        self.navigate_to_page(8, pet_id=pet["id"])
        self.load_services_for_pet(pet["id"])

    def show_custom_calendar(self, dateEdit):
        self.activeDateEdit = dateEdit
        pos = dateEdit.mapToGlobal(QPoint(0, dateEdit.height()))
        self.customCalendar.move(pos)

        # special condition for returnDateEdit
        if dateEdit == self.returnDateEdit:
            min_date = self.dateEdit.date().addDays(1)
            self.calendarWidget.setMinimumDate(min_date)
        else:
            # reset to today or earliest allowed
            self.calendarWidget.setMinimumDate(QDate(1752, 9, 14))  # earliest date supported
        # optional: also reset max date if you want
        # self.calendarWidget.setMaximumDate(QDate(9999, 12, 31))

        current_date = dateEdit.date()
        self.calendarWidget.setSelectedDate(current_date)

        self.customCalendar.show()
        QApplication.processEvents()
        self.calendarWidget.repaint()

    def set_date_from_calendar(self, date):
        if self.activeDateEdit:
            self.activeDateEdit.setDate(date)
        self.customCalendar.hide()

    def handlePrintButton(self):
        if self.selected_patient_id and self.selected_pet_id:
            print_url = f"http://127.0.0.1:8000/api/print/{self.selected_patient_id}/{self.selected_pet_id}/"
            webbrowser.open(print_url)
        else:
            QMessageBox.warning(self, "Missing Info", "Please select a patient and a pet first.")


if __name__ == "__main__":
    app = QApplication(sys.argv)


    font_path = os.path.join(os.path.dirname(__file__), "font/Montserrat/Montserrat-VariableFont_wght.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    ui = MainUI()
    ui.show()
    app.exec()

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QWidget,QComboBox,QButtonGroup,QMessageBox,QDateEdit
from PyQt6 import uic
from PyQt6.QtCore import Qt,QDate
import resources_rc
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QIcon, QAction,QColor
from uiLogic import UIHandler
from input_styles import *
from toast import Toast
from Backend.api_client import add_new_patient, add_new_pet
from confirm_card import ConfirmCard
import requests
import os
import sys



class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("Home.ui", self)

        self.ui_handler = UIHandler(self.provinceComboBox, self.cityComboBox, self.barangayComboBox)
        self.ui_handler.load_provinces()

        # Set layout before loading patients
        self.patientListLayout = self.scrollAreaWidgetContents.layout()
        self.patientListLayout.setSpacing(10)  # spacing between cards
        self.patientListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Load patients now
        self.load_patients()

        #Changing main Page
        self.stackedWidget.setCurrentIndex(0)
        self.homeBtn.clicked.connect(lambda: self.navigate_to_page(0))
        self.addPatientBtn.clicked.connect(lambda: self.navigate_to_page(1))
        self.petRecordsBtn.clicked.connect(lambda: self.navigate_to_page(2))
        self.appointmentBtn.clicked.connect(lambda: self.navigate_to_page(3))
        self.schedVaxBtn.clicked.connect(lambda: self.navigate_to_page(4))

        # send owner data to db
        self.confirmButton.clicked.connect(self.submit_data)
        # send pet data to db
        self.petConfirmButton.clicked.connect(self.submit_pet_data)

        #add Appointment Button
        self.toolButton_2.clicked.connect(lambda: self.navigate_to_page(6))
        self.toolButton_3.clicked.connect(lambda: self.navigate_to_page(6))
        self.addWalkinButton.mousePressEvent = lambda event: self.navigate_to_page(6)

        # Make buttons checkable
        self.walkInBtn.setCheckable(True)
        self.websiteBtn.setCheckable(True)
        self.walkInBtn.clicked.connect(lambda: self.addWalkinButton.setVisible(True))
        self.websiteBtn.clicked.connect(lambda: self.addWalkinButton.setVisible(False))

        # Create a QButtonGroup to keep only one active
        self.sourceBtnGroup = QButtonGroup(self)
        self.sourceBtnGroup.setExclusive(True)
        self.sourceBtnGroup.addButton(self.walkInBtn)
        self.sourceBtnGroup.addButton(self.websiteBtn)
        self.walkInBtn.setChecked(True)

        #changing page walkIn/website appointment
        self.walkInOrWeb.setCurrentIndex(0)
        self.walkInBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(0))
        self.websiteBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(1))


        #backbutton in profile page
        self.profileBackbutton.clicked.connect(lambda: self.navigate_to_page(2))
        self.profileBackbutton.clicked.connect(lambda: self.cancelBtn())
        self.selected_patient_id = None

        #backbutton in pet profile page
        self.petProfileBackBtn.clicked.connect(lambda: self.load_pets_for_owner(self.selected_patient_id))
        self.petProfileBackBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

        #service history/add new history tab
        self.addNewServiceBtn.setCheckable(True)
        self.serviceHistoryBtn.setCheckable(True)
        self.serviceHistoryStackedWidget.setCurrentIndex(0)
        self.sourceBtnGroup.addButton(self.addNewServiceBtn)
        self.sourceBtnGroup.addButton(self.serviceHistoryBtn)
        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryBtn.clicked.connect(lambda: self.serviceHistoryStackedWidget.setCurrentIndex(0))
        self.addNewServiceBtn.clicked.connect(lambda: self.serviceHistoryStackedWidget.setCurrentIndex(1))
        # Set to current date
        self.dateEdit.setDate(QDate.currentDate())
        #return date optional
        # initially disabled (user must check to enable)
        self.returnDateEdit.setEnabled(False)

        # optional: visually empty if date == minimum
        self.returnDateEdit.setMinimumDate(QDate(2000, 1, 1))
        self.returnDateEdit.setSpecialValueText("")  # empty text when min date
        self.returnDateEdit.setDate(self.returnDateEdit.minimumDate())

        # connect checkbox
        self.returnCheckBox.toggled.connect(self.toggle_return_date)

        #for delete button in profile page
        self.profileDeleteBtn.clicked.connect(self.delete_selected_patient)

        # Create confirm card instance para sa delete
        self.confirmCard = ConfirmCard(self)
        self.confirmCard.hide()  # hide initially

        # Add sa layout o manual add para overlay
        self.confirmCard = ConfirmCard(self.findChild(QWidget, "MainContent"))
        self.confirmCard.hide()

        # Connect buttons
        self.confirmCard.yesButton.clicked.connect(self.really_delete_patient)
        self.confirmCard.noButton.clicked.connect(self.cancel_delete)

        self.patientToDelete = None

        #add pet button navigation
        self.profileStackedWidget.setCurrentIndex(0)
        self.addpetQtoolBtn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(1))
        self.plusSignBtn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(1))
        self.addPetButton.mousePressEvent = lambda event: self.profileStackedWidget.setCurrentIndex(1)


        # cancelBtn
        self.backBtn.clicked.connect(lambda: self.cancelBtn())

        # setup grid layout para sa pet cards
        self.gridLayout_6.setAlignment(Qt.AlignmentFlag.AlignTop)


        # add the addPetButton as first item, fixed place
        self.gridLayout_6.addWidget(self.addPetButton, 0, 0)

    def toggle_return_date(self, checked):
        self.returnDateEdit.setEnabled(checked)
        if not checked:
            # reset to look empty
            self.returnDateEdit.setDate(self.returnDateEdit.minimumDate())

    def navigate_to_page(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def collect_and_validate_fields(self, required_fields):
        missing = []

        def apply_style(widget, error=False):
            is_combobox = "QComboBox" in widget.__class__.__name__
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

        data = {}
        for name, widget in required_fields.items():
            is_combobox = "QComboBox" in widget.__class__.__name__
            if is_combobox:
                if widget.currentIndex() == 0:
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
        data["owner"] = self.selected_patient_id

        # Call your API: e.g. add_new_pet(data)
        if add_new_pet(data):
            self.profileStackedWidget.setCurrentIndex(0)
            self.load_pets_for_owner(self.selected_patient_id)

            self.petName.clear()
            self.petColor.clear()
            self.breed.clear()
            self.age.clear()


            self.speciesComboBox.setCurrentIndex(0)
            self.petSexComboBox.setCurrentIndex(0)

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

        for patient in patients:
            card = uic.loadUi("PatientCard.ui")
            card.nameLabel.setText(f"{patient['firstName']} {patient['lastName']}")
            card.emailLabel.setText(patient['email'])

            # Connect delete button
            card.deleteButton.clicked.connect(lambda _, p_id=patient['id']: self.confirm_and_delete(p_id))

            # Connect the card click to open profile
            card.mousePressEvent = lambda event, p=patient: self.show_patient_profile(p)

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
            pet_card.petNameCard.setText(pet["petName"])

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

            self.gridLayout_6.addWidget(pet_card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1


    def delete_patient(self, patient_id):
        response = requests.delete(f"http://127.0.0.1:8000/api/patients/{patient_id}/")
        if response.status_code == 204:
            toast = Toast(self, "Deleted successfully!", icon_path="Icons/check.png")
            toast.show_toast()
            self.load_patients()
        else:
            toast = Toast(self, "Failed to delete!", icon_path="Icons/warning.png")
            toast.show_toast()

    def delete_selected_patient(self):
        if self.selected_patient_id is None:
            QMessageBox.warning(self, "Error", "No patient selected.")
            return

        self.patientToDelete = self.selected_patient_id
        self.confirmCard.show()

    def confirm_and_delete(self, patient_id):
        self.patientToDelete = patient_id
        self.confirmCard.show_card()

    def really_delete_patient(self):
        if self.patientToDelete is not None:
            self.delete_patient(self.patientToDelete)
            self.patientToDelete = None
            self.stackedWidget.setCurrentIndex(2)
        self.confirmCard.hide()

    def cancel_delete(self):
        self.patientToDelete = None
        self.confirmCard.hide()

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

        self.load_pets_for_owner(self.selected_patient_id)
        # Navigate to the profile page
        self.stackedWidget.setCurrentIndex(5)

    def show_pet_profile(self, pet):
        # Fill labels with pet data
        self.petProfileNameLabel.setText(pet["petName"].upper())
        self.petColorLabel.setText(pet["petColor"].upper())
        self.breedLabel.setText(pet["breed"].upper())
        self.speciesLabel.setText(pet["species"].upper())
        self.petSexLabel.setText(pet["sex"].upper())

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

        # Navigate to pet profile page (adjust index if needed)
        self.stackedWidget.setCurrentIndex(8)


if __name__ == "__main__":
    app = QApplication(sys.argv)


    font_path = os.path.join(os.path.dirname(__file__), "font/Montserrat/Montserrat-VariableFont_wght.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    ui = MainUI()
    ui.show()
    app.exec()

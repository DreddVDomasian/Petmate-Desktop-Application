import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox,QComboBox
from PyQt6.QtCore import Qt, QDate, QTimer


class Update:
    def __init__(self, ui_context):
        self.ui = ui_context  # Reference to main UI
        self.ui.updateBasicInfo.clicked.connect(self.update_patient_to_api)
        self.ui.petUpdateButton.clicked.connect(self.update_pet_to_api)
        self.ui.updateServiceBtn.clicked.connect(self.update_service_to_api)
    # UPDATE OWNER INFO

    def set_combobox_value(self, combo: QComboBox, value: str):
        if not isinstance(value, str):
            value = ""
        index = combo.findText(value.strip(), Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)
        else:
            combo.setCurrentIndex(0)

    def populate_patient_form(self, patient):
        self.ui.firstNameEdit.setText(patient.get("firstName"))
        self.ui.lastNameEdit.setText(patient.get("lastName"))
        self.ui.middleNameEdit.setText(patient.get("middleName") or None)
        self.ui.phoneNumberEdit.setText(patient.get("phoneNumber"))
        self.set_combobox_value(self.ui.provinceComboBox, patient.get("province"))
        self.set_combobox_value(self.ui.cityComboBox, patient.get("city"))
        self.set_combobox_value(self.ui.barangayComboBox, patient.get("barangay"))
        self.ui.detailedAddressEdit.setText(patient.get("detailedAddress"))
        self.ui.emailEdit.setText(patient.get("email"))
        self.ui.emergencyNoEdit.setText(patient.get("emergencyNumber"))
        self.ui.selected_patient_id = patient.get("id")

    def update_patient_info(self, owner_id):
        response = requests.get(f"http://127.0.0.1:8000/api/patients/{owner_id}/")
        if response.status_code == 200:
            patient = response.json()
            self.populate_patient_form(patient)
            self.ui.navigate_to_page(1, is_update=True)
        else:
            Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast()

    def update_patient_to_api(self):
        patient_id = getattr(self.ui, "selected_patient_id", None)
        if not patient_id:
            Toast(self.ui, "No patient selected!", icon_path="Icons/warning.png").show_toast()
            return

        # Collect data from widgets safely
        data = {
            "firstName": self.ui.firstNameEdit.text().strip(),
            "lastName": self.ui.lastNameEdit.text().strip(),
            "middleName": self.ui.middleNameEdit.text().strip() or None,  # send None if empty
            "email": self.ui.emailEdit.text().strip() or None,
            "phoneNumber": self.ui.phoneNumberEdit.text().strip(),
            "province": self.ui.provinceComboBox.currentText(),
            "city": self.ui.cityComboBox.currentText(),
            "barangay": self.ui.barangayComboBox.currentText(),
            "detailedAddress": self.ui.detailedAddressEdit.text().strip() or None,
            "emergencyNumber": self.ui.emergencyNoEdit.text().strip() or None
        }

        # Validate combo boxes
        for combo, name in [
            (self.ui.provinceComboBox, "province"),
            (self.ui.cityComboBox, "city"),
            (self.ui.barangayComboBox, "barangay")
        ]:
            if combo.currentIndex() == 0 or combo.currentText().strip() == "":
                Toast(self.ui, f"Invalid {name} selected!", icon_path="Icons/warning.png").show_toast()
                return

        # Birthday / stored_age logic
        sentinel = QDate(1900, 1, 1)
        bday_qdate = self.ui.Bday.date()
        if bday_qdate.isValid() and bday_qdate != sentinel:
            data["birthDay"] = bday_qdate.toString("yyyy-MM-dd")
            data["stored_age"] = None
        else:
            data["birthDay"] = None
            data["stored_age"] = self.ui.age.text().strip() or None

        url = f"http://127.0.0.1:8000/api/patients/{patient_id}/"

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                # Defer UI updates to prevent crash
                def post_update_ui():
                    self.ui.load_patients()
                    self.ui.clearInputs()
                    self.ui.navigate_to_page(2)
                    Toast(self.ui, "Patient updated successfully!", icon_path="Icons/check.png").show_toast()

                QTimer.singleShot(0, post_update_ui)
            else:
                Toast(self.ui, f"Update failed! {response.text}", icon_path="Icons/warning.png").show_toast()
        except Exception as e:
            Toast(self.ui, f"Unexpected error: {str(e)}", icon_path="Icons/warning.png").show_toast()

    # UPDATE PET INFO
    def populate_pet_form(self, pet):
        self.ui.petName.setText(pet["petName"])
        self.ui.petColor.setText(pet["petColor"])
        self.ui.breed.setText(pet["breed"])
        self.ui.speciesComboBox.setCurrentText(pet["species"])
        self.ui.age.setText(str(pet["age"]))
        self.ui.petSexComboBox.setCurrentText(pet["sex"])
        self.ui.selected_pet_id = pet["id"]
        date_str = pet.get("birthDate")
        if date_str:
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.ui.Bday.setDate(qdate)

    def update_pet_info(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/")
        if response.status_code == 200:
            pet = response.json()
            self.populate_pet_form(pet)
            self.ui.show_patient_profile(pet["owner"])
            self.ui.profileStackedWidget.setCurrentIndex(1)  # Show the pet form
            self.ui.petConfirmButton.hide()
            self.ui.petUpdateButton.show()
        else:
            Toast(self.ui, "Failed to load pet!", icon_path="Icons/warning.png").show_toast()

    def update_pet_to_api(self):
        pet_id = self.ui.selected_pet_id
        if not pet_id:
            return

        data = {
            "petName": self.ui.petName.text(),
            "petColor": self.ui.petColor.text(),
            "breed": self.ui.breed.text(),
            "species": self.ui.speciesComboBox.currentText(),
            "sex": self.ui.petSexComboBox.currentText(),
            "owner_id": self.ui.selected_patient_id,
            "remarks": self.ui.petRemarks.text().strip() or None
        }

        # --- Birthday / stored_age logic ---
        sentinel = QDate(1900, 1, 1)
        bday_qdate = self.ui.Bday.date()
        has_birthday = (bday_qdate is not None) and (bday_qdate != sentinel)

        if has_birthday:
            data["birthDay"] = bday_qdate.toString("yyyy-MM-dd")
            data["stored_age"] = None
        else:
            data["birthDay"] = None
            typed_age = self.ui.age.text().strip()
            data["stored_age"] = typed_age if typed_age else None

        url = f"http://127.0.0.1:8000/api/pets/{pet_id}/"
        response = requests.put(url, json=data)

        if response.status_code == 200:
            Toast(self.ui, "Pet updated successfully!", icon_path="Icons/check.png").show_toast()

            # 🔄 Fetch updated pet so age recalculates
            refreshed = requests.get(url)
            if refreshed.status_code == 200:
                pet = refreshed.json()
                self.ui.show_pet_profile(pet)  # refresh profile page with new computed age

            self.ui.load_pets_for_owner(self.ui.selected_patient_id)
            self.ui.profileStackedWidget.setCurrentIndex(0)
        else:
            Toast(self.ui, "Failed to update pet!", icon_path="Icons/warning.png").show_toast()

    # UDPATE SERVICE INFO
    def populate_service_form(self, service):
        # Service type
        self.ui.serviceTypeComboBox.setCurrentText(service.get("service_type", ""))
        # Date (required)
        date_str = service.get("date")
        if date_str:
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.ui.dateEdit.setDate(qdate)
        # Return date (optional)
        return_date_str = service.get("return_date")
        if return_date_str:
            qdate = QDate.fromString(return_date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.ui.returnDateEdit.setDate(qdate)
            self.ui.returnCheckBox.setChecked(True)
        else:
            self.ui.returnCheckBox.setChecked(False)
        # Notes
        self.ui.addNoteLineEdit.setPlainText(service.get("notes", ""))

    def update_service_info(self, service_id):
        self.ui.selected_service_id = service_id
        response = requests.get(f"http://127.0.0.1:8000/api/services/{service_id}/")
        if response.status_code == 200:
            service = response.json()
            self.populate_service_form(service)
            self.ui.addServiceBtn.hide()
            self.ui.updateServiceBtn.show()
            self.ui.addNewServiceBtn.setChecked(True)
            self.ui.addNewServiceBtn.setText("Update service")
            self.ui.dateEdit.setEnabled(False)
            self.ui.serviceHistoryStackedWidget.setCurrentIndex(1)
        else:
            Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast()

    def update_service_to_api(self):
        service_id = self.ui.selected_service_id  # Make sure this is set when clicking "edit"
        if not service_id:
            Toast(self.ui, "No service selected for update!", icon_path="Icons/warning.png").show_toast()
            return

        # Build data payload
        data = {

            "service_type": self.ui.serviceTypeComboBox.currentText(),
            "date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "notes": self.ui.addNoteLineEdit.toPlainText(),
            "owner": self.ui.selected_patient_id,  # set when showing profile
            "pet": self.ui.selected_pet_id
        }

        # Handle optional return date
        if self.ui.returnCheckBox.isChecked():
            data["return_date"] = self.ui.returnDateEdit.date().toString("yyyy-MM-dd")
        else:
            data["return_date"] = None  # or skip this key entirely depending on API

        # Send PUT request
        url = f"http://127.0.0.1:8000/api/services/{service_id}/"
        response = requests.put(url, json=data)

        # Handle response
        if response.status_code == 200:
            Toast(self.ui, "Service updated successfully!", icon_path="Icons/check.png").show_toast()
            self.ui.load_services_for_pet(self.ui.selected_pet_id)  # refresh list
            self.ui.service_stackedWidget(0) # go back to history
            self.ui.updateServiceBtn.hide()
            self.ui.addServiceBtn.show()
        else:
            Toast(self.ui, "Failed to update service!", icon_path="Icons/warning.png").show_toast()


def is_valid_combobox_input(combo: QComboBox) -> bool:
    text = combo.currentText()
    for i in range(combo.count()):
        if combo.itemText(i).strip().lower() == text.strip().lower():
            return True
    return False


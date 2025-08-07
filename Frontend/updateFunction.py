import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox,QComboBox


class Update:
    def __init__(self, ui_context):
        self.ui = ui_context  # Reference to main UI
        self.ui.updateBasicInfo.clicked.connect(self.update_patient_to_api)


    def populate_patient_form(self, patient):
        self.ui.firstNameEdit.setText(patient["firstName"])
        self.ui.lastNameEdit.setText(patient["lastName"])
        self.ui.phoneNumberEdit.setText(patient["phoneNumber"])
        self.ui.provinceComboBox.setCurrentText(patient["province"])
        self.ui.cityComboBox.setCurrentText(patient["city"])
        self.ui.barangayComboBox.setCurrentText(patient["barangay"])
        self.ui.detailedAddressEdit.setText(patient["detailedAddress"])
        self.ui.emailEdit.setText(patient["email"])
        self.ui.emergencyNoEdit.setText(patient["emergencyNumber"])
        self.ui.selected_patient_id = patient["id"]

    def update_patient_info(self, owner_id):
        response = requests.get(f"http://127.0.0.1:8000/api/patients/{owner_id}/")
        if response.status_code == 200:
            patient = response.json()
            self.populate_patient_form(patient)
            self.ui.navigate_to_page(1, is_update=True)
        else:
            Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast()

    def update_patient_to_api(self):
        patient_id = self.ui.selected_patient_id
        if not patient_id:
            return

        data = {
            "firstName": self.ui.firstNameEdit.text(),
            "lastName": self.ui.lastNameEdit.text(),
            "email": self.ui.emailEdit.text(),
            "phoneNumber": self.ui.phoneNumberEdit.text(),
            "province": self.ui.provinceComboBox.currentText(),
            "city": self.ui.cityComboBox.currentText(),
            "barangay": self.ui.barangayComboBox.currentText(),
            "detailedAddress": self.ui.detailedAddressEdit.text(),
            "emergencyNumber": self.ui.emergencyNoEdit.text()
        }

        province = self.ui.provinceComboBox
        city = self.ui.cityComboBox
        barangay = self.ui.barangayComboBox

        if not is_valid_combobox_input(province):
            Toast(self.ui, "Invalid province selected!", icon_path="Icons/warning.png").show_toast()
            return

        if not is_valid_combobox_input(city):
            Toast(self.ui, "Invalid city selected!", icon_path="Icons/warning.png").show_toast()
            return

        if not is_valid_combobox_input(barangay):
            Toast(self.ui, "Invalid barangay selected!", icon_path="Icons/warning.png").show_toast()
            return

        url = f"http://127.0.0.1:8000/api/patients/{patient_id}/"
        response = requests.put(url, json=data)


        if response.status_code == 200:
            Toast(self.ui, "Patient updated successfully!", icon_path="Icons/check.png").show_toast()
            self.ui.load_patients()
            self.ui.navigate_to_page(2)
        else:
            Toast(self.ui, "Update failed!", icon_path="Icons/warning.png").show_toast()

def is_valid_combobox_input(combo: QComboBox) -> bool:
    text = combo.currentText()
    for i in range(combo.count()):
        if combo.itemText(i).strip().lower() == text.strip().lower():
            return True
    return False
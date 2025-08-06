import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox

class Delete:
    def __init__(self, ui_context):
        self.ui = ui_context  # ← this is your main window or controller
        self.patientToDelete = None

    def delete_patient(self, patient_id):
        response = requests.delete(f"http://127.0.0.1:8000/api/patients/{patient_id}/")
        if response.status_code == 204:
            toast = Toast(self.ui, "Deleted successfully!", icon_path="Icons/check.png")
            toast.show_toast()
            self.ui.load_patients()
        else:
            toast = Toast(self.ui, "Failed to delete!", icon_path="Icons/warning.png")
            toast.show_toast()

    def delete_selected_patient(self):
        if self.ui.selected_patient_id is None:
            QMessageBox.warning(self.ui, "Error", "No patient selected.")
            return

        self.patientToDelete = self.ui.selected_patient_id
        self.ui.confirmCard.show_card()

    def confirm_and_delete(self, patient_id):
        self.patientToDelete = patient_id
        self.ui.confirmCard.show_card()

    def really_delete_patient(self):
        if self.patientToDelete is not None:
            self.delete_patient(self.patientToDelete)
            self.patientToDelete = None
            self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.confirmCard.hide()

    def cancel_delete(self):
        self.patientToDelete = None
        self.ui.confirmCard.hide()

import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox


class Delete:
    def __init__(self, ui_context):
        self.ui = ui_context  # Reference to main UI
        self.delete_type = None  # "patient", "pet", "service"
        self.delete_id = None

    def set_delete_target(self, target_type, target_id):
        self.delete_type = target_type  # "patient", "pet", "service"
        self.delete_id = target_id
        self.ui.confirmCard.show_card()

    def delete_selected_patient(self):
        if self.ui.selected_patient_id is None:
            QMessageBox.warning(self.ui, "Error", "No patient selected.")
            return
        self.set_delete_target("patient", self.ui.selected_patient_id)

    def delete_selected_pet(self):
        if self.ui.selected_pet_id is None:
            QMessageBox.warning(self.ui, "Error", "No pet selected.")
            return
        self.set_delete_target("pet", self.ui.selected_pet_id)

    def delete_selected_service(self):
        if self.ui.selected_service_id is None:
            QMessageBox.warning(self.ui, "Error", "No service selected.")
            return
        self.set_delete_target("service", self.ui.selected_service_id)

    def really_delete(self):
        if not self.delete_type or not self.delete_id:
            return

        url_map = {
            "patient": f"http://127.0.0.1:8000/api/patients/{self.delete_id}/",
            "pet": f"http://127.0.0.1:8000/api/pets/{self.delete_id}/",
            "service": f"http://127.0.0.1:8000/api/services/{self.delete_id}/",
        }

        url = url_map.get(self.delete_type)
        if not url:
            return

        response = requests.delete(url)
        if response.status_code == 204:
            Toast(self.ui, f"{self.delete_type.capitalize()} deleted successfully!",
                  icon_path="Icons/check.png").show_toast()

            if self.delete_type == "patient":
                self.ui.load_patients(self.ui.patient_currentPage,search_term=None)
                self.ui.load_scheduled_services()
                self.ui.appointmentCard.load_walkInAppointments()
                self.ui.stackedWidget.setCurrentIndex(2)
            elif self.delete_type == "pet":
                self.ui.load_scheduled_services()
                self.ui.appointmentCard.load_walkInAppointments()
                self.ui.load_pets_for_owner(self.ui.selected_patient_id)  # use existing patient id
                self.ui.stackedWidget.setCurrentIndex(5)
            elif self.delete_type == "service":
                self.ui.load_scheduled_services()
                self.ui.load_services_for_pet(self.ui.selected_pet_id)


        else:
            Toast(self.ui, f"Failed to delete {self.delete_type}.", icon_path="Icons/warning.png").show_toast()

        self.delete_type = None
        self.delete_id = None
        self.ui.confirmCard.hide()

    def cancel_delete(self):
        self.delete_id = None
        self.delete_type = None
        self.ui.confirmCard.reject_dialog()


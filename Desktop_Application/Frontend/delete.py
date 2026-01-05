import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox
from config_loader import API_BASE_URL
from PyQt6.QtCore import QTimer


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
            "patient": f"{API_BASE_URL}/api/patients/{self.delete_id}/",
            "pet": f"{API_BASE_URL}/api/pets/{self.delete_id}/",
            "service": f"{API_BASE_URL}/api/services/{self.delete_id}/",
            "service_type": f"{API_BASE_URL}/api/service-types/{self.delete_id}/",
        }

        url = url_map.get(self.delete_type)
        if not url:
            return

        if self.delete_type == "patient":
            # For patients: PATCH to set desktop_record to 'hide'
            data = {"desktop_record": "hide"}
            response = requests.patch(url, json=data)

            if response.status_code == 200:
                Toast(self.ui, "Patient deleted  successfully!",
                      icon_path="Icons/check.png").show_toast()

                # Refresh UI
                safe_page = getattr(self.ui, 'patient_currentPage', None) or 1
                self.ui.load_patients(safe_page, search_term=None)
                self.ui.load_scheduled_services()
                if hasattr(self.ui, 'appointmentCard'):
                    self.ui.appointmentCard.load_appointments(1)
                self.ui.stackedWidget.setCurrentIndex(2)
            else:
                Toast(self.ui, "Failed to deleted  patient.",
                      icon_path="Icons/warning.png").show_toast()

        else:
            # For other types: DELETE normally
            response = requests.delete(url)
            if response.status_code == 204:
                Toast(self.ui, f"{self.delete_type.capitalize()} deleted successfully!",
                      icon_path="Icons/check.png").show_toast()

                if self.delete_type == "pet":
                    owner_id = getattr(self.ui, "selected_patient_id", None)

                    # Invalidate cached pets for this owner
                    if owner_id and hasattr(self.ui, 'api'):
                        self.ui.api.invalidate_cache(f"/api/pets/?owner_id={owner_id}")
                        if hasattr(self.ui, '_pets_sig_by_owner'):
                            self.ui._pets_sig_by_owner.pop(owner_id, None)

                    self.ui.load_scheduled_services()
                    if hasattr(self.ui, "appointmentCard"):
                        self.ui.appointmentCard.load_appointments(1)
                    if owner_id:
                        self.ui.load_pets_for_owner(owner_id, force_refresh=True, show_loading_on_miss=False)
                    else:
                        print("Warning: owner_id not found after pet deletion")
                    self.ui.stackedWidget.setCurrentIndex(5)
                elif self.delete_type == "service":
                    # Invalidate cached services for this pet
                    pet_id = getattr(self.ui, 'selected_pet_id', None)
                    if pet_id and hasattr(self.ui, 'api'):
                        self.ui.api.invalidate_cache(f"/api/services/?pet_id={pet_id}")
                        if hasattr(self.ui, '_services_sig_by_pet'):
                            self.ui._services_sig_by_pet.pop(pet_id, None)

                    self.ui.load_scheduled_services()
                    self.ui.load_services_for_pet(self.ui.selected_pet_id, force_refresh=True, show_loading_on_miss=False)
                elif self.delete_type == "service_type":
                    self.ui.addServiceCard.load_service_types(self.ui.addServiceCard.service_currentPage)
            else:
                Toast(self.ui, f"Failed to delete {self.delete_type}.",
                      icon_path="Icons/warning.png").show_toast()

        self.delete_type = None
        self.delete_id = None
        self.ui.confirmCard.hide()

    def _refresh_after_patient_delete(self):
        """Safely refresh UI after patient deletion"""
        try:
            # Use current page or fall back to page 1 if it doesn't exist
            current_page = getattr(self.ui, 'patient_currentPage', 1) or 1
            self.ui.load_patients(current_page, search_term=None)
            self.ui.load_scheduled_services()

            # ✅ Fixed: Use correct method name
            if hasattr(self.ui, 'appointmentCard'):
                self.ui.appointmentCard.load_appointments(1)

            self.ui.stackedWidget.setCurrentIndex(2)
        except Exception as e:
            print(f"Error refreshing after patient delete: {e}")

    def _refresh_after_pet_delete(self):
        """Safely refresh UI after pet deletion"""
        try:
            self.ui.load_scheduled_services()

            # ✅ Fixed: Use correct method name
            if hasattr(self.ui, 'appointmentCard'):
                self.ui.appointmentCard.load_appointments(1)

            if hasattr(self.ui, 'selected_patient_id') and self.ui.selected_patient_id:
                self.ui.load_pets_for_owner(self.ui.selected_patient_id)

            self.ui.stackedWidget.setCurrentIndex(5)
        except Exception as e:
            print(f"Error refreshing after pet delete: {e}")

    def _refresh_after_service_delete(self):
        """Safely refresh UI after service deletion"""
        try:
            self.ui.load_scheduled_services()

            if hasattr(self.ui, 'selected_pet_id') and self.ui.selected_pet_id:
                self.ui.load_services_for_pet(self.ui.selected_pet_id)
        except Exception as e:
            print(f"Error refreshing after service delete: {e}")

    def cancel_delete(self):
        self.delete_id = None
        self.delete_type = None
        self.ui.confirmCard.reject_dialog()

    def start_service_type_delete(self, service_type_id):
        self.delete_type = "service_type"
        self.delete_id = service_type_id
        self.ui.confirmCard.show_card()

    def delete_service_type(self, service_type_id, service_name=None):
        """Delete a service type"""
        try:
            # Perform soft delete
            delete_response = requests.delete(f"{API_BASE_URL}/api/service-types/{service_type_id}/")

            if delete_response.status_code == 204 or delete_response.status_code == 200:
                Toast(self.ui, f"Service type '{service_name}' deleted",
                      icon_path="Icons/check.png").show_toast()

                # Refresh service types list if popup is open
                if hasattr(self.ui, 'addServiceCard') and self.ui.addServiceCard.isVisible():
                    self.ui.addServiceCard.load_service_types(self.ui.addServiceCard.service_currentPage)
            else:
                Toast(self.ui, "Failed to delete service type",
                      icon_path="Icons/warning.png").show_toast()

        except Exception as e:
            print(f"Error deleting service type: {e}")
            Toast(self.ui, "Error deleting service type",
                  icon_path="Icons/warning.png").show_toast()

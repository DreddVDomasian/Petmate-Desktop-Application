import requests
from toast import Toast
from PyQt6.QtWidgets import QMessageBox
from config_loader import API_BASE_URL
from PyQt6.QtCore import QTimer
from async_helper import AsyncHelper


class Delete:
    def __init__(self, ui_context):
        self.ui = ui_context  # Reference to main UI
        # Prefer the main window's shared AsyncHelper (shared cache + queue), fall back if missing.
        self.api = getattr(self.ui, 'api', None) or AsyncHelper(self.ui, base_url=API_BASE_URL)
        self.delete_type = None  # "patient", "pet", "service"
        self.delete_id = None

    def set_delete_target(self, target_type, target_id):
        self.delete_type = target_type  # "patient", "pet", "service"
        self.delete_id = target_id
        # Ensure confirm card uses default delete message/styles/actions
        if hasattr(self.ui, 'restore_confirm_card_default'):
            try:
                self.ui.restore_confirm_card_default()
            except Exception:
                pass
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
            # For patients: PATCH to set desktop_record to 'hide' (async + loading)
            delete_id = self.delete_id
            safe_page = getattr(self.ui, 'patient_currentPage', None) or 1

            # Clear state early to prevent double-submit
            self.delete_type = None
            self.delete_id = None
            self.ui.confirmCard.hide()

            def _on_patient_deleted(_data):
                Toast(self.ui, "Patient deleted successfully!",
                      icon_path="Icons/check.png").show_toast()
                self.ui.load_patients(safe_page, search_term=None)
                self.ui.load_scheduled_services()
                if hasattr(self.ui, 'appointmentCard'):
                    self.ui.appointmentCard.load_appointments(1)
                self.ui.stackedWidget.setCurrentIndex(2)

            def _on_patient_delete_error(err: str):
                Toast(self.ui, "Failed to delete patient.",
                      icon_path="Icons/warning.png").show_toast()
                print(f"Delete patient failed: {err}")

            self.api.patch(
                url=f"/api/patients/{delete_id}/",
                on_success=_on_patient_deleted,
                data={"desktop_record": "hide"},
                on_error=_on_patient_delete_error,
                timeout=15,
                show_loading=True,
                loading_title="Deleting patient...",
                loading_subtitle="Please wait"
            )

        else:
            # For other types: DELETE asynchronously with loading modal (prevents UI freeze)
            delete_type = self.delete_type
            delete_id = self.delete_id

            # Capture IDs needed for refresh BEFORE clearing selection / state
            owner_id = getattr(self.ui, "selected_patient_id", None)
            selected_pet_id = getattr(self.ui, "selected_pet_id", None)

            # Clear state early to prevent double-submit
            self.delete_type = None
            self.delete_id = None
            self.ui.confirmCard.hide()

            endpoint_map = {
                "pet": f"/api/pets/{delete_id}/",
                "service": f"/api/services/{delete_id}/",
                "service_type": f"/api/service-types/{delete_id}/",
            }
            endpoint = endpoint_map.get(delete_type)
            if not endpoint:
                return

            def _on_deleted(_data):
                Toast(self.ui, f"{delete_type.capitalize()} deleted successfully!",
                      icon_path="Icons/check.png").show_toast()

                if delete_type == "pet":
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

                elif delete_type == "service":
                    # Invalidate cached services for this pet
                    if selected_pet_id and hasattr(self.ui, 'api'):
                        self.ui.api.invalidate_cache(f"/api/services/?pet_id={selected_pet_id}")
                        if hasattr(self.ui, '_services_sig_by_pet'):
                            self.ui._services_sig_by_pet.pop(selected_pet_id, None)

                    self.ui.load_scheduled_services()
                    if selected_pet_id:
                        self.ui.load_services_for_pet(selected_pet_id, force_refresh=True, show_loading_on_miss=False)

                elif delete_type == "service_type":
                    if hasattr(self.ui, 'addServiceCard'):
                        self.ui.addServiceCard.load_service_types(self.ui.addServiceCard.service_currentPage)

            def _on_delete_error(err: str):
                Toast(self.ui, f"Failed to delete {delete_type}.",
                      icon_path="Icons/warning.png").show_toast()
                print(f"Delete {delete_type} failed: {err}")

            self.api.delete(
                url=endpoint,
                on_success=_on_deleted,
                on_error=_on_delete_error,
                timeout=15,
                show_loading=True,
                loading_title=f"Deleting {delete_type}...",
                loading_subtitle="Please wait"
            )

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
        endpoint = f"/api/service-types/{service_type_id}/"

        def _on_deleted(_data):
            name = f" '{service_name}'" if service_name else ""
            Toast(self.ui, f"Service type{name} deleted",
                  icon_path="Icons/check.png").show_toast()
            if hasattr(self.ui, 'addServiceCard') and self.ui.addServiceCard.isVisible():
                self.ui.addServiceCard.load_service_types(self.ui.addServiceCard.service_currentPage)

        def _on_error(err: str):
            print(f"Error deleting service type: {err}")
            Toast(self.ui, "Failed to delete service type",
                  icon_path="Icons/warning.png").show_toast()

        self.api.delete(
            url=endpoint,
            on_success=_on_deleted,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_title="Deleting service type...",
            loading_subtitle="Please wait"
        )

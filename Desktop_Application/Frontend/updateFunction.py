
from Desktop_Application.Frontend.toast import Toast
from PyQt6.QtWidgets import QMessageBox,QComboBox
from PyQt6.QtCore import Qt, QDate, QTimer
from Desktop_Application.Frontend.config_loader import API_BASE_URL
from Desktop_Application.Frontend.async_helper import AsyncHelper

class Update:
    def __init__(self, ui_context):
        self.ui = ui_context  # Reference to main UI
        # Prefer the main window's shared AsyncHelper (shared cache + queue), fall back if missing.
        self.api = getattr(self.ui, 'api', None) or AsyncHelper(self.ui, API_BASE_URL)
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
        self.ui.secondaryPhoneEdit.setText(patient.get("SecondaryNumber"))
        self.ui.selected_patient_id = patient.get("id")

    def update_patient_info(self, owner_id):
        self.api.get(
            url=f"/api/patients/{owner_id}/",
            on_success=lambda patient: self._on_patient_loaded_for_edit(patient),
            on_error=lambda err: Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast(),
            timeout=15,
            show_loading=True,
            loading_title="Loading patient...",
            loading_subtitle="Preparing edit form"
        )

    def _on_patient_loaded_for_edit(self, patient):
        try:
            if not isinstance(patient, dict):
                raise ValueError("Invalid patient payload")

            handler = getattr(self.ui, 'ui_handler', None)
            if handler is not None and hasattr(handler, 'is_loaded') and hasattr(handler, 'load_address_data_async'):
                if not handler.is_loaded():
                    # Load address data first so province/city/barangay selections can be applied correctly.
                    handler.load_address_data_async(
                        on_ready=lambda: self._apply_patient_form_after_address_loaded(patient),
                        on_error=lambda err: self._apply_patient_form_after_address_loaded(patient)
                    )
                    return

            self._apply_patient_form_after_address_loaded(patient)
        except Exception as e:
            print(f"Failed to apply patient edit form: {e}")
            Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast()

    def _apply_patient_form_after_address_loaded(self, patient):
        try:
            self.populate_patient_form(patient)
            self.ui.navigate_to_page(1, is_update=True)

            # If patient has a linked user account, email becomes read-only
            if patient.get('user_account') is not None:
                self.ui.emailEdit.setReadOnly(True)
            else:
                self.ui.emailEdit.setReadOnly(False)
        except Exception as e:
            print(f"Failed to apply patient edit form (after address load): {e}")
            Toast(self.ui, "Failed to load patient!", icon_path="Icons/warning.png").show_toast()

    def is_email_enable(self,owner_id):
        # Legacy method: keep behavior but make it non-blocking
        self.api.get(
            url=f"/api/patients/{owner_id}/",
            on_success=lambda patient: self.ui.emailEdit.setReadOnly(bool(isinstance(patient, dict) and patient.get('user_account') is not None)),
            on_error=lambda err: Toast(self.ui, "Failed to check patient email!", icon_path="Icons/warning.png").show_toast(),
            timeout=10
        )
    def update_patient_to_api(self):
        patient_id = getattr(self.ui, "selected_patient_id", None)
        if not patient_id:
            Toast(self.ui, "No patient selected!", icon_path="Icons/warning.png").show_toast()
            return

        # Normalize phone numbers (same rules as add-patient)
        raw_phone = self.ui.phoneNumberEdit.text().strip()
        normalized_phone = getattr(self.ui, 'validate_phone_number', None)
        if callable(normalized_phone):
            formatted_phone = normalized_phone(raw_phone)
        else:
            formatted_phone = raw_phone

        if not formatted_phone:
            Toast(self.ui, "Invalid phone number. Use 09xxxxxxxxx or +639xxxxxxxxx", icon_path="Icons/warning.png").show_toast()
            return

        raw_secondary = self.ui.secondaryPhoneEdit.text().strip()
        if raw_secondary:
            if callable(normalized_phone):
                formatted_secondary = normalized_phone(raw_secondary)
            else:
                formatted_secondary = raw_secondary

            if not formatted_secondary:
                Toast(self.ui, "Invalid secondary phone number.", icon_path="Icons/warning.png").show_toast()
                return
        else:
            formatted_secondary = None

        # Collect data from widgets (same as before)
        data = {
            "firstName": self.ui.firstNameEdit.text().strip(),
            "lastName": self.ui.lastNameEdit.text().strip(),
            "middleName": self.ui.middleNameEdit.text().strip() or None,
            "email": self.ui.emailEdit.text().strip() or None,
            "phoneNumber": formatted_phone,
            "province": self.ui.provinceComboBox.currentText(),
            "city": self.ui.cityComboBox.currentText(),
            "barangay": self.ui.barangayComboBox.currentText(),
            "detailedAddress": self.ui.detailedAddressEdit.text().strip() or None,
            "SecondaryNumber": formatted_secondary
        }
        # Validate combo boxes (same as before)
        for combo, name in [
            (self.ui.provinceComboBox, "province"),
            (self.ui.cityComboBox, "city"),
            (self.ui.barangayComboBox, "barangay")
        ]:
            if combo.currentIndex() == 0 or combo.currentText().strip() == "":
                Toast(self.ui, f"Invalid {name} selected!", icon_path="Icons/warning.png").show_toast()
                return

        # --- New: Fetch current patient data and compare before updating ---
        def compare_and_update(current_patient):
            # Map API patient fields to form fields for comparison
            def norm(val):
                return (val or "").strip() if isinstance(val, str) else val
            # Compose comparable dicts
            current = {
                "firstName": norm(current_patient.get("firstName")),
                "lastName": norm(current_patient.get("lastName")),
                "middleName": norm(current_patient.get("middleName")),
                "email": norm(current_patient.get("email")),
                "phoneNumber": norm(current_patient.get("phoneNumber")),
                "province": norm(current_patient.get("province")),
                "city": norm(current_patient.get("city")),
                "barangay": norm(current_patient.get("barangay")),
                "detailedAddress": norm(current_patient.get("detailedAddress")),
                "SecondaryNumber": norm(current_patient.get("SecondaryNumber")),
            }
            new = {k: norm(v) for k, v in data.items()}
            if current == new:
                Toast(self.ui, "No updates made.", icon_path="Icons/warning.png").show_toast()
                return
            # If different, proceed with duplicate check and update
            duplicate_payload = data.copy()
            duplicate_payload["current_id"] = patient_id
            self.api.post(
                url="/api/check-duplicate/",
                data=duplicate_payload,
                on_success=lambda dup: self._on_patient_duplicate_checked(patient_id, data, dup),
                on_error=lambda err: Toast(self.ui, f"Unexpected error: {str(err)}", icon_path="Icons/warning.png").show_toast(),
                timeout=15,
                show_loading=True,
                loading_title="Updating patient...",
                loading_subtitle="Checking duplicates"
            )

        # Fetch current patient data for comparison
        self.api.get(
            url=f"/api/patients/{patient_id}/",
            on_success=compare_and_update,
            on_error=lambda err: Toast(self.ui, "Failed to check for changes!", icon_path="Icons/warning.png").show_toast(),
            timeout=10,
            show_loading=True,
            loading_title="Checking for changes...",
            loading_subtitle="Comparing data"
        )

    def _on_patient_duplicate_checked(self, patient_id, data, dup_response):
        try:
            if isinstance(dup_response, dict):
                if dup_response.get("email_conflict"):
                    Toast(self.ui, "This email is already used by another patient.",
                          icon_path="Icons/warning.png").show_toast()
                    return
                if dup_response.get("duplicates"):
                    Toast(self.ui, "Another patient already has this name.",
                          icon_path="Icons/warning.png").show_toast()
                    return

            self.api.put(
                url=f"/api/patients/{patient_id}/",
                data=data,
                on_success=lambda updated: self._on_patient_updated(patient_id, data),
                on_error=lambda err: Toast(self.ui, "Update failed!", icon_path="Icons/warning.png").show_toast(),
                timeout=20,
                show_loading=True,
                loading_title="Updating patient...",
                loading_subtitle="Saving changes"
            )
        except Exception as e:
            Toast(self.ui, f"Unexpected error: {str(e)}", icon_path="Icons/warning.png").show_toast()

    def _on_patient_updated(self, patient_id, data):
        # Invalidate patient caches so lists/detail refresh quickly
        try:
            if hasattr(self.api, 'invalidate_cache'):
                self.api.invalidate_cache("/api/patients/")
                self.api.invalidate_cache(f"/api/patients/{patient_id}/")
        except Exception:
            pass

        # Best-effort auth_user sync (non-blocking)
        self.sync_to_auth_user_if_linked(patient_id, data)

        safe_page = getattr(self.ui, 'patient_currentPage', None) or 1

        def post_update_ui():
            self.ui.clearInputs()
            self.ui.navigate_to_page(2)
            self.ui.load_patients(safe_page, search_term=None)
            Toast(self.ui, "Patient updated successfully!", icon_path="Icons/check.png").show_toast()

        QTimer.singleShot(100, post_update_ui)

    def sync_to_auth_user_if_linked(self, patient_id, patient_data):
        """Sync patient data to auth_user only if a linked account exists"""
        try:
            self.api.get(
                url=f"/api/patients/{patient_id}/",
                on_success=lambda patient_info: self._on_patient_loaded_for_user_sync(patient_info, patient_data),
                on_error=lambda err: print(f"SYNC: Failed to get patient data: {err}"),
                timeout=10
            )
        except Exception as e:
            print(f"SYNC ERROR: {e}")

    def _on_patient_loaded_for_user_sync(self, patient_info, patient_data):
        try:
            if not isinstance(patient_info, dict):
                return
            user_account_id = patient_info.get('user_account')
            if not user_account_id:
                return

            user_update_data = {
                "first_name": patient_data.get("firstName"),
                "last_name": patient_data.get("lastName"),
                "email": patient_data.get("email")
            }

            self.api.patch(
                url=f"/api/user/{user_account_id}/",
                data=user_update_data,
                on_success=lambda _: None,
                on_error=lambda err: print(f"SYNC: Failed to update User {user_account_id}: {err}"),
                timeout=10
            )
        except Exception as e:
            print(f"SYNC ERROR: {e}")
    # UPDATE PET INFO
    def populate_pet_form(self, pet):
        self.ui.petName.setText(pet["petName"])
        self.ui.petColor.setText(pet["petColor"])
        self.ui.breed.setText(pet["breed"])
        species_value = pet.get("species", "").strip()
        # Check if species exists in combo box
        index = self.ui.speciesComboBox.findText(species_value, Qt.MatchFlag.MatchFixedString)

        if index >= 0:
            # Species found (Cat or Dog)
            self.ui.speciesComboBox.setCurrentIndex(index)
            self.ui.otherSpeciesLineEdit.hide()
            self.ui.otherSpeciesLineEdit.clear()
            self.ui.clearSpeciesBtn.hide()
            self.ui.speciesComboBox.show()
        else:
            # Species not found → treat as "Others"
            others_index = self.ui.speciesComboBox.findText("Others", Qt.MatchFlag.MatchFixedString)
            if others_index >= 0:
                self.ui.speciesComboBox.setCurrentIndex(others_index)
            else:
                self.ui.speciesComboBox.setCurrentIndex(0)  # fallback
            self.ui.otherSpeciesLineEdit.show()
            self.ui.otherSpeciesLineEdit.setText(species_value)
        self.ui.age.setText(str(pet["age"]))
        self.ui.petSexComboBox.setCurrentText(pet["sex"])
        self.ui.selected_pet_id = pet["id"]
        date_str = pet.get("birthDate")
        if date_str:
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.ui.Bday.setDate(qdate)

    def update_pet_info(self, pet_id):
        self.api.get(
            url=f"/api/pets/{pet_id}/",
            on_success=lambda pet: self._on_pet_loaded_for_edit(pet),
            on_error=lambda err: Toast(self.ui, "Failed to load pet!", icon_path="Icons/warning.png").show_toast(),
            timeout=15,
            show_loading=True,
            loading_title="Loading pet...",
            loading_subtitle="Preparing edit form"
        )

    def _on_pet_loaded_for_edit(self, pet):
        try:
            if not isinstance(pet, dict):
                raise ValueError("Invalid pet payload")
            self.populate_pet_form(pet)
            self.ui.show_patient_profile(pet["owner"])
            self.ui.profileStackedWidget.setCurrentIndex(1)  # Show the pet form
            self.ui.petConfirmButton.hide()
            self.ui.petUpdateButton.show()
        except Exception as e:
            print(f"Failed to apply pet edit form: {e}")
            Toast(self.ui, "Failed to load pet!", icon_path="Icons/warning.png").show_toast()

    def update_pet_to_api(self):
        pet_id = self.ui.selected_pet_id
        if not pet_id:
            return
        species_value = self.ui.speciesComboBox.currentText()
        if species_value.lower() == "others":
            species_value = self.ui.otherSpeciesLineEdit.text().strip()
        data = {
            "petName": self.ui.petName.text(),
            "petColor": self.ui.petColor.text(),
            "breed": self.ui.breed.text(),
            "species": species_value,
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

        url = f"/api/pets/{pet_id}/"

        def compare_and_update(current_pet):
            def norm(val):
                return (val or "").strip() if isinstance(val, str) else val
            current = {
                "petName": norm(current_pet.get("petName")),
                "petColor": norm(current_pet.get("petColor")),
                "breed": norm(current_pet.get("breed")),
                "species": norm(current_pet.get("species")),
                "sex": norm(current_pet.get("sex")),
                "owner_id": current_pet.get("owner"),
                "remarks": norm(current_pet.get("remarks")),
                "birthDay": norm(current_pet.get("birthDate")),
                "stored_age": norm(str(current_pet.get("age")) if current_pet.get("age") is not None else None)
            }
            new = {
                "petName": norm(data["petName"]),
                "petColor": norm(data["petColor"]),
                "breed": norm(data["breed"]),
                "species": norm(data["species"]),
                "sex": norm(data["sex"]),
                "owner_id": data["owner_id"],
                "remarks": norm(data["remarks"]),
                "birthDay": norm(data.get("birthDay")),
                "stored_age": norm(str(data.get("stored_age")) if data.get("stored_age") is not None else None)
            }
            # Compare birthDay and stored_age logic
            if current == new:
                Toast(self.ui, "No updates made.", icon_path="Icons/warning.png").show_toast()
                return
            self.api.put(
                url=url,
                data=data,
                on_success=lambda _: self._on_pet_updated(pet_id, url),
                on_error=lambda err: Toast(self.ui, "Failed to update pet!", icon_path="Icons/warning.png").show_toast(),
                timeout=20,
                show_loading=True,
                loading_title="Updating pet...",
                loading_subtitle="Saving changes"
            )

        self.api.get(
            url=url,
            on_success=compare_and_update,
            on_error=lambda err: Toast(self.ui, "Failed to check for changes!", icon_path="Icons/warning.png").show_toast(),
            timeout=10,
            show_loading=True,
            loading_title="Checking for changes...",
            loading_subtitle="Comparing data"
        )

    def _on_pet_updated(self, pet_id, pet_url):
        Toast(self.ui, "Pet updated successfully!", icon_path="Icons/check.png").show_toast()

        # Invalidate caches for pet detail + owner's pet list
        try:
            owner_id = getattr(self.ui, 'selected_patient_id', None)
            if owner_id:
                self.api.invalidate_cache(f"/api/pets/?owner_id={owner_id}")
                if hasattr(self.ui, '_pets_sig_by_owner'):
                    self.ui._pets_sig_by_owner.pop(owner_id, None)
            self.api.invalidate_cache(pet_url)
        except Exception:
            pass

        # 🔄 Fetch updated pet so computed age reflects
        self.api.get(
            url=pet_url,
            on_success=lambda pet: self.ui.show_pet_profile(pet) if isinstance(pet, dict) else None,
            on_error=lambda err: None,
            timeout=15
        )

        owner_id = getattr(self.ui, 'selected_patient_id', None)
        if owner_id:
            try:
                self.ui.load_pets_for_owner(owner_id, force_refresh=True, show_loading_on_miss=False)
            except TypeError:
                self.ui.load_pets_for_owner(owner_id)

        self.ui.profileStackedWidget.setCurrentIndex(0)

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
        # Prescription
        if hasattr(self.ui, "prescriptionTextedit"):
            self.ui.prescriptionTextedit.setPlainText(service.get("prescription", ""))

    def update_service_info(self, service_id):
        self.ui.selected_service_id = service_id
        self.api.get(
            url=f"/api/services/{service_id}/",
            on_success=lambda service: self._on_service_loaded_for_edit(service),
            on_error=lambda err: Toast(self.ui, "Failed to load service!", icon_path="Icons/warning.png").show_toast(),
            timeout=15,
            show_loading=True,
            loading_title="Loading service...",
            loading_subtitle="Preparing edit form"
        )

    def _on_service_loaded_for_edit(self, service):
        try:
            if not isinstance(service, dict):
                raise ValueError("Invalid service payload")
            self.populate_service_form(service)
            self.ui.addServiceBtn.hide()
            self.ui.updateServiceBtn.show()
            self.ui.addNewServiceBtn.setChecked(True)
            self.ui.addNewServiceBtn.setText("Update service")
            self.ui.serviceHistoryStackedWidget.setCurrentIndex(1)
            if (service.get("service_type") or "").upper() == "VACCINATION":
                self.ui.dateEdit.setEnabled(False)
        except Exception as e:
            print(f"Failed to apply service edit form: {e}")
            Toast(self.ui, "Failed to load service!", icon_path="Icons/warning.png").show_toast()

    def update_service_to_api(self):
        service_id = self.ui.selected_service_id  # Make sure this is set when clicking "edit"
        if not service_id:
            Toast(self.ui, "No service selected for update!", icon_path="Icons/warning.png").show_toast()
            return

        # Build data payload
        data = {
            "owner": self.ui.selected_patient_id,
            "pet": self.ui.selected_pet_id,
            "service_type_id": self.ui.serviceTypeComboBox.currentData(),
            "date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "notes": self.ui.addNoteLineEdit.toPlainText(),
            "prescription": getattr(self.ui, "prescriptionTextedit", None).toPlainText().strip() if hasattr(self.ui, "prescriptionTextedit") else ""
        }

        # Handle optional return date
        if self.ui.returnCheckBox.isChecked():
            data["return_date"] = self.ui.returnDateEdit.date().toString("yyyy-MM-dd")
        else:
            data["return_date"] = None  # or skip this key entirely depending on API

        url = f"/api/services/{service_id}/"

        def compare_and_update(current_service):
            def norm(val):
                return (val or "").strip() if isinstance(val, str) else val
            current = {
                "owner": current_service.get("owner"),
                "pet": current_service.get("pet"),
                "service_type_id": current_service.get("service_type_id"),
                "date": norm(current_service.get("date")),
                "notes": norm(current_service.get("notes")),
                "prescription": norm(current_service.get("prescription")),
                "return_date": norm(current_service.get("return_date")),
            }
            new = {
                "owner": data["owner"],
                "pet": data["pet"],
                "service_type_id": data["service_type_id"],
                "date": norm(data["date"]),
                "notes": norm(data["notes"]),
                "prescription": norm(data["prescription"]),
                "return_date": norm(data["return_date"]),
            }
            if current == new:
                Toast(self.ui, "No updates made.", icon_path="Icons/warning.png").show_toast()
                return
            self.api.put(
                url=url,
                data=data,
                on_success=lambda _: self._on_service_updated(service_id),
                on_error=lambda err: Toast(self.ui, "Failed to update service!", icon_path="Icons/warning.png").show_toast(),
                timeout=20,
                show_loading=True,
                loading_title="Updating service...",
                loading_subtitle="Saving changes"
            )

        self.api.get(
            url=url,
            on_success=compare_and_update,
            on_error=lambda err: Toast(self.ui, "Failed to check for changes!", icon_path="Icons/warning.png").show_toast(),
            timeout=10,
            show_loading=True,
            loading_title="Checking for changes...",
            loading_subtitle="Comparing data"
        )

    def _on_service_updated(self, service_id):
        Toast(self.ui, "Service updated successfully!", icon_path="Icons/check.png").show_toast()

        # Invalidate caches for this pet's services
        try:
            pet_id = getattr(self.ui, 'selected_pet_id', None)
            if pet_id:
                self.api.invalidate_cache(f"/api/services/?pet_id={pet_id}")
                if hasattr(self.ui, '_services_sig_by_pet'):
                    self.ui._services_sig_by_pet.pop(pet_id, None)
            self.api.invalidate_cache(f"/api/services/{service_id}/")
        except Exception:
            pass

        pet_id = getattr(self.ui, 'selected_pet_id', None)
        if pet_id:
            try:
                self.ui.load_services_for_pet(pet_id, force_refresh=True, show_loading_on_miss=False)
            except TypeError:
                self.ui.load_services_for_pet(pet_id)

        self.ui.service_stackedWidget(0)  # go back to history
        self.ui.updateServiceBtn.hide()
        self.ui.dateEdit.setEnabled(True)
        self.ui.addServiceBtn.show()
        self.ui.clearInputs()

    # SERVICE TYPE UPDATE METHODS
    def update_service_type_info(self, service_type_id):
        """Load service type info into addServiceCard for editing."""
        self.api.get(
            url=f"/api/service-types/{service_type_id}/",
            on_success=lambda service: self._on_service_type_loaded_for_edit(service_type_id, service),
            on_error=lambda err: Toast(self.ui, "Failed to load service type", icon_path="Icons/warning.png").show_toast(),
            timeout=15,
            show_loading=True,
            loading_title="Loading service type...",
            loading_subtitle="Preparing edit form"
        )

    def _on_service_type_loaded_for_edit(self, service_type_id, service):
        try:
            if not isinstance(service, dict):
                raise ValueError("Invalid service type payload")

            # SHOW POPUP
            self.ui.addServiceCard.show_card()

            # ENABLE EDIT MODE
            self.ui.addServiceCard.is_edit_mode = True
            self.ui.addServiceCard.selected_service_type_id = service_type_id

            # POPULATE FIELDS
            self.ui.addServiceCard.serviceNameLineEdit.setText(service.get("name", ""))
            self.ui.addServiceCard.serviceDescription.setText(service.get("description", ""))

            # CHANGE BUTTON TEXT
            self.ui.addServiceCard.addServiceBtn.setText("UPDATE SERVICE")
        except Exception as e:
            print(f"Error loading service type: {e}")
            Toast(self.ui, "Error loading service type", icon_path=resource_path("Icons/warning.png")).show_toast()
            
    def update_service_type_to_api(self, service_type_id):
        # This method assumes you have a UI for editing service types and a button that calls this
        name = self.ui.addServiceCard.serviceNameLineEdit.text().strip()
        description = self.ui.addServiceCard.serviceDescription.text().strip()
        data = {
            "name": name,
            "description": description
        }
        url = f"/api/service-types/{service_type_id}/"

        def compare_and_update(current_type):
            def norm(val):
                return (val or "").strip() if isinstance(val, str) else val
            current = {
                "name": norm(current_type.get("name")),
                "description": norm(current_type.get("description")),
            }
            new = {
                "name": norm(data["name"]),
                "description": norm(data["description"]),
            }
            if current == new:
                Toast(self.ui, "No updates made.", icon_path="Icons/warning.png").show_toast()
                return
            self.api.put(
                url=url,
                data=data,
                on_success=lambda _: Toast(self.ui, "Service type updated successfully!", icon_path="Icons/check.png").show_toast(),
                on_error=lambda err: Toast(self.ui, "Failed to update service type!", icon_path="Icons/warning.png").show_toast(),
                timeout=20,
                show_loading=True,
                loading_title="Updating service type...",
                loading_subtitle="Saving changes"
            )

        self.api.get(
            url=url,
            on_success=compare_and_update,
            on_error=lambda err: Toast(self.ui, "Failed to check for changes!", icon_path="Icons/warning.png").show_toast(),
            timeout=10,
            show_loading=True,
            loading_title="Checking for changes...",
            loading_subtitle="Comparing data"
        )


def is_valid_combobox_input(combo: QComboBox) -> bool:
    text = combo.currentText()
    for i in range(combo.count()):
        if combo.itemText(i).strip().lower() == text.strip().lower():
            return True
    return False


import os
import sys

# Get the Desktop_Application directory (one level up from frontend/)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)      # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter, QLabel, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate, QTimer
from input_styles import *
from shadowEffects import *
from toast import Toast
from Desktop_Application.Backend.api_client import add_new_appointment
from datetime import datetime
import requests


class AddAppointmentCard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("addAppointmentCard.ui", self)
        self.card_manager = AppointmentCardManager(self)

        # store a ref to animation so it's not GC'd and we can stop it
        self.anim = None

        # layouts
        self.setup_stackLayout()

        # for frameless pop up
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # shadow
        self.setup_input_shadow()

        self.popUpDateEdit.setDate(QDate.currentDate())
        self.popUpDateEdit.mousePressEvent = lambda event: self.on_date_field_clicked(self.popUpDateEdit)

        # Avoid double wiring on init: ensure combobox connections are clear
        try:
            self.selectPatientPopUp.currentIndexChanged.disconnect()
        except Exception:
            pass

        self.setup_comboboxes()

        # submit data
        # ensure single connection
        try:
            self.addAppointmentBtn.clicked.disconnect()
        except Exception:
            pass
        self.addAppointmentBtn.clicked.connect(self.submit_appointment_data)

        # load data
        self.load_appointments(1)
        self.setup_status_filters()
        self.web_Appointment()

        # make sure we only connect once
        if self.main_window:
            try:
                self.main_window.websiteBtn.clicked.disconnect()
            except Exception:
                pass
            self.main_window.websiteBtn.clicked.connect(lambda: self.web_Appointment())

        if parent:
            parent.installEventFilter(self)

    # SET UP LAYOUT/SHADOW FOR MODAL
    def setup_stackLayout(self):
        # pending layout
        self.pendingLayout = self.main_window.walkInScrollAreaWidgetContents.layout()
        self.pendingLayout.setSpacing(10)
        self.pendingLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # completed layout
        self.completedLayout = self.main_window.completedScrollAreaWidgetContents.layout()
        self.completedLayout.setSpacing(10)
        self.completedLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # overdue layout
        self.overdueLayout = self.main_window.overdueScrollAreaWidgetContents.layout()
        self.overdueLayout.setSpacing(10)
        self.overdueLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # cancelled layout
        self.cancelledLayout = self.main_window.cancelledScrollAreaWidgetContents.layout()
        self.cancelledLayout.setSpacing(10)
        self.cancelledLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Web Appointment
        self.pendingWebLayout = self.main_window.scrollAreaWebAppPending.layout()
        self.pendingWebLayout.setSpacing(10)
        self.pendingWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Accepted layout
        self.acceptedWebLayout = self.main_window.scrollAreaWebAppAccepted.layout()
        self.acceptedWebLayout.setSpacing(10)
        self.acceptedWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # declined layout
        self.declinedWebLayout = self.main_window.scrollAreaWebAppDeclined.layout()
        self.declinedWebLayout.setSpacing(10)
        self.declinedWebLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setup_input_shadow(self):
        for comboBox in self.addPopUPFrame.findChildren(QComboBox):
            comboBox.setGraphicsEffect(create_card_shadow())

        self.popUpDateEdit.setGraphicsEffect(create_card_shadow())
        self.timeEdit.setGraphicsEffect(create_card_shadow())

        # other Shadows
        self.addPopUPFrame.setGraphicsEffect(create_card_shadow())
        self.cancelAddAppointment.setGraphicsEffect(create_card_shadow())
        self.addAppointmentBtn.setGraphicsEffect(create_card_shadow())

        # ensure safe connect
        try:
            self.selectPatientPopUp.currentIndexChanged.disconnect()
        except Exception:
            pass
        self.selectPatientPopUp.currentIndexChanged.connect(self.on_patient_selected)

    # CARD POSITION LOGIC
    def show_card(self):
        if self.parent():
            parent_widget = self.parent()
            # Center sa parent
            x = (parent_widget.width() - self.width()) // 2
            y = (parent_widget.height() - self.height()) // 2
            self.move(x, y)

        # Fade in animation (stop previous if exists)
        if hasattr(self, "anim") and self.anim:
            try:
                self.anim.stop()
            except Exception:
                pass
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.anim = anim  # Keep reference para di ma-garbage collect
        # refresh data
        self.load_appointments(1)

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)

    # SET UP COMBO BOXES AND DATA SUBMITTING
    def load_patients_to_combobox(self):
        """Load ALL patients for the combobox without pagination"""
        try:
            response = requests.get(
                "http://127.0.0.1:8000/api/patient-combobox-data/",
                timeout=10
            )
        except requests.exceptions.ConnectionError:
            print("Backend offline — cannot load combobox yet.")
            return  # Stop early — avoid trying to parse response
        except Exception as e:
            print(f"Unexpected error while requesting patients combobox: {e}")
            return

        # If request succeeded but backend returned error status
        if response.status_code != 200:
            print(f"Failed to load patients for combobox: {response.status_code}")
            return

        try:
            patients = response.json()
        except ValueError:
            print("Invalid JSON received from backend")
            return

        # ✅ Clear and repopulate combobox
        self.selectPatientPopUp.blockSignals(True)
        self.selectPatientPopUp.clear()
        self.selectPatientPopUp.addItem("", None)

        for patient in patients:
            # guard fields
            name = patient.get("full_name") or ""
            pid = patient.get("id")
            self.selectPatientPopUp.addItem(name, pid)

        self.selectPatientPopUp.blockSignals(False)
        self.set_dynamic_completer(self.selectPatientPopUp)

    def on_patient_selected(self, index):
        # safe guard in case combobox is not yet populated
        try:
            patient_id = self.selectPatientPopUp.itemData(index)
        except Exception:
            patient_id = None

        if not patient_id:
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            return

        url = f"http://127.0.0.1:8000/api/pets/?owner_id={patient_id}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.ConnectionError:
            print("Backend offline — cannot load pets.")
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            return
        except Exception as e:
            print(f"Error loading pets: {e}")
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            return

        if response.status_code == 200:
            try:
                pets = response.json()
            except ValueError:
                pets = []
        else:
            pets = []

        self.selectPetPopUp.clear()
        self.selectPetPopUp.addItem("", None)
        for pet in pets:
            pet_name = pet.get("petName") or ""
            pet_id = pet.get("id")
            self.selectPetPopUp.addItem(pet_name, pet_id)

        self.set_dynamic_completer(self.selectPetPopUp)

    def on_date_field_clicked(self, dateEdit):
        if self.main_window:
            self.main_window.show_custom_calendar(dateEdit)

    def setup_comboboxes(self):
        # ensure single initialization
        # call load patients non-blocking? it's fine synchronously here
        self.load_patients_to_combobox()
        combo_boxes = [self.selectPatientPopUp, self.selectPetPopUp]
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
        completer.setFilterMode(Qt.MatchFlag.MatchContains)  # Change to MatchContains
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
        service_name = self.serviceTypeComboBox.currentText()

        # basic validation
        missing = []
        if not patient_id:
            missing.append("Patient")
        if not date:
            missing.append("Date")
        if not time:
            missing.append("Time")
        if not service_name:
            missing.append("Service")

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
            "service_name": service_name,  # include service
        }

        # send data to backend (api_client wrapper handles HTTP)
        try:
            ok = add_new_appointment(appointment_data)
        except Exception as e:
            print(f"Error adding appointment: {e}")
            ok = False

        if ok:
            toast = Toast(self.main_window, "Appointment added!", icon_path="Icons/check.png")
            toast.show_toast()
            self.close()
            # refresh appointment list in this modal
            QTimer.singleShot(150, lambda: self.load_appointments(1))
        else:
            toast = Toast(self.main_window, "Failed to add appointment!", icon_path="Icons/warning.png")
            toast.show_toast()

    # LOADING WALK IN APPOINTMENTS AND CARD LOGIC
    def setup_status_filters(self):
        """Connect status buttons to filter appointments"""
        status_buttons = {
            "pending": self.main_window.pendingBtn,
            "completed": self.main_window.completedBtn,
            "overdue": self.main_window.overdueBtn,
            "cancelled": self.main_window.cancelledBtn
        }

        for status, button in status_buttons.items():
            try:
                button.clicked.disconnect()
            except Exception:
                pass
            button.clicked.connect(lambda checked, s=status: self.load_appointments(1, s))

    def load_appointments(self, page=1, status_filter=None):
        """Load appointments with pagination and filtering"""
        try:
            # Clear existing appointment cards
            self.card_manager.clear_layouts()

            # Build API URL with pagination and filtering
            url = f"http://127.0.0.1:8000/api/walkIn/?page={page}"
            if status_filter:
                url += f"&status={status_filter}"

            # Make API request (safe)
            try:
                response = requests.get(url, timeout=10)
            except requests.exceptions.ConnectionError:
                print("Backend is offline. Skipping load.")
                self.show_empty_all_layouts()
                return
            except Exception as e:
                print(f"Unexpected error requesting appointments: {e}")
                self.show_empty_all_layouts()
                return

            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    print("Invalid JSON for appointments")
                    self.show_empty_all_layouts()
                    return

                # If backend returned empty safely, treat it as no data rather than an error
                if data.get('count', 0) == 0:
                    self.show_empty_all_layouts()
                    return

                appointments = data.get('results', [])
                # Update pagination info
                self.card_manager.current_appointment_page = page
                self.card_manager.total_appointment_pages = data.get('total_pages', 1)
                self.card_manager.total_appointment_count = data.get('count', 0)
                self.card_manager.current_status_filter = status_filter

            else:
                print(f"Failed to load appointments: {response.status_code}")
                self.show_empty_all_layouts()
                return

            # Handle empty results
            if not appointments:
                self.show_empty_all_layouts()
                return

            # Create and distribute appointment cards to appropriate layouts
            self.distribute_appointment_cards(appointments)

            # Add pagination to the current active layout
            current_layout = self.get_current_active_layout()
            if current_layout:
                self.card_manager.add_appointment_pagination_controls(current_layout, status_filter)

        except Exception as e:
            # This is a last-resort catch — avoid letting errors bubble up to OS-level crash
            import traceback
            traceback.print_exc()
            print(f"Error loading appointments (caught): {e}")
            self.show_empty_all_layouts()

    def distribute_appointment_cards(self, appointments):
        """Distribute appointment cards to their respective status layouts"""
        status_layouts = {
            "pending": self.pendingLayout,  # Access directly
            "completed": self.completedLayout,
            "overdue": self.overdueLayout,
            "cancelled": self.cancelledLayout
        }

        # Group appointments by status
        appointments_by_status = {status: [] for status in status_layouts.keys()}
        for appointment in appointments:
            status = appointment.get("status", "pending")
            if status in appointments_by_status:
                appointments_by_status[status].append(appointment)

        # Create cards for each status group
        for status, layout in status_layouts.items():
            status_appointments = appointments_by_status.get(status, [])
            if not status_appointments:
                self.card_manager.show_empty_state(layout)
                continue

            for appointment in status_appointments:
                card = self.card_manager.create_appointment_card(appointment)
                layout.addWidget(card)
                self.card_manager.appointment_cards.append(card)

    def get_current_active_layout(self):
        """Get the currently active layout based on status filter"""
        status_layout_map = {
            "pending": self.pendingLayout,  # Access directly
            "completed": self.completedLayout,
            "overdue": self.overdueLayout,
            "cancelled": self.cancelledLayout,
            None: self.pendingLayout  # Default to pending if no filter
        }
        return status_layout_map.get(self.card_manager.current_status_filter)

    def open_pet_from_appointment(self, pet_id):
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/", timeout=10)
        except Exception:
            return
        if response.status_code == 200:
            try:
                pet = response.json()
            except ValueError:
                return
            self.main_window.show_pet_profile(pet)

    def cancelled_appointment(self, appointment_id):
        # avoid stacking connections
        try:
            self.main_window.confirmCard.yesButton.clicked.disconnect()
            self.main_window.confirmCard.noButton.clicked.disconnect()
        except Exception:
            pass

        self.main_window.confirmCard.confirmationMessage.setText("Are you sure you want to cancel \nthis appointment?")
        self.main_window.confirmCard.show_card()

        def clicked_yes():
            url = f"http://127.0.0.1:8000/api/walkIn/{appointment_id}/"
            try:
                response = requests.patch(url, json={"status": "cancelled"}, timeout=10)
            except Exception as e:
                print("Failed to contact backend to cancel appointment:", e)
                self.main_window.confirmCard.hide()
                return

            if response.status_code in [200, 202]:
                print("Reminder marked as cancelled")
                # refresh current modal appointment list safely
                QTimer.singleShot(100, lambda: self.load_appointments(1))
            else:
                print("Failed:", response.text)
            self.main_window.confirmCard.hide()

        def clicked_no():
            self.main_window.confirmCard.hide()

        # single connect
        self.main_window.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.main_window.confirmCard.noButton.clicked.connect(clicked_no)

    def show_empty_all_layouts(self):
        """Show empty state in all layouts"""
        layouts = [
            self.pendingLayout,  # Access directly, not through main_window
            self.completedLayout,
            self.overdueLayout,
            self.cancelledLayout
        ]
        for layout in layouts:
            self.card_manager.show_empty_state(layout)

    # -------------------------------------------WEB APPOINTMENT---------------------------------------
    def web_Appointment(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/appointments/", timeout=10)
        except requests.exceptions.ConnectionError:
            print("Backend offline — cannot load web appointments")
            appointments = []
        except Exception as e:
            print(f"Error loading web appointments: {e}")
            appointments = []
        else:
            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    data = []
                # handle both cases safely
                if isinstance(data, dict) and "appointments" in data:
                    appointments = data["appointments"]
                else:
                    appointments = data
            else:
                appointments = []

        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        for appoint in appointments:
            card = uic.loadUi("webAppointmentCard.ui")
            card.ownerName.setText(appoint.get("client_name", "").title())
            raw_datetime = appoint.get("appointment_datetime", "")
            # Split into date and time parts
            parts = raw_datetime.split(" ", 1)  # ["2025-09-18", "9:00 AM"]
            date_only = parts[0] if parts else ""
            time_only = parts[1] if len(parts) > 1 else ""
            # Format the date
            formatted_date = self.main_window.format_date(date_only)
            # date + time
            dateAndTime = f"{formatted_date}   {time_only}"

            card.DateTime.setText(dateAndTime)

            card.setGraphicsEffect(create_card_shadow())
            status = appoint.get("status", "pending")

            if status == "pending":
                self.pendingWebLayout.addWidget(card)
            elif status == "accepted":
                self.acceptedWebLayout.addWidget(card)
            elif status == "declined":
                self.declinedWebLayout.addWidget(card)

            # avoid stacking many connects — use lambda default args
            card.ReviewButton.clicked.connect(lambda _, a=appoint, date=dateAndTime: self.show_review_page(a, date))

        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            if layout.count() == 0:
                self.add_empty_label(layout)

    def show_review_page(self, appoint, date):
        # Owner details
        self.main_window.BookingId.setText(appoint.get("booking_id", ""))
        self.main_window.reviewFullname.setText(appoint.get("client_name", "").capitalize())
        self.main_window.reviewPhoneNo.setText(appoint.get("phone", ""))
        self.main_window.reviewEmail.setText(appoint.get("email", "").capitalize())
        address = f"{appoint.get('barangay','')}, {appoint.get('city','')}, {appoint.get('province','')}"
        self.main_window.reviewAddress.setText(address.capitalize())
        self.main_window.reviewDetailedAddress.setText(appoint.get("detailed_address", "").capitalize())

        # Pet details
        self.main_window.reviewPetName.setText(appoint.get("pet_name", "").capitalize())
        self.main_window.reviewSpecies.setText(appoint.get("species", "").capitalize())
        self.main_window.reviewBreed.setText(appoint.get("breed", "").capitalize())
        self.main_window.reviewSex.setText(appoint.get("sex", "").capitalize())
        self.main_window.reviewColor.setText(appoint.get("color", "").capitalize())
        self.main_window.reviewDoctor.setText(appoint.get("provider", "").capitalize())
        self.main_window.reviewService.setText(appoint.get("appointment_reason", "").capitalize())
        self.main_window.reviewComments.setText(appoint.get("comments", "").capitalize())
        self.main_window.reviewDateTime.setText(date)
        self.main_window.navigate_to_page(7)

        status = appoint.get("status", "pending")
        self.main_window.AcceptDeclineFrame.setVisible(status == "pending")

        species = appoint.get("species", "").lower()
        if species == "dog":
            icon_path = "Icons/dog.png"
        elif species == "cat":
            icon_path = "Icons/catIcon.png"
        else:
            icon_path = "Icons/otherSpecies.png"
        self.main_window.ReviewPetIcon.setPixmap(QPixmap(icon_path))

        # disconnect previous connectors (safe)
        try:
            self.main_window.acceptAppointmentBtn.clicked.disconnect()
            self.main_window.declineAppointmentBtn.clicked.disconnect()
        except Exception:
            pass

        self.main_window.acceptAppointmentBtn.clicked.connect(lambda _, r_id=appoint.get('id'): self.accepted_booking(r_id))
        self.main_window.declineAppointmentBtn.clicked.connect(lambda _, r_id=appoint.get('id'): self.declined_booking(r_id))

    def accepted_booking(self, review_id):
        if not review_id:
            return
        url = f"http://127.0.0.1:8000/api/appointments/{review_id}/statusUpdate/"
        try:
            response = requests.patch(url, json={"status": "accepted"}, timeout=10)
        except Exception as e:
            print("Failed to accept booking:", e)
            return
        if response.status_code in [200, 202]:
            self.web_Appointment()
            self.main_window.navigate_to_page(3)
            self.main_window.walkInOrWeb.setCurrentIndex(1)
            self.main_window.webAppointmentStackWidget.setCurrentIndex(1)
            self.main_window.AcceptedBtn.setChecked(True)
        else:
            print("Failed:", response.text)

    def declined_booking(self, review_id):
        if not review_id:
            return
        url = f"http://127.0.0.1:8000/api/appointments/{review_id}/statusUpdate/"
        try:
            response = requests.patch(url, json={"status": "declined"}, timeout=10)
        except Exception as e:
            print("Failed to decline booking:", e)
            return
        if response.status_code in [200, 202]:
            self.web_Appointment()
            self.main_window.navigate_to_page(3)
            self.main_window.walkInOrWeb.setCurrentIndex(1)
            self.main_window.webAppointmentStackWidget.setCurrentIndex(2)
            self.main_window.DeclinedBtn.setChecked(True)
        else:
            print("Failed:", response.text)

    def add_empty_label(self, layout, message="EMPTY"):
        empty_label = QLabel(message)
        empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
        layout.addStretch()
        layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()


class AppointmentCardManager:
    def __init__(self, appointment_card_instance):
        self.appointment_card = appointment_card_instance  # Reference to AddAppointmentCard instance
        self.main_window = appointment_card_instance.main_window
        self.appointment_cards = []
        self.current_appointment_page = 1
        self.total_appointment_pages = 1
        self.total_appointment_count = 0
        self.current_status_filter = None
        self.appointment_pagination_widget = None

    def clear_layouts(self):
        """Clear all appointment layouts"""
        layouts = [
            self.appointment_card.pendingLayout,  # Access through appointment_card, not main_window
            self.appointment_card.completedLayout,
            self.appointment_card.overdueLayout,
            self.appointment_card.cancelledLayout
        ]

        for layout in layouts:
            while layout.count():
                child = layout.takeAt(0)
                if child and child.widget():
                    child.widget().deleteLater()

    def show_empty_state(self, layout, message="EMPTY"):
        """Show empty state message in a layout"""
        empty_label = QLabel(message)
        empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
        layout.addStretch()
        layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

    def create_appointment_card(self, appointment):
        """Create and configure an appointment card"""
        card = uic.loadUi("appointmentCard.ui")

        # Set appointment information (guard keys)
        card.ownerName.setText(appointment.get("owner_full_name", "").title())
        card.petNameApp.setText((appointment.get("petName") or "").capitalize())
        card.serviceApp.setText((appointment.get("service_name") or "").capitalize())
        card.appDate.setText(self.main_window.format_date(appointment.get("date")))

        # Format time
        time_str = appointment.get("prefTime")
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
                formatted_time = time_obj.strftime("%I:%M %p").lstrip("0")
                card.preferredTime.setText(formatted_time)
            except ValueError:
                card.preferredTime.setText("N/A")
        else:
            card.preferredTime.setText("N/A")

        # Connect buttons (avoid stacking)
        appointment_id = appointment.get("id")
        try:
            card.deleteButton.clicked.disconnect()
        except Exception:
            pass
        card.deleteButton.clicked.connect(lambda _, a_id=appointment_id: self.appointment_card.cancelled_appointment(a_id))
        card.mousePressEvent = lambda event, pid=appointment.get("pet"): self.appointment_card.open_pet_from_appointment(pid)

        card.setGraphicsEffect(create_card_shadow())
        return card

    def add_appointment_pagination_controls(self, layout, status_filter=None):
        """Add pagination controls for appointments"""
        # Safely remove existing pagination widget
        if self.appointment_pagination_widget:
            try:
                if self.appointment_pagination_widget and self.appointment_pagination_widget.isWidgetType():
                    self.appointment_pagination_widget.deleteLater()
            except RuntimeError:
                pass
            self.appointment_pagination_widget = None

        if self.total_appointment_pages <= 1:
            return

        try:
            self.appointment_pagination_widget = uic.loadUi("paginationUi.ui")

            # Connect prev/next buttons with status filter (disconnect first)
            try:
                self.appointment_pagination_widget.PrevPage.clicked.disconnect()
            except Exception:
                pass
            try:
                self.appointment_pagination_widget.NextPage.clicked.disconnect()
            except Exception:
                pass

            self.appointment_pagination_widget.PrevPage.clicked.connect(
                lambda: self.appointment_card.load_appointments(self.current_appointment_page - 1, status_filter)
            )
            self.appointment_pagination_widget.NextPage.clicked.connect(
                lambda: self.appointment_card.load_appointments(self.current_appointment_page + 1, status_filter)
            )

            # Set button states
            self.appointment_pagination_widget.PrevPage.setEnabled(self.current_appointment_page > 1)
            self.appointment_pagination_widget.NextPage.setEnabled(
                self.current_appointment_page < self.total_appointment_pages)

            # Create page buttons with status filter support
            self.create_appointment_page_buttons(status_filter)

            self.appointment_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())
            layout.addWidget(self.appointment_pagination_widget)

        except Exception as e:
            print(f"Error creating appointment pagination: {e}")

    def create_appointment_page_buttons(self, status_filter=None):
        """Create page buttons for appointment pagination"""
        if not self.appointment_pagination_widget:
            return

        page_layout = self.appointment_pagination_widget.pageButtonsLayout

        # Clear existing buttons
        while page_layout.count():
            child = page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_page = self.current_appointment_page
        total_pages = self.total_appointment_pages
        max_visible_pages = 7

        if total_pages <= max_visible_pages:
            start_page = 1
            end_page = total_pages
        else:
            if current_page <= 4:
                start_page = 1
                end_page = 7
            elif current_page >= total_pages - 3:
                start_page = total_pages - 6
                end_page = total_pages
            else:
                start_page = current_page - 3
                end_page = current_page + 3

        # Add page number buttons
        for page in range(start_page, end_page + 1):
            page_btn = QPushButton(str(page))
            page_btn.setFixedSize(40, 40)
            if current_page > 99:
                page_btn.setFixedSize(45, 45)
            font = page_btn.font()
            font.setPointSize(10)
            font.setBold(True)
            page_btn.setFont(font)

            try:
                page_btn.clicked.disconnect()
            except Exception:
                pass

            if page == current_page:
                page_btn.setStyleSheet(current_pageBtn)
            else:
                page_btn.setStyleSheet(other_pageBtn)
                # Pass status filter when loading different pages
                page_btn.clicked.connect(lambda checked, p=page: self.appointment_card.load_appointments(p, status_filter))

            page_layout.addWidget(page_btn)

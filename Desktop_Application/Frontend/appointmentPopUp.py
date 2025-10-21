import os
import sys

# ETO ANG SAGGOT
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)      # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QCompleter, QLabel, QComboBox, QPushButton, QSizePolicy, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate,QTimer
from input_styles import *
from  shadowEffects import *
from toast import Toast
from Desktop_Application.Backend.api_client import add_new_appointment
from datetime import datetime
from functools import partial
import requests

class AddAppointmentCard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/addAppointmentCard.ui", self)
        self.card_manager = AppointmentCardManager(self)

        #layouts
        self.setup_stackLayout()

        #for frameless pop up
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # shaadow
        self.setup_input_shadow()

        self.popUpDateEdit.setMinimumDate(QDate.currentDate())
        self.popUpDateEdit.setReadOnly(True)
        self.popUpDateEdit.setDate(QDate.currentDate())
        self.popUpDateEdit.mousePressEvent = lambda event: self.on_date_field_clicked(self.popUpDateEdit)

        self.setup_comboboxes()

        # submit data
        self.addAppointmentBtn.clicked.connect(self.submit_appointment_data)

        # load data
        self.load_appointments(1,"pending", search_term=None)
        self.setup_status_filters()
        self.web_Appointment()
        self.status_filter_global = None
        self.main_window.websiteBtn.clicked.connect(lambda: self.web_Appointment())
        self.main_window.appointmentBtn.clicked.connect(lambda: self.web_Appointment())
        self.setup_search()

        self.setup_time_combo_box()
        # Connect date change signal to update time slots
        self.popUpDateEdit.dateChanged.connect(self.update_time_slots_availability)
        if parent:
            parent.installEventFilter(self)

    #SET UP LAYOUT/SHADOW FOR MODAL
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
        self.timeComboBox.setGraphicsEffect(create_card_shadow())

        #other Shadows
        self.addPopUPFrame.setGraphicsEffect(create_card_shadow())
        self.cancelAddAppointment.setGraphicsEffect(create_card_shadow())
        self.addAppointmentBtn.setGraphicsEffect(create_card_shadow())

        self.selectPatientPopUp.currentIndexChanged.connect(self.on_patient_selected)


        #OTHER SHADOW
        self.addAppointmentHeader.setGraphicsEffect(create_card_shadow(3,2,2,))

    #CARD POSITION LOGIC
    def show_card(self):
        if self.parent():
            parent_widget = self.parent()
            # Center sa parent
            x = (parent_widget.width() - self.width()) // 2
            y = (parent_widget.height() - self.height()) // 2
            self.move(x, y)

        # Fade in animation
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.anim = anim  # Keep reference para di ma-garbage collect
        self.load_appointments(1, "pending", search_term=None)
    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)

    #SET UP COMBO BOXES AND DATA SUBMITTING
    def load_patients_to_combobox(self):
        """Load ALL patients for the combobox without pagination"""
        try:
            response = requests.get("http://127.0.0.1:8000/api/patient-combobox-data/")
            if response.status_code == 200:
                patients = response.json()  # This will be the direct list, no pagination
                self.selectPatientPopUp.clear()
                self.selectPatientPopUp.addItem("", None)

                for patient in patients:
                    self.selectPatientPopUp.addItem(patient['full_name'], patient['id'])

                self.set_dynamic_completer(self.selectPatientPopUp)

            else:
                print("Failed to load patients for combobox")

        except Exception as e:
            print(f"Error loading patients for combobox: {e}")
    def on_patient_selected(self, index):
        patient_id = self.selectPatientPopUp.itemData(index)
        if not patient_id:
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            return

        url = f"http://127.0.0.1:8000/api/pets/?owner_id={patient_id}"
        response = requests.get(url)
        if response.status_code == 200:
            pets = response.json()
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            for pet in pets:
                self.selectPetPopUp.addItem(pet['petName'], pet['id'])

            self.set_dynamic_completer(self.selectPetPopUp)
        else:
            print("Failed to load pets")
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
    def on_date_field_clicked(self, dateEdit):
        if self.main_window:
            self.main_window.show_custom_calendar(dateEdit)
    def setup_time_combo_box(self):
        """Set up the time combo box with clinic hours and real-time availability"""
        self.timeComboBox.clear()

        # Generate time slots from 9:30 AM to 5:30 PM in 1-hour intervals
        start_hour = 9
        start_minute = 30
        end_hour = 17  # 5 PM
        end_minute = 30

        current_hour = start_hour
        current_minute = start_minute

        selected_date = self.popUpDateEdit.date().toString("yyyy-MM-dd")

        while current_hour < end_hour or (current_hour == end_hour and current_minute <= end_minute):
            # Format time for display (12-hour format with AM/PM)
            period = "AM" if current_hour < 12 else "PM"
            display_hour = current_hour if current_hour <= 12 else current_hour - 12
            if display_hour == 0:
                display_hour = 12

            time_display = f"{display_hour}:{current_minute:02d} {period}"

            # Format time for storage (24-hour format)
            time_value = f"{current_hour:02d}:{current_minute:02d}:00"

            # Check availability for this time slot
            is_available = self.is_time_slot_available(selected_date, time_value)

            if is_available:
                self.timeComboBox.addItem(time_display, time_value)
            else:
                # Show unavailable slots as disabled
                self.timeComboBox.addItem(f"{time_display} (FULL)", time_value)
                # Get the last added item and disable it
                last_index = self.timeComboBox.count() - 1
                self.timeComboBox.model().item(last_index).setEnabled(False)

            # Move to next hour
            current_hour += 1

            # If we go past 5:30 PM, break
            if current_hour > end_hour or (current_hour == end_hour and current_minute > end_minute):
                break
    def update_time_slots_availability(self):
        """Update time slots availability when date changes"""
        current_index = self.timeComboBox.currentIndex()
        current_data = self.timeComboBox.currentData() if current_index >= 0 else None

        self.setup_time_combo_box()

        # Try to restore previous selection if still available
        if current_data:
            index = self.timeComboBox.findData(current_data)
            if index >= 0 and self.timeComboBox.model().item(index).isEnabled():
                self.timeComboBox.setCurrentIndex(index)
    def setup_comboboxes(self):
        self.selectPetPopUp, self.selectPatientPopUp
        self.load_patients_to_combobox()
        combo_boxes = [self.selectPatientPopUp,self.selectPetPopUp,self.serviceTypeComboBox]
        placeholders = ["Select Patient", "Select Pet","Select Service Type"]
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

        # Get time from combo box
        time_index = self.timeComboBox.currentIndex()
        time = self.timeComboBox.itemData(time_index) if time_index >= 0 else ""

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

        # Additional validation: Check if the selected time slot is available
        if not self.is_time_slot_available(date, time):
            toast = Toast(self.main_window, "This time slot is already fully booked! Please choose another time.",
                          icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # build data - USE THE NEW FIELD NAMES
        appointment_data = {
            "owner_id": patient_id,
            "pet_id": pet_id,
            "date": date,
            "prefTime": time,
            "service_name": service_name,
            "request": "accepted"
        }


        # send data to backend
        if add_new_appointment(appointment_data):
            toast = Toast(self.main_window, "Appointment added!", icon_path="Icons/check.png")
            toast.show_toast()
            self.close()
            self.serviceTypeComboBox.setCurrentIndex(-1)
            self.timeComboBox.setCurrentIndex(-1)  # Reset time combo box
            self.load_appointments(1, "pending", search_term=None)
        else:
            toast = Toast(self.main_window, "Failed to add appointment!", icon_path="Icons/warning.png")
            toast.show_toast()
    def is_time_slot_available(self, date, time):
        """Check if the selected time slot has available appointments (max 4 ACCEPTED per slot)"""
        try:
            # Use API call instead of direct import
            url = "http://127.0.0.1:8000/api/check-time-slot/"
            params = {
                'date': date,
                'time': time
            }

            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return data.get('available', True)
            else:
                print(f"API error: {response.status_code}")
                return True  # Default to available if API fails

        except Exception as e:
            print(f"Error checking time slot availability: {e}")
            return True  # Default to available if there's an error

    #LOADING WALK IN APPOINTMENTS AND CARD LOGIC
    def setup_status_filters(self):
        """Connect status buttons to filter appointments"""
        status_buttons = {
            "pending": self.main_window.pendingBtn,
            "completed": self.main_window.completedBtn,
            "overdue": self.main_window.overdueBtn,
            "cancelled": self.main_window.cancelledBtn
        }

        for status, button in status_buttons.items():
            button.clicked.connect(lambda checked, s=status: self.load_appointments(1, s,search_term=None))
    def setup_search(self):
        """Setup search functionality for appointments"""
        # Connect search bar to search handler
        self.main_window.searchBar_2.textEdited.connect(self.handle_appointment_search_input)

        # Setup search timer for debouncing
        self._appointment_search_timer = QTimer()
        self._appointment_search_timer.setSingleShot(True)
        self._appointment_search_timer.timeout.connect(self.perform_appointment_search)

        # Search state variables
        self.current_appointment_search_term = ""
        self.is_appointment_searching = False
    def handle_appointment_search_input(self, text):
        """Handle search input with debouncing"""
        self.current_appointment_search_term = text.strip()
        self._appointment_search_timer.start(500)
    def perform_appointment_search(self):
        """Perform the actual search"""
        if self.current_appointment_search_term:
            self.is_appointment_searching = True
            self.load_appointments(1, self.status_filter_global, self.current_appointment_search_term)
        else:
            # If search is empty, load normal appointment list
            self.is_appointment_searching = False
            self.load_appointments(1, self.status_filter_global)
    def load_appointments(self, page=1, status_filter="pending", search_term=None):
        """Updated load_appointments with search support"""
        try:
            self.status_filter_global = status_filter
            current_layout = self.get_layout_for_status(status_filter)

            # Build API URL with search term
            url = f"http://127.0.0.1:8000/api/walkIn/?request=accepted&page={page}"
            if status_filter:
                url += f"&status={status_filter}"
            if search_term:
                import urllib.parse
                encoded_term = urllib.parse.quote(search_term.strip())
                url += f"&search={encoded_term}"

            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to load appointments: {response.status_code}")
                if current_layout:
                    self.card_manager.show_empty_state(current_layout)
                return

            data = response.json()

            # Handle paginated response
            if isinstance(data, dict) and 'results' in data:
                appointments = data.get('results', [])
                total_pages = data.get('total_pages', 1)
                total_count = data.get('count', 0)
                current_page = data.get('current_page', page)
            else:
                appointments = data or []
                total_pages = 1
                total_count = len(appointments)
                current_page = page

            # Update card_manager pagination state
            self.card_manager.current_appointment_page = current_page
            self.card_manager.total_appointment_pages = max(1, total_pages)
            self.card_manager.total_appointment_count = total_count
            self.card_manager.current_status_filter = status_filter
            self.card_manager.current_search_term = search_term

            # Clear current layout
            if current_layout:
                while current_layout.count():
                    child = current_layout.takeAt(0)
                    if child and child.widget():
                        child.widget().deleteLater()

            # Create UI cards
            self.distribute_appointment_cards(appointments, target_layout=current_layout)

            # Add pagination controls
            if current_layout and self.card_manager.total_appointment_pages > 1:
                self.card_manager.add_appointment_pagination_controls(current_layout, status_filter, search_term)
            else:
                # Remove any leftover pagination widget
                try:
                    if hasattr(self.card_manager, 'appointment_pagination_widget'):
                        self.card_manager.appointment_pagination_widget.deleteLater()
                except Exception:
                    pass
        except Exception as e:
            print(f"Error loading appointments: {e}")
            current_layout = self.get_layout_for_status(status_filter)
            if current_layout:
                self.card_manager.show_empty_state(current_layout, "Error loading appointments")
    def distribute_appointment_cards(self, appointments, target_layout=None):
        """Add appointment cards to a single target layout (the active status layout)."""
        if target_layout is None:
            target_layout = self.get_layout_for_status(None)  # default to pending layout


        created_any = False
        for appointment in appointments:
            card = self.card_manager.create_appointment_card(appointment)
            target_layout.addWidget(card)
            self.card_manager.appointment_cards.append(card)
            created_any = True

        if not created_any:
            self.card_manager.show_empty_state(target_layout)
    def get_layout_for_status(self, status_filter):
        """Return the Qt layout corresponding to the given status_filter."""
        map_ = {
            "pending": self.pendingLayout,
            "completed": self.completedLayout,
            "overdue": self.overdueLayout,
            "cancelled": self.cancelledLayout,
            None: self.pendingLayout  # default
        }

        layout = map_.get(status_filter, self.pendingLayout)



        return layout
    def open_pet_from_appointment(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/")
        if response.status_code == 200:
            pet = response.json()

            # Extract both IDs
            self.main_window.selected_pet_id = pet["id"]
            self.main_window.selected_patient_id = pet["owner"]["id"]

            # Open pet profile with full data
            self.main_window.show_pet_profile(pet)
        else:
            print(f"Failed to fetch pet {pet_id}: {response.status_code}")
    def cancelled_appointment(self, appointment_id):
        self.main_window.confirmCard.confirmationMessage.setText(
            "Are you sure you want to cancel \nthis appointment?"
        )
        self.main_window.confirmCard.show_card()

        def clicked_yes():
            # First get the appointment details to know which time slot to free up
            try:
                appointment_url = f"http://127.0.0.1:8000/api/walkIn/{appointment_id}/"
                appointment_response = requests.get(appointment_url)

                if appointment_response.status_code == 200:
                    appointment_data = appointment_response.json()
                    # Store the date and time before cancelling
                    date = appointment_data.get('date')
                    time = appointment_data.get('prefTime')

                    # Now cancel the appointment
                    url = f"http://127.0.0.1:8000/api/walkIn/{appointment_id}/"
                    response = requests.patch(url, json={"status": "cancelled", "request": "accepted"})

                    if response.status_code in [200, 202]:
                        print("Appointment cancelled - time slot freed up")
                        toast = Toast(self.main_window, "Appointment cancelled! Time slot is now available.",
                                      icon_path="Icons/check.png")
                        toast.show_toast()
                        self.load_appointments(1, self.status_filter_global)

                        # Refresh time slot availability if the add appointment card is open
                        if hasattr(self, 'setup_time_combo_box'):
                            self.setup_time_combo_box()
                    else:
                        print("Failed:", response.text)
                        toast = Toast(self.main_window, "Failed to cancel appointment!", icon_path="Icons/warning.png")
                        toast.show_toast()
                else:
                    print("Failed to fetch appointment details")
            except Exception as e:
                print(f"Error cancelling appointment: {e}")
                toast = Toast(self.main_window, "Error cancelling appointment!", icon_path="Icons/warning.png")
                toast.show_toast()

            self.main_window.confirmCard.hide()

        def clicked_no():
            self.main_window.confirmCard.hide()

        # Disconnect any previous connections first
        try:
            self.main_window.confirmCard.yesButton.clicked.disconnect()
        except TypeError:
            pass
        try:
            self.main_window.confirmCard.noButton.clicked.disconnect()
        except TypeError:
            pass

        # Reconnect safely
        self.main_window.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.main_window.confirmCard.noButton.clicked.connect(clicked_no)


    #-------------------------------------------WEB APPOINTMENT---------------------------------------

    def web_Appointment(self):
        # Fetch all walk-in appointments with different request statuses
        pending_response = requests.get("http://127.0.0.1:8000/api/walkIn/?request=pending")
        accepted_response = requests.get("http://127.0.0.1:8000/api/walkIn/?request=accepted")
        declined_response = requests.get("http://127.0.0.1:8000/api/walkIn/?request=declined")

        # Helper function to safely extract data
        def get_appointments(response):
            if response.status_code == 200:
                data = response.json()
                # Handle paginated response
                if isinstance(data, dict) and 'results' in data:
                    return data['results']
                else:
                    return data
            return []

        pending_appointments = get_appointments(pending_response)
        accepted_appointments = get_appointments(accepted_response)
        declined_appointments = get_appointments(declined_response)

        # Clear all layouts first
        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Process pending appointments
        for appoint in pending_appointments:
            card = self.create_walkin_card(appoint)
            if card:
                self.pendingWebLayout.addWidget(card)

        # Process accepted appointments
        for appoint in accepted_appointments:
            card = self.create_walkin_card(appoint)
            if card:
                self.acceptedWebLayout.addWidget(card)

        # Process declined appointments
        for appoint in declined_appointments:
            card = self.create_walkin_card(appoint)
            if card:
                self.declinedWebLayout.addWidget(card)

        # Add empty labels if no appointments
        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            if layout.count() == 0:
                self.add_empty_label(layout)
    def create_walkin_card(self, appoint):
        """Helper method to create a walk-in appointment card"""
        try:
            card = uic.loadUi("ui-files/webAppointmentCard.ui")

            # Get owner and pet information
            owner = appoint.get("owner", {})
            pet = appoint.get("pet", {})

            # Set owner name
            first_name = owner.get("firstName", "").title()
            last_name = owner.get("lastName", "").title()
            owner_name = f"{first_name} {last_name}".strip()
            card.ownerName.setText(owner_name or "Unknown Owner")

            # Format date and time
            date_str = appoint.get("date", "")
            time_str = appoint.get("prefTime", "")
            if time_str:
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M:%S")
                    formatted_time = time_obj.strftime("%I:%M %p").lstrip("0")
                except ValueError:
                    formatted_time = "N/A"
            else:
                formatted_time = "N/A"
            formatted_date = self.main_window.format_date(date_str)
            date_and_time = f"{formatted_date}   {formatted_time}" if formatted_time else formatted_date

            card.DateTime.setText(date_and_time)

            # Add service name if available
            service_name = appoint.get("service_name", "")
            if service_name and service_name != "none":
                # You might want to add a label for service name in your UI
                pass

            card.setGraphicsEffect(create_card_shadow())

            # Connect review button
            card.ReviewButton.clicked.connect(lambda _, a=appoint, date=date_and_time: self.show_review_page(a, date))

            return card
        except Exception as e:
            print(f"Error creating walk-in card: {e}")
            return None
    def show_review_page(self, appoint, date):
        # Owner details - updated for WalkInAppointment structure
        self.main_window.BookingId.setText(appoint.get("booking_id", ""))

        # Get owner and pet information from nested objects
        owner = appoint.get("owner", {})
        pet = appoint.get("pet", {})

        # Owner details
        first_name = owner.get("firstName", "").title()
        last_name = owner.get("lastName", "").title()
        full_name = f"{first_name} {last_name}".strip()
        self.main_window.reviewFullname.setText(full_name)
        contactNumber = f"{owner.get('phoneNumber', '')} / {owner.get('SecondaryNumber', 'NONE')}"
        self.main_window.reviewPhoneNo.setText(contactNumber)
        self.main_window.reviewEmail.setText(owner.get("email", "").lower())

        address = f"{owner.get('barangay', '')}, {owner.get('city', '')}, {owner.get('province', '')}"
        self.main_window.reviewAddress.setText(address.title())
        self.main_window.reviewDetailedAddress.setText(owner.get("detailedAddress", "").title())

        # Pet details
        self.main_window.reviewPetName.setText(pet.get("petName", "").title())
        self.main_window.reviewSpecies.setText(pet.get("species", "").title())
        self.main_window.reviewBreed.setText(pet.get("breed", "").title())
        self.main_window.reviewSex.setText(pet.get("sex", "").title())
        self.main_window.reviewColor.setText(pet.get("petColor", "").title())
        dateTime = date.split(" ",3)
        mdy = " ".join(dateTime[:3])  # 'oct 19, 2025'
        time = dateTime[3]
        # WalkInAppointment specific fields
        self.main_window.reviewDoctor.setText("Walk-in")  # Default for walk-ins
        self.main_window.reviewService.setText(appoint.get("service_name", "").title())
        self.main_window.reviewTime.setText(time)
        self.main_window.reviewDate.setText(mdy)

        self.main_window.navigate_to_page(7)

        # Check request status instead of status
        request_status = appoint.get("request", "pending")
        if request_status == "pending":
            self.main_window.AcceptDeclineFrame.setVisible(True)
        else:
            self.main_window.AcceptDeclineFrame.setVisible(False)

        # Pet icon
        species = pet.get("species", "").lower()
        if species == "dog":
            icon_path = "Icons/dog.png"
        elif species == "cat":
            icon_path = "Icons/catIcon.png"
        else:
            icon_path = "Icons/otherSpecies.png"
        self.main_window.ReviewPetIcon.setPixmap(QPixmap(icon_path))

        # Disconnect previous connections
        try:
            self.main_window.acceptAppointmentBtn.clicked.disconnect()
            self.main_window.declineAppointmentBtn.clicked.disconnect()
        except TypeError:
            pass

        # Connect buttons with walk-in appointment ID
        self.main_window.acceptAppointmentBtn.clicked.connect(
            lambda _, r_id=appoint['id']: self.accepted_booking(r_id, owner.get('id')))
        self.main_window.declineAppointmentBtn.clicked.connect(
            lambda _, r_id=appoint['id']: self.declined_booking(r_id))
    def accepted_booking(self, walkin_id, owner_id):
        # First check if the time slot is still available
        try:
            # Get the appointment details to check date and time
            appointment_url = f"http://127.0.0.1:8000/api/walkIn/{walkin_id}/"
            appointment_response = requests.get(appointment_url)

            if appointment_response.status_code == 200:
                appointment_data = appointment_response.json()
                date = appointment_data.get('date')
                time = appointment_data.get('prefTime')

                # Check if time slot is available
                if not self.is_time_slot_available(date, time):
                    toast = Toast(self.main_window,
                                  "This time slot is already fully booked! Cannot accept this appointment.",
                                  icon_path="Icons/warning.png")
                    toast.show_toast()
                    return  # Don't proceed with acceptance

        except Exception as e:
            print(f"Error checking time slot before acceptance: {e}")
            # Continue anyway if there's an error checking

        # If time slot is available, proceed with acceptance
        url = f"http://127.0.0.1:8000/api/walkIn/{walkin_id}/"

        # First, update the walk-in request status
        response = requests.patch(url, json={"request": "accepted"})

        if response.status_code in [200, 202]:
            # Update basicInfo desktop_record to 'show' if owner_id is provided
            if owner_id:
                owner_url = f"http://127.0.0.1:8000/api/patients/{owner_id}/"
                # Get current owner data first
                owner_response = requests.get(owner_url)
                if owner_response.status_code == 200:
                    owner_data = owner_response.json()
                    # Only update if current desktop_record is 'hide'
                    if owner_data.get('desktop_record') == 'hide':
                        update_response = requests.patch(owner_url, json={"desktop_record": "show"})
                        print(f"Updated desktop_record to show: {update_response.status_code}")

            # Refresh the appointments and navigate
            self.web_Appointment()
            self.main_window.navigate_to_page(3)
            self.main_window.walkInOrWeb.setCurrentIndex(1)
            self.load_appointments()
            self.main_window.statusStackedWidget.setCurrentIndex(0)
            self.main_window.pendingBtn.setChecked(True)
            self.main_window.walkInBtn.setChecked(True)
            self.main_window.load_patients(1, None)

            toast = Toast(self.main_window, "Appointment accepted successfully!", icon_path="Icons/check.png")
            toast.show_toast()
        else:
            print("Failed to accept walk-in:", response.text)
            toast = Toast(self.main_window, "Failed to accept appointment!", icon_path="Icons/warning.png")
            toast.show_toast()
    def declined_booking(self, walkin_id):
        # Update the walk-in appointment request to 'declined'
        url = f"http://127.0.0.1:8000/api/walkIn/{walkin_id}/"

        response = requests.patch(url, json={"request": "declined"})

        if response.status_code in [200, 202]:
            # For declined bookings, desktop_record remains unchanged
            self.web_Appointment()
            self.main_window.navigate_to_page(3)
            self.main_window.walkInOrWeb.setCurrentIndex(0)
            self.main_window.webAppointmentStackWidget.setCurrentIndex(2)
            self.main_window.DeclinedBtn.setChecked(True)

            # Refresh time slot availability
            if hasattr(self, 'setup_time_combo_box'):
                self.setup_time_combo_box()

            toast = Toast(self.main_window, "Appointment declined! Time slot is now available.",
                          icon_path="Icons/check.png")
            toast.show_toast()
        else:
            print("Failed to decline walk-in:", response.text)
            toast = Toast(self.main_window, "Failed to decline appointment!", icon_path="Icons/warning.png")
            toast.show_toast()
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

        self._pagination_cooldown = QTimer()
        self._pagination_cooldown.setInterval(300)
        self._pagination_cooldown.setSingleShot(True)
        self._can_paginate = True

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
    def show_empty_state(self, layout, message="No appointments found"):

        empty_label = QLabel(message)
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("""
            font: 81 16pt 'Montserrat ExtraBold';
            color: rgb(168,168,168);
            padding: 60px;
            background: transparent;
        """)
        empty_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addStretch()
        layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    def create_appointment_card(self, appointment):
        """Create and configure an appointment card"""
        card = uic.loadUi("ui-files/appointmentCard.ui")
        status = appointment.get("status", "").lower()
        if status in ["completed", "cancelled"]:
            card.deleteButton.setVisible(False)
        else:
            card.deleteButton.setVisible(True)
        # Set appointment information
        card.ownerName.setText(appointment["owner_full_name"].title())
        card.petNameApp.setText(appointment["petName"].capitalize())
        card.serviceApp.setText(appointment["service_name"].capitalize())
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

        # Connect buttons
        appointment_id = appointment["id"]
        pet_id = appointment["pet"]["id"]
        card.deleteButton.clicked.connect(lambda _, a_id=appointment_id: self.appointment_card.cancelled_appointment(a_id))
        card.mousePressEvent = lambda event, pid=pet_id: self.appointment_card.open_pet_from_appointment(pid)
        card.setGraphicsEffect(create_card_shadow())
        return card

    def add_appointment_pagination_controls(self, layout, status_filter=None, search_term=None):
        """Add pagination controls for appointments with search support"""
        # Safely remove existing pagination widget
        if hasattr(self, 'appointment_pagination_widget'):
            try:
                if self.appointment_pagination_widget and self.appointment_pagination_widget.isWidgetType():
                    self.appointment_pagination_widget.deleteLater()
            except RuntimeError:
                pass
            finally:
                if hasattr(self, 'appointment_pagination_widget'):
                    delattr(self, 'appointment_pagination_widget')

        if self.total_appointment_pages <= 1:
            return

        try:
            self.appointment_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

            # Connect prev/next buttons with status filter and search term
            self.appointment_pagination_widget.PrevPage.clicked.connect(
                partial(self.safe_paginate, self.current_appointment_page - 1, status_filter, search_term)
            )
            self.appointment_pagination_widget.NextPage.clicked.connect(
                partial(self.safe_paginate, self.current_appointment_page + 1, status_filter, search_term)
            )

            # Set button states
            self.appointment_pagination_widget.PrevPage.setEnabled(self.current_appointment_page > 1)
            self.appointment_pagination_widget.NextPage.setEnabled(
                self.current_appointment_page < self.total_appointment_pages)

            # Create page buttons with status filter and search support
            self.create_appointment_page_buttons(status_filter, search_term)

            self.appointment_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())
            layout.addWidget(self.appointment_pagination_widget)

        except Exception as e:
            print(f"Error creating appointment pagination: {e}")

    def create_appointment_page_buttons(self, status_filter=None, search_term=None):
        """Create page buttons for appointment pagination with search support"""
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

            # Dynamically resize button width based on text length
            btn_width = 40 + (len(str(page)) - 1) * 8
            page_btn.setFixedSize(btn_width, 40)
            font = page_btn.font()
            font.setPointSize(10)
            font.setBold(True)
            page_btn.setFont(font)

            if page == current_page:
                page_btn.setStyleSheet(current_pageBtn)
            else:
                page_btn.setStyleSheet(other_pageBtn)
                # Pass status filter AND search term when loading different pages
                page_btn.clicked.connect(partial(self.safe_paginate, page, status_filter, search_term))

            page_layout.addWidget(page_btn)

    def safe_paginate(self, page, status_filter, search_term):
        """Prevent spamming pagination clicks with search support."""
        if not self._can_paginate:
            print("[DEBUG] Pagination ignored (cooldown active)")
            return

        self._can_paginate = False
        self._pagination_cooldown.start()
        self._pagination_cooldown.timeout.connect(lambda: setattr(self, "_can_paginate", True))

        # Trigger actual loading with search term
        self.appointment_card.load_appointments(page, status_filter, search_term)


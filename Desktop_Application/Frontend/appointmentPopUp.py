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
from PyQt6.QtWidgets import QWidget, QCompleter, QLabel, QComboBox, QPushButton, QSizePolicy, QVBoxLayout, QScrollArea, \
    QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate,QTimer,QThread, pyqtSignal
from input_styles import *
from  shadowEffects import *
from toast import Toast
from Desktop_Application.Frontend.api_client import add_new_appointment
from datetime import datetime
from loading_overlay import LoadingOverlay
from functools import partial
from config_loader import API_BASE_URL
from async_helper import AsyncHelper
import requests


class _TimeSlotDetailsBatchWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, base_url: str, date_str: str, time_values: list[str]):
        super().__init__()
        self.base_url = base_url
        self.date_str = date_str
        self.time_values = time_values

    def run(self):
        try:
            results: dict[str, dict] = {}
            url = f"{self.base_url}/api/check-time-slot/"
            for t in self.time_values:
                try:
                    resp = requests.get(url, params={'date': self.date_str, 'time': t}, timeout=5)
                    if resp.status_code == 200:
                        results[t] = resp.json()
                    else:
                        results[t] = {'available': True, 'is_past': False, 'is_full': False}
                except Exception:
                    results[t] = {'available': True, 'is_past': False, 'is_full': False}

            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class AddAppointmentCard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/addAppointmentCard.ui", self)
        self.card_manager = AppointmentCardManager(self)
        self.scheduled_card_manager = ScheduledServiceCardManager(self.main_window)
        
        # Initialize async helper for non-blocking API calls
        self.api = AsyncHelper(self, base_url=API_BASE_URL)

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

        # load data - deferred to not block initialization
        # Don't load appointments here - will be loaded when navigating to page
        self.setup_status_filters()
        # Don't load web appointments here - will be loaded when clicking website tab
        self.status_filter_global = "pending"
        self.main_window.websiteBtn.clicked.connect(lambda: QTimer.singleShot(0, lambda: self.web_Appointment(1, "pending")))
        self.main_window.reminderbtns.setVisible(False)
        self.main_window.appointmentBtn.clicked.connect(lambda: QTimer.singleShot(0, lambda: self.web_Appointment(1, "pending")))
        self.setup_search()

        self.setup_time_combo_box()
        # Connect date change signal to update time slots
        self.popUpDateEdit.dateChanged.connect(self.update_time_slots_availability)
        if parent:
            parent.installEventFilter(self)

        self.setup_reminder_controls()

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
        # Don't load appointments here - already loaded when navigating to page
    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)

    #SET UP COMBO BOXES AND DATA SUBMITTING
    def load_service_types_to_combobox(self):
        """Load ALL service types for the combobox - returns IDs not names - async"""
        # Don't block UI - load async
        self.api.get(
            url="/api/service-types/?is_active=true&no_pagination=true",
            on_success=self._on_service_types_combobox_loaded,
            on_error=lambda error: self._on_service_types_combobox_error(error)
        )
    
    def _on_service_types_combobox_loaded(self, data):
        """Callback when service types data is loaded"""
        # Handle both response formats
        if isinstance(data, list):
            service_types = data
        elif isinstance(data, dict) and 'results' in data:
            service_types = data['results']
        else:
            service_types = []

        self.serviceTypeComboBox.clear()
        self.serviceTypeComboBox.addItem("Select Service Type", None)

        for service_type in service_types:
            if service_type.get('is_active', True):
                name = service_type.get('name', '')
                service_id = service_type.get('id')
                if name and service_id:
                    # Store ID as data, name as display text
                    self.serviceTypeComboBox.addItem(name, service_id)

        if self.serviceTypeComboBox.count() == 1:
            self.serviceTypeComboBox.addItem("No service types available", None)
    
    def _on_service_types_combobox_error(self, error):
        """Callback when service types loading fails"""
        print(f"Error loading service types: {error}")
        self.serviceTypeComboBox.clear()
        self.serviceTypeComboBox.addItem("Select Service Type", None)
        self.serviceTypeComboBox.addItem("Error loading services", None)
    def load_patients_to_combobox(self):
        """Load ALL patients for the combobox without pagination - async"""
        # Don't block UI - load async
        self.api.get(
            url="/api/patient-combobox-data/",
            on_success=self._on_patients_combobox_loaded,
            on_error=lambda error: print(f"Error loading patients for combobox: {error}")
        )
    
    def _on_patients_combobox_loaded(self, patients):
        """Callback when patients data is loaded"""
        self.selectPatientPopUp.clear()
        self.selectPatientPopUp.addItem("", None)

        for patient in patients:
            self.selectPatientPopUp.addItem(patient['full_name'], patient['id'])

        self.set_dynamic_completer(self.selectPatientPopUp)
    def on_patient_selected(self, index):
        patient_id = self.selectPatientPopUp.itemData(index)
        if not patient_id:
            self.selectPetPopUp.clear()
            self.selectPetPopUp.addItem("", None)
            return

        # Non-blocking load; also handle paginated/error dict responses safely.
        self.selectPetPopUp.clear()
        self.selectPetPopUp.addItem("", None)

        self.api.get(
            url="/api/pets/",
            params={"owner_id": patient_id},
            on_success=self._on_pets_for_patient_loaded,
            on_error=lambda err: self._on_pets_for_patient_error(err),
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window,
            loading_title="Loading pets...",
            loading_subtitle="Please wait"
        )

    def _normalize_pets_response(self, data):
        """Return a list of pet dicts from API response."""
        if data is None:
            return []
        if isinstance(data, list):
            return [p for p in data if isinstance(p, dict)]
        if isinstance(data, dict):
            # Common DRF pagination shape
            if isinstance(data.get('results'), list):
                return [p for p in data.get('results') if isinstance(p, dict)]
            # Single object shape
            if 'id' in data and ('petName' in data or 'pet_name' in data):
                return [data]
            # Error shape (e.g., {'detail': '...'}): treat as empty
            return []
        # Unexpected types (e.g., string)
        return []

    def _on_pets_for_patient_loaded(self, data):
        pets = self._normalize_pets_response(data)

        self.selectPetPopUp.clear()
        self.selectPetPopUp.addItem("", None)

        for pet in pets:
            name = pet.get('petName') or pet.get('pet_name') or ""
            pet_id = pet.get('id')
            if name and pet_id is not None:
                self.selectPetPopUp.addItem(name, pet_id)

        self.set_dynamic_completer(self.selectPetPopUp)

    def _on_pets_for_patient_error(self, err):
        print(f"Failed to load pets: {err}")
        self.selectPetPopUp.clear()
        self.selectPetPopUp.addItem("", None)
    def on_date_field_clicked(self, dateEdit):
        if self.main_window:
            self.main_window.show_custom_calendar(dateEdit)
    def setup_time_combo_box(self, slot_details_map=None):
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

            # Get detailed availability information
            if isinstance(slot_details_map, dict) and time_value in slot_details_map:
                slot_details = slot_details_map.get(time_value) or {}
            else:
                slot_details = self.get_time_slot_details(selected_date, time_value)
            is_available = slot_details.get('available', True)
            is_past = slot_details.get('is_past', False)
            is_full = slot_details.get('is_full', False)

            if is_past:
                # Show past slots as disabled with "PASSED"
                self.timeComboBox.addItem(f"{time_display} (TIME PASSED)", time_value)
                last_index = self.timeComboBox.count() - 1
                self.timeComboBox.model().item(last_index).setEnabled(False)
            elif not is_available and is_full:
                # Show full slots as disabled with "FULL"
                self.timeComboBox.addItem(f"{time_display} (FULL)", time_value)
                last_index = self.timeComboBox.count() - 1
                self.timeComboBox.model().item(last_index).setEnabled(False)
            else:
                # Show available slots
                self.timeComboBox.addItem(time_display, time_value)

            # Move to next hour
            current_hour += 1

            # If we go past 5:30 PM, break
            if current_hour > end_hour or (current_hour == end_hour and current_minute > end_minute):
                break

    def refresh_time_combo_box_async(self):
        """Refresh time slots without blocking the UI (batch fetch in a worker thread)."""
        try:
            selected_date = self.popUpDateEdit.date().toString("yyyy-MM-dd")

            # Generate the same time_value list we use in setup_time_combo_box
            time_values: list[str] = []
            start_hour = 9
            start_minute = 30
            end_hour = 17
            end_minute = 30
            current_hour = start_hour
            current_minute = start_minute

            while current_hour < end_hour or (current_hour == end_hour and current_minute <= end_minute):
                time_values.append(f"{current_hour:02d}:{current_minute:02d}:00")
                current_hour += 1
                if current_hour > end_hour or (current_hour == end_hour and current_minute > end_minute):
                    break

            # Show loading overlay while fetching all slots
            self._time_refresh_overlay = LoadingOverlay(self.main_window)
            self._time_refresh_overlay.set_message(
                "Updating time slots...",
                "Checking availability"
            )
            self._time_refresh_overlay.show()

            worker = _TimeSlotDetailsBatchWorker(API_BASE_URL, selected_date, time_values)

            def _done(slot_map):
                try:
                    if hasattr(self, '_time_refresh_overlay') and self._time_refresh_overlay:
                        self._time_refresh_overlay.close()
                        self._time_refresh_overlay = None
                    self.setup_time_combo_box(slot_details_map=slot_map)
                except Exception as e:
                    print(f"Failed to apply time slot refresh: {e}")

            def _err(msg):
                try:
                    if hasattr(self, '_time_refresh_overlay') and self._time_refresh_overlay:
                        self._time_refresh_overlay.close()
                        self._time_refresh_overlay = None
                except Exception:
                    pass
                print(f"Time slot refresh failed: {msg}")
                # Fallback to old method (may block, but at least user can proceed)
                QTimer.singleShot(0, self.setup_time_combo_box)

            worker.finished.connect(_done)
            worker.error.connect(_err)

            # Keep a reference so it doesn't get GC'd
            self._time_refresh_worker = worker
            worker.start()

        except Exception as e:
            print(f"Error starting time slot refresh: {e}")
            QTimer.singleShot(0, self.setup_time_combo_box)
    def get_time_slot_details(self, date, time):
        """Get detailed information about time slot availability"""
        try:
            url = f"{API_BASE_URL}/api/check-time-slot/"
            params = {
                'date': date,
                'time': time
            }

            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                return {'available': True, 'is_past': False, 'is_full': False}

        except Exception as e:
            print(f"Error getting time slot details: {e}")
            return {'available': True, 'is_past': False, 'is_full': False}
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

        self.serviceTypeComboBox.setEditable(False)
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

        # CHANGED: Get service_type_id (not service_name)
        service_index = self.serviceTypeComboBox.currentIndex()
        service_type_id = self.serviceTypeComboBox.itemData(service_index)

        # Debug prints
        print(f"DEBUG: Service index: {service_index}")
        print(f"DEBUG: Service type ID: {service_type_id}")
        print(f"DEBUG: Service text: {self.serviceTypeComboBox.currentText()}")

        # basic validation - UPDATED for service_type_id
        missing = []
        if not patient_id:
            missing.append("Patient")
        if not date:
            missing.append("Date")
        if not time:
            missing.append("Time")
        if not service_type_id:  # CHANGED: Check for ID, not name
            missing.append("Service")

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self.main_window, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        slot_details = self.get_time_slot_details(date, time)

        if not slot_details.get('available', True):
            if slot_details.get('is_past', False):
                toast = Toast(self.main_window, "This time slot has already passed! Please choose a future time.",
                              icon_path="Icons/warning.png")
            else:
                toast = Toast(self.main_window, "This time slot is already fully booked! Please choose another time.",
                              icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # build data - CHANGED: Use service_type_id instead of service_name
        appointment_data = {
            "owner_id": patient_id,
            "pet_id": pet_id,
            "date": date,
            "prefTime": time,
            "service_type_id": service_type_id,  # CHANGED: Send ID, not name
            "request": "accepted"
        }

        print(f"DEBUG: Sending appointment data: {appointment_data}")

        # Show loading overlay
        self.appointment_loading_overlay = LoadingOverlay(self.main_window)
        self.appointment_loading_overlay.set_message(
            "Adding Appointment...",
            "Please wait while we save the appointment"
        )
        self.appointment_loading_overlay.show()

        # Use async helper for non-blocking POST request
        self.api.post(
            url="/api/walkIn/",
            data=appointment_data,
            on_success=self._on_appointment_added,
            on_error=self._on_appointment_error
        )

    def _on_appointment_added(self, response):
        """Callback when appointment is successfully added"""
        # Hide loading overlay
        if hasattr(self, 'appointment_loading_overlay') and self.appointment_loading_overlay:
            self.appointment_loading_overlay.close()
            self.appointment_loading_overlay = None

        toast = Toast(self.main_window, "Appointment added!", icon_path="Icons/check.png")
        toast.show_toast()
        self.refresh_appointments_safely()
        self.close()
        self.update_time_slots_availability()
        self.serviceTypeComboBox.setCurrentIndex(-1)
        self.timeComboBox.setCurrentIndex(-1)  # Reset time combo box
        self.load_appointments(1, "pending", search_term=None)

    def _on_appointment_error(self, error_msg):
        """Callback when appointment addition fails"""
        # Hide loading overlay
        if hasattr(self, 'appointment_loading_overlay') and self.appointment_loading_overlay:
            self.appointment_loading_overlay.close()
            self.appointment_loading_overlay = None

        toast = Toast(self.main_window, "Failed to add appointment!", icon_path="Icons/warning.png")
        toast.show_toast()
    def is_time_slot_available(self, date, time):
        """Check if the selected time slot has available appointments (max 4 ACCEPTED per slot)"""
        try:
            # Use API call instead of direct import
            url = f"{API_BASE_URL}/api/check-time-slot/"
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
        """Updated load_appointments with search support - ASYNC"""
        self.status_filter_global = status_filter
        current_layout = self.get_layout_for_status(status_filter)
        
        # Show loading label immediately
        if current_layout:
            self.show_loading_label(current_layout, "Loading appointments...")
        
        # Build API URL
        url = f"/api/walkIn/?request=accepted&page={page}"
        if status_filter:
            url += f"&status={status_filter}"
        if search_term:
            import urllib.parse
            encoded_term = urllib.parse.quote(search_term.strip())
            url += f"&search={encoded_term}"

        # Use async API call - non-blocking!
        self.api.get(
            url=url,
            on_success=lambda data: self._on_appointments_loaded(data, page, status_filter, search_term, current_layout),
            on_error=lambda error: self._on_appointments_error(error, status_filter, current_layout),
            timeout=10
        )
    
    def _on_appointments_loaded(self, data, page, status_filter, search_term, current_layout):
        """Callback when appointments data is loaded"""
        try:
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

            if not appointments and page > 1:
                return self.load_appointments(page - 1, status_filter, search_term)

            if hasattr(self.main_window, 'reminderbtns'):
                self.main_window.reminderbtns.setVisible(False)
            
            # Clear the cards list BEFORE clearing layout
            self.card_manager.appointment_cards.clear()

            # Clear current layout
            if current_layout:
                while current_layout.count():
                    child = current_layout.takeAt(0)
                    if child and child.widget():
                        child.widget().deleteLater()

            # Update card_manager pagination state
            self.card_manager.current_appointment_page = current_page
            self.card_manager.total_appointment_pages = max(1, total_pages)
            self.card_manager.total_appointment_count = total_count
            self.card_manager.current_status_filter = status_filter
            self.card_manager.current_search_term = search_term

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
            print(f"Error processing appointments: {e}")
            if current_layout:
                self.card_manager.show_empty_state(current_layout, "Error loading appointments")
    
    def _on_appointments_error(self, error_msg, status_filter, current_layout):
        """Callback when appointments loading fails"""
        print(f"Error loading appointments: {error_msg}")
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
    
    def show_loading_label(self, layout, message="Loading..."):
        """Show a loading label in the given layout"""
        from PyQt6.QtWidgets import QLabel, QSizePolicy
        # Clear existing items
        while layout.count():
            child = layout.takeAt(0)
            if child and child.widget():
                child.widget().deleteLater()
        
        # Create loading label with same styling as empty state
        loading_label = QLabel(message)
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet("""
            font: 81 16pt 'Montserrat ExtraBold';
            color: rgb(168,168,168);
            padding: 60px;
            background: transparent;
        """)
        loading_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        loading_label.setObjectName("loadingLabel")
        
        layout.addStretch()
        layout.addWidget(loading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    
    def open_pet_from_appointment(self, pet_id):
        try:
            # Delegate to main window (cache-first + background refresh)
            self.main_window.open_pet_from_service(pet_id)
        except Exception as e:
            print(f"Failed to open pet {pet_id} from appointment: {e}")
    def cancelled_appointment(self, appointment_id):
        self.main_window.confirmCard.confirmationMessage.setText(
            "Are you sure you want to cancel \nthis appointment?"
        )
        self.main_window.confirmCard.show_card()

        def clicked_yes():
            # Non-blocking cancel with loading modal (prevents UI freeze)
            self.main_window.confirmCard.hide()

            def _on_details_loaded(appointment_data):
                # We don't strictly need these fields to cancel, but keeping this mirrors old behavior.
                try:
                    _ = appointment_data.get('date') if isinstance(appointment_data, dict) else None
                    _ = appointment_data.get('prefTime') if isinstance(appointment_data, dict) else None
                except Exception:
                    pass

                self.api.patch(
                    url=f"/api/walkIn/{appointment_id}/",
                    data={"status": "cancelled", "request": "accepted"},
                    on_success=lambda _: _on_cancelled_saved(),
                    on_error=lambda err: _on_cancel_failed(err),
                    timeout=15,
                    show_loading=True,
                    loading_widget=self.main_window,
                    loading_title="Cancelling appointment...",
                    loading_subtitle="Saving changes"
                )

            def _on_cancelled_saved():
                toast = Toast(
                    self.main_window,
                    "Appointment cancelled! Time slot is now available.",
                    icon_path="Icons/check.png"
                )
                toast.show_toast()
                self.load_appointments(1, self.status_filter_global)
                if hasattr(self, 'refresh_time_combo_box_async'):
                    self.refresh_time_combo_box_async()

            def _on_cancel_failed(err):
                print(f"Failed to cancel appointment: {err}")
                toast = Toast(self.main_window, "Failed to cancel appointment!", icon_path="Icons/warning.png")
                toast.show_toast()

            # Fetch details first (non-blocking) then cancel
            self.api.get(
                url=f"/api/walkIn/{appointment_id}/",
                on_success=_on_details_loaded,
                on_error=lambda err: _on_cancel_failed(err),
                timeout=10,
                show_loading=True,
                loading_widget=self.main_window,
                loading_title="Cancelling appointment...",
                loading_subtitle="Loading appointment"
            )

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
    def setup_reminder_controls(self):
        """Connect reminder control buttons"""
        # Connect buttons from your reminderbtns frame
        self.main_window.selecAllBtn.clicked.connect(self.select_all_appointments)  # Select All
        self.main_window.clearAllBtn.clicked.connect(self.clear_all_appointments)  # Clear All
        self.main_window.sendReminersBtn.clicked.connect(self.send_selected_reminders)  # Send Reminders
    def select_all_appointments(self):
        """Select all visible appointment cards - SAFE VERSION"""
        print(f"DEBUG: select_all_appointments called")
        selected_count = 0

        # Create a new list with only valid cards
        valid_cards = []
        for card in self.card_manager.appointment_cards:
            try:
                # Test if card still exists
                if card and hasattr(card, 'checkBox'):
                    # Try to access a property to see if it's alive
                    _ = card.objectName() or card.checkBox.objectName()
                    valid_cards.append(card)

            except RuntimeError:
                # Card was deleted, skip it
                print(f"DEBUG: Found deleted card, skipping")
                continue
        # ✅ NEW: Update visibility
        self.card_manager.update_reminder_controls_visibility()
        # Update the main list with only valid cards
        self.card_manager.appointment_cards = valid_cards

        # Now select valid cards
        for card in valid_cards:
            try:
                if card.checkBox.isEnabled():
                    card.checkBox.setChecked(True)
                    selected_count += 1
            except RuntimeError:
                # Just in case
                continue

        print(f"DEBUG: Selected {selected_count} cards")
    def clear_all_appointments(self):
        """Deselect all appointment cards"""
        for card in self.card_manager.appointment_cards:
            if hasattr(card, 'checkBox'):
                card.checkBox.setChecked(False)
        # Also clear the tracking list
        self.card_manager.selected_appointment_ids = []
        self.card_manager.update_reminder_controls_visibility()
    def send_selected_reminders(self):
        """Send reminders to selected appointments - using confirmCard"""
        if not self.card_manager.selected_appointment_ids:
            self.show_toast("Please select at least one appointment", "warning")
            return

        count = len(self.card_manager.selected_appointment_ids)

        # Use your existing confirmCard
        self.main_window.confirmCard.confirmationMessage.setText(
            f"Send reminders to {count} selected appointment(s)?\n\n"
            f"This will remind selected patients."
        )
        self.main_window.confirmCard.yesButton.setStyleSheet(reset_yes_style)
        self.main_window.confirmCard.noButton.setStyleSheet(reset_no_style)
        self.main_window.confirmCard.show_card()

        def clicked_yes():
            # Get admin ID
            admin_id = getattr(self.main_window, 'current_admin_id', 1)

            # Prepare data
            data = {
                'admin_id': admin_id,
                'appointment_ids': self.card_manager.selected_appointment_ids,
                'reminder_type': 'manual_batch'
            }

            # Send reminders
            self.send_reminders_simple(data)

            # Hide confirm card
            self.main_window.confirmCard.hide()
            self.main_window.confirmCard.yesButton.setStyleSheet(original_yes_style)
            self.main_window.confirmCard.noButton.setStyleSheet(original_no_style)

        def clicked_no():
            self.main_window.confirmCard.hide()
            self.main_window.confirmCard.yesButton.setStyleSheet(original_yes_style)
            self.main_window.confirmCard.noButton.setStyleSheet(original_no_style)
        # Disconnect previous connections
        try:
            self.main_window.confirmCard.yesButton.clicked.disconnect()
        except TypeError:
            pass
        try:
            self.main_window.confirmCard.noButton.clicked.disconnect()
        except TypeError:
            pass

        # Reconnect
        self.main_window.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.main_window.confirmCard.noButton.clicked.connect(clicked_no)
    def send_reminders_to_backend(self):
        """Call the API to send reminders"""
        try:

            # Get admin ID (you need to track this somewhere)
            admin_id = getattr(self.main_window, 'current_admin_id', 1)

            # Prepare data
            data = {
                'admin_id': admin_id,
                'appointment_ids': self.card_manager.selected_appointment_ids,
                'reminder_type': 'manual_batch'
            }

            # Call API - First let's check if we have the endpoint
            # We'll create a simple version first
            self.send_reminders_simple(data)

        except Exception as e:
            self.show_toast(f"Error: {str(e)}", "error")
            print(f"Error sending reminders: {e}")
    def send_reminders_simple(self, data):
        """Send reminders using worker thread"""
        print(f"DEBUG: Starting thread for {len(data['appointment_ids'])} appointments")

        # Create and show loading overlay
        self.loading_overlay = LoadingOverlay(self.main_window)
        self.loading_overlay.set_message(
            f"Sending {len(data['appointment_ids'])} reminder(s)...",
            "Please wait while we send the emails"
        )
        self.loading_overlay.show()

        # Disable buttons to prevent double-clicking
        self._disable_all_buttons()

        # Create and start worker thread
        self.worker = ReminderWorker(data)
        self.worker.finished.connect(self._on_reminders_finished)
        self.worker.error.connect(self._on_reminders_error)
        self.worker.start()
    def _disable_all_buttons(self):
        """Disable all control buttons"""
        if hasattr(self.main_window, 'sendRemindersBtn'):
            self.main_window.sendRemindersBtn.setEnabled(False)
        if hasattr(self.main_window, 'selecAllBtn'):
            self.main_window.selecAllBtn.setEnabled(False)
        if hasattr(self.main_window, 'clearAllBtn'):
            self.main_window.clearAllBtn.setEnabled(False)
    def _reenable_buttons(self):
        """Re-enable all control buttons"""
        if hasattr(self.main_window, 'sendRemindersBtn'):
            self.main_window.sendRemindersBtn.setEnabled(True)
        if hasattr(self.main_window, 'selecAllBtn'):
            self.main_window.selecAllBtn.setEnabled(True)
        if hasattr(self.main_window, 'clearAllBtn'):
            self.main_window.clearAllBtn.setEnabled(True)
    def _on_reminders_finished(self, successful, failed):
        """Called when worker thread finishes successfully"""
        print(f"DEBUG: Thread finished callback: {successful} successful, {failed} failed")

        # Hide loading overlay
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.close()
            self.loading_overlay = None

        # Re-enable buttons
        self._reenable_buttons()

        # Show result toast
        message = f"Sent {successful} reminder(s)"
        if failed > 0:
            message += f",{failed} failed"

        self.show_toast(message, "success" if successful > 0 else "warning")

        # Clear selection and hide buttons
        self._cleanup_after_sending()
    def _on_reminders_error(self, error_message):
        """Called when worker thread has an error"""
        print(f"DEBUG: Thread error callback: {error_message}")

        # Hide loading overlay
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.close()
            self.loading_overlay = None

        # Re-enable buttons
        self._reenable_buttons()

        # Show error toast
        self.show_toast(f"❌ Error: {error_message}", "error")

        # Still clean up
        self._cleanup_after_sending()
    def _cleanup_after_sending(self):
        """Clean up after sending reminders"""
        print("DEBUG: Cleaning up after sending...")

        # 1. Clear the selection (uncheck all checkboxes)
        self.clear_all_appointments()  # You already have this

        # 2. Hide the reminder buttons frame
        if hasattr(self.main_window, 'reminderbtns'):
            self.main_window.reminderbtns.setVisible(False)

        # 3. Clear the selected IDs list
        if hasattr(self, 'card_manager') and hasattr(self.card_manager, 'selected_appointment_ids'):
            self.card_manager.selected_appointment_ids.clear()
            self.card_manager.persistently_checked_ids.clear()

        # 4. Clean up worker thread (if using threads)
        if hasattr(self, 'worker') and self.worker:
            try:
                self.worker.quit()
                self.worker.wait(1000)  # Wait up to 1 second
                self.worker = None
            except Exception as e:
                print(f"DEBUG: Error cleaning up worker: {e}")

        # 5. Update button visibility (if you have that method)
        if hasattr(self, 'card_manager') and hasattr(self.card_manager, 'update_reminder_controls_visibility'):
            self.card_manager.update_reminder_controls_visibility()

        print("DEBUG: Cleanup complete")
    def show_toast(self, message, type="info"):
        """Show a toast notification"""
        # Use your existing toast system
        icon_map = {
            "success": "Icons/check.png",
            "warning": "Icons/warning.png",
            "error": "Icons/error.png",
            "info": "Icons/info.png"
        }

        toast = Toast(self.main_window, message, icon_path=icon_map.get(type, "Icons/info.png"))
        toast.show_toast()
    def refresh_appointments_safely(self):
        """Safely refresh appointments without memory issues"""
        # Clear all tracked data
        self.card_manager.selected_appointment_ids.clear()

        # Clear any stored handlers
        for card in self.card_manager.appointment_cards:
            try:
                if hasattr(card, '_checkbox_handler'):
                    delattr(card, '_checkbox_handler')
            except:
                pass

        # Clear the cards list
        self.card_manager.appointment_cards.clear()

        # Now load fresh
        self.load_appointments(1, self.status_filter_global)
    #-------------------------------------------WEB REQUEST---------------------------------------

    def web_Appointment(self, page=1, request_filter="pending"):
        """Paginated loader for web appointment requests - ASYNC"""
        # Select layout based on request_filter
        layout_map = {
            "pending": self.pendingWebLayout,
            "accepted": self.acceptedWebLayout,
            "declined": self.declinedWebLayout,
        }
        target_layout = layout_map[request_filter]
        
        # Show loading label immediately
        self.show_loading_label(target_layout, "Loading web appointments...")

        # Build URL
        url = f"/api/walkIn/?request={request_filter}&page={page}"

        # Use async API call - non-blocking!
        self.api.get(
            url=url,
            on_success=lambda data: self._on_web_appointments_loaded(data, page, request_filter, target_layout),
            on_error=lambda error: self._on_web_appointments_error(error, target_layout),
            timeout=10
        )
    
    def _on_web_appointments_loaded(self, data, page, request_filter, target_layout):
        """Callback when web appointments data is loaded"""
        try:
            # Extract pagination
            results = data.get("results", [])
            current_page = data.get("current_page", 1)
            total_pages = data.get("total_pages", 1)
            total_count = data.get("count", 0)

            # Rollback if empty page
            if not results and page > 1:
                return self.web_Appointment(page - 1, request_filter)

            # Clear layout
            while target_layout.count():
                child = target_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Add cards
            for appoint in results:
                card = self.create_walkin_card(appoint)
                if card:
                    target_layout.addWidget(card)

            # If empty
            if not results:
                self.add_empty_label(target_layout)

            # Add pagination controls
            self.add_web_pagination_controls(
                target_layout,
                current_page,
                total_pages,
                request_filter
            )

        except Exception as e:
            print(f"Error processing web appointments: {e}")
            self.add_empty_label(target_layout, "Error loading appointments")
    
    def _on_web_appointments_error(self, error_msg, target_layout):
        """Callback when web appointments loading fails"""
        print(f"Error loading web appointments: {error_msg}")
        # Clear layout and show error
        while target_layout.count():
            child = target_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.add_empty_label(target_layout, "Error loading appointments")
    def add_web_pagination_controls(self, layout, current_page, total_pages, request_filter):
        # Remove old pagination widget
        try:
            if hasattr(self, "web_pagination_widget"):
                self.web_pagination_widget.deleteLater()
        except:
            pass

        if total_pages <= 1:
            return

        # Load pagination UI
        self.web_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

        # Prev / Next
        self.web_pagination_widget.PrevPage.clicked.connect(
            lambda: self.web_Appointment(current_page - 1, request_filter)
        )
        self.web_pagination_widget.NextPage.clicked.connect(
            lambda: self.web_Appointment(current_page + 1, request_filter)
        )

        self.web_pagination_widget.PrevPage.setEnabled(current_page > 1)
        self.web_pagination_widget.NextPage.setEnabled(current_page < total_pages)

        # Page numbers
        page_layout = self.web_pagination_widget.pageButtonsLayout
        while page_layout.count():
            child = page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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

        for p in range(start_page, end_page + 1):
            btn = QPushButton(str(p))
            btn.setFixedSize(40, 40)

            if p == current_page:
                btn.setStyleSheet(current_pageBtn)
            else:
                btn.setStyleSheet(other_pageBtn)
                btn.clicked.connect(lambda _, x=p: self.web_Appointment(x, request_filter))

            page_layout.addWidget(btn)

        layout.addWidget(self.web_pagination_widget)
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
            service_name = appoint.get("service_type_name", "")
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
        self.main_window.reviewService.setText(appoint.get("service_type_name", "").title())
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
        self._set_review_action_busy(True)
        # Non-blocking: fetch appointment details, check slot availability, then accept.
        self.api.get(
            url=f"/api/walkIn/{walkin_id}/",
            on_success=lambda appointment_data: self._on_accept_details_loaded(appointment_data, walkin_id, owner_id),
            on_error=lambda err: self._accept_without_slot_check(walkin_id, owner_id, err),
            timeout=10,
            show_loading=True,
            loading_widget=self.main_window,
            loading_title="Accepting appointment...",
            loading_subtitle="Checking availability"
        )

    def _on_accept_details_loaded(self, appointment_data, walkin_id, owner_id):
        try:
            date = appointment_data.get('date')
            time = appointment_data.get('prefTime')
            if not date or not time:
                # If missing fields, proceed with acceptance (matches previous behavior of being permissive).
                return self._accept_patch(walkin_id, owner_id)

            self.api.get(
                url="/api/check-time-slot/",
                params={'date': date, 'time': time},
                on_success=lambda slot_data: self._on_slot_checked(slot_data, walkin_id, owner_id),
                on_error=lambda err: self._accept_without_slot_check(walkin_id, owner_id, err),
                timeout=10,
                show_loading=True,
                loading_widget=self.main_window,
                loading_title="Accepting appointment...",
                loading_subtitle="Checking time slot"
            )
        except Exception as e:
            print(f"Error preparing slot check: {e}")
            self._accept_patch(walkin_id, owner_id)

    def _on_slot_checked(self, slot_data, walkin_id, owner_id):
        try:
            # API returns {'available': bool, ...}
            if isinstance(slot_data, dict) and not slot_data.get('available', True):
                toast = Toast(
                    self.main_window,
                    "This time slot is already fully booked! Cannot accept this appointment.",
                    icon_path="Icons/warning.png"
                )
                toast.show_toast()
                self._set_review_action_busy(False)
                return
        except Exception as e:
            print(f"Error interpreting slot response: {e}")

        self._accept_patch(walkin_id, owner_id)

    def _accept_without_slot_check(self, walkin_id, owner_id, err):
        # Preserve previous behavior: proceed even if slot check fails.
        print(f"Slot check failed (continuing anyway): {err}")
        self._accept_patch(walkin_id, owner_id)

    def _accept_patch(self, walkin_id, owner_id):
        self.api.patch(
            url=f"/api/walkIn/{walkin_id}/",
            data={"request": "accepted"},
            on_success=lambda _: self._on_accepted_saved(walkin_id, owner_id),
            on_error=lambda err: self._on_accept_failed(err),
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window,
            loading_title="Accepting appointment...",
            loading_subtitle="Saving changes"
        )

    def _on_accepted_saved(self, walkin_id, owner_id):
        # Best-effort update: set desktop_record to 'show' (non-blocking).
        if owner_id:
            self.api.get(
                url=f"/api/patients/{owner_id}/",
                on_success=lambda owner_data: self._maybe_set_desktop_record_show(owner_id, owner_data),
                on_error=lambda err: print(f"Failed to fetch owner before desktop_record update: {err}"),
                timeout=10
            )

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

        # Refresh time slot availability (non-blocking)
        if hasattr(self, 'refresh_time_combo_box_async'):
            self.refresh_time_combo_box_async()

        self._set_review_action_busy(False)

    def _maybe_set_desktop_record_show(self, owner_id, owner_data):
        try:
            if isinstance(owner_data, dict) and owner_data.get('desktop_record') == 'hide':
                self.api.patch(
                    url=f"/api/patients/{owner_id}/",
                    data={"desktop_record": "show"},
                    on_success=lambda _: None,
                    on_error=lambda err: print(f"Failed to update desktop_record: {err}"),
                    timeout=10
                )
        except Exception as e:
            print(f"Error updating desktop_record: {e}")

    def _on_accept_failed(self, err):
        print(f"Failed to accept walk-in: {err}")
        toast = Toast(self.main_window, "Failed to accept appointment!", icon_path="Icons/warning.png")
        toast.show_toast()
        self._set_review_action_busy(False)
    def declined_booking(self, walkin_id):
        self._set_review_action_busy(True)
        # Non-blocking decline
        self.api.patch(
            url=f"/api/walkIn/{walkin_id}/",
            data={"request": "declined"},
            on_success=lambda _: self._on_declined_saved(),
            on_error=lambda err: self._on_decline_failed(err),
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window,
            loading_title="Declining appointment...",
            loading_subtitle="Saving changes"
        )

    def _on_declined_saved(self):
        # For declined bookings, desktop_record remains unchanged
        self.web_Appointment()
        self.main_window.navigate_to_page(3)
        self.main_window.walkInOrWeb.setCurrentIndex(0)
        self.main_window.webAppointmentStackWidget.setCurrentIndex(2)
        self.main_window.DeclinedBtn.setChecked(True)
        self.web_Appointment(1, "declined")

        # Refresh time slot availability
        if hasattr(self, 'refresh_time_combo_box_async'):
            self.refresh_time_combo_box_async()

        toast = Toast(self.main_window, "Appointment declined! Time slot is now available.",
                      icon_path="Icons/check.png")
        toast.show_toast()

        self._set_review_action_busy(False)

    def _on_decline_failed(self, err):
        print(f"Failed to decline walk-in: {err}")
        toast = Toast(self.main_window, "Failed to decline appointment!", icon_path="Icons/warning.png")
        toast.show_toast()
        self._set_review_action_busy(False)

    def _set_review_action_busy(self, busy: bool):
        """Disable accept/decline buttons during async review actions.

        Note: Visual feedback is provided by the loading modal (show_loading=True).
        """
        try:
            accept_btn = getattr(self.main_window, 'acceptAppointmentBtn', None)
            decline_btn = getattr(self.main_window, 'declineAppointmentBtn', None)

            if accept_btn:
                accept_btn.setEnabled(not busy)
            if decline_btn:
                decline_btn.setEnabled(not busy)
        except Exception as e:
            print(f"Failed to set review action busy state: {e}")
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
        self.selected_appointment_ids = []
        self.persistently_checked_ids = []
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
            card.checkBox.setVisible(False)
        else:
            card.deleteButton.setVisible(True)
            card.checkBox.setVisible(True)

        appointment_id = appointment["id"]
        card.appointment_id = appointment_id

        print(f"DEBUG: Creating card for appointment {appointment_id}")
        print(f"DEBUG: Manager instance: {id(self)}")

        # Set appointment information
        card.ownerName.setText(appointment["owner_full_name"].title())
        card.petNameApp.setText(appointment["petName"].capitalize())
        card.serviceApp.setText(appointment["service_type_name"].capitalize())
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

        # Connect delete button
        pet_id = appointment["pet"]["id"]
        card.deleteButton.clicked.connect(
            lambda _, a_id=appointment_id: self.appointment_card.cancelled_appointment(a_id)
        )
        card.mousePressEvent = lambda event, pid=pet_id: self.appointment_card.open_pet_from_appointment(pid)
        card.setGraphicsEffect(create_card_shadow())

        # Connect checkbox - FIXED VERSION
        # Connect checkbox
        if hasattr(card, 'checkBox'):
            print(f"DEBUG: Card has checkbox, connecting...")

            # ✅ RESTORE CHECKED STATE
            if appointment_id in self.persistently_checked_ids:
                card.checkBox.setChecked(True)
                if appointment_id not in self.selected_appointment_ids:
                    self.selected_appointment_ids.append(appointment_id)

            # Create handler
            def on_state_changed(state):
                try:
                    if not card or not hasattr(card, 'checkBox'):
                        return
                    self.handle_checkbox_change(state, appointment_id)
                except RuntimeError:
                    print(f"DEBUG: Card {appointment_id} was deleted")

            card.checkBox.stateChanged.connect(on_state_changed)
            card._checkbox_handler = on_state_changed

        return card

    def handle_checkbox_change(self, state, appointment_id):
        """Handle checkbox selection/deselection"""
        if state == 2:  # Checked
            if appointment_id not in self.selected_appointment_ids:
                self.selected_appointment_ids.append(appointment_id)
            if appointment_id not in self.persistently_checked_ids:
                self.persistently_checked_ids.append(appointment_id)
        else:  # Unchecked
            if appointment_id in self.selected_appointment_ids:
                self.selected_appointment_ids.remove(appointment_id)
            if appointment_id in self.persistently_checked_ids:
                self.persistently_checked_ids.remove(appointment_id)

        self.update_reminder_controls_visibility()
        print(f"Selected IDs: {self.selected_appointment_ids}")
        print(f"Persistent IDs: {self.persistently_checked_ids}")
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

    def update_reminder_controls_visibility(self):
        """Show/hide reminder buttons based on selection"""
        if hasattr(self.appointment_card.main_window, 'reminderbtns'):
            frame = self.appointment_card.main_window.reminderbtns
            should_show = len(self.selected_appointment_ids) > 0

            # Only change if needed (prevents flickering)
            if frame.isVisible() != should_show:
                frame.setVisible(should_show)

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


# In appointmentPopUp.py, update the ReminderWorker class
class ReminderWorker(QThread):
    """Worker thread for sending reminders"""
    finished = pyqtSignal(int, int)  # successful, failed
    error = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        """Run in background thread"""
        successful = 0
        failed = 0

        try:
            # Use batch endpoint
            response = requests.post(
                f"{API_BASE_URL}/api/desktop-manual-reminder/",
                json={
                    'admin_id': self.data['admin_id'],
                    'appointment_ids': self.data['appointment_ids']
                },
                timeout=120  # 2 minutes timeout for sending multiple emails/SMS
            )

            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('success'):
                    # Count successful from results
                    results = response_data.get('results', {})
                    successful = len(results.get('successful', []))
                    failed = len(results.get('failed', []))
                    print(f"DEBUG: Batch result - {successful} successful, {failed} failed")
                else:
                    failed = len(self.data['appointment_ids'])
                    print(f"DEBUG: Batch failed: {response_data.get('message')}")
            else:
                failed = len(self.data['appointment_ids'])
                print(f"DEBUG: API error {response.status_code}: {response.text}")

            print(f"DEBUG: Worker finished: {successful} successful, {failed} failed")
            self.finished.emit(successful, failed)

        except Exception as e:
            print(f"DEBUG: Worker error: {e}")
            self.error.emit(str(e))


class ScheduledServiceCardManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.scheduled_cards = []
        self.selected_service_ids = []
        self.persistently_checked_ids = []

        # Pagination state
        self.current_page = 1
        self.total_pages = 1
        self.total_count = 0
        self.current_filter = "pending"
        self.current_search_term = ""

        # Initialize UI connections
        self.setup_scheduled_reminder_controls()

    def create_scheduled_card(self, service):
        """Create and configure a scheduled service card"""
        try:
            card = uic.loadUi("ui-files/schedCard.ui")

            # Set service information
            owner_name = service.get('owner_full_name', 'Unknown Owner')
            pet_name = service.get('pet_name', 'Unknown Pet')
            service_type = service.get('service_type_name', 'Unknown Service')

            card.ReturnNameLabel.setText(str(owner_name).title())
            card.petName.setText(str(pet_name).capitalize())
            card.ReturnServiceLabel.setText(str(service_type))

            # Format return date
            return_date = service.get("return_date")
            if return_date:
                # Assuming your main_window has a format_date method
                formatted_date = self.main_window.format_date(return_date)
                card.ReturnDateCardLabel.setText(formatted_date)
            else:
                card.ReturnDateCardLabel.setText("No return date")

            # Set graphics effect
            card.setGraphicsEffect(create_card_shadow())

            # Get service ID
            service_id = service.get("id")
            card.service_id = service_id

            # Hide checkbox for completed/cancelled services
            status = service.get("status", "").lower()

            if status in ["completed", "cancelled"]:
                card.checkBox.setVisible(False)
                card.deleteButton.setVisible(True)  # Show delete button for completed/cancelled
                card.deleteButton.setEnabled(True)
                card.deleteButton.setToolTip(f"Delete service {service_id}")
            else:
                card.checkBox.setVisible(True)
                card.deleteButton.setVisible(False)  # Hide delete button for active services

                # ✅ RESTORE CHECKED STATE from persistent list
                if service_id in self.persistently_checked_ids:
                    card.checkBox.setChecked(True)
                    if service_id not in self.selected_service_ids:
                        self.selected_service_ids.append(service_id)

                # Create checkbox handler with proper lambda capture
                def create_checkbox_handler(card_obj, s_id):
                    def handler(state):
                        try:
                            if not card_obj or not hasattr(card_obj, 'checkBox'):
                                return
                            self.handle_scheduled_checkbox_change(state, s_id)
                        except RuntimeError:
                            print(f"DEBUG: Card for service {s_id} was deleted")

                    return handler

                handler = create_checkbox_handler(card, service_id)
                card.checkBox.stateChanged.connect(handler)
                card._checkbox_handler = handler

            # Connect click event to open pet profile
            pet_id = service.get("pet")
            if pet_id:
                # Only allow clicking on the card if not clicking on checkbox
                def mouse_press_handler(event, pid=pet_id):
                    # Check if click was on checkbox or delete button
                    if (hasattr(card, 'checkBox') and card.checkBox.underMouse()) or \
                            (hasattr(card, 'deleteButton') and card.deleteButton.underMouse()):
                        # Let those widgets handle the click
                        event.ignore()
                        return
                    # Otherwise open pet profile
                    self.main_window.open_pet_from_service(pid)

                card.mousePressEvent = mouse_press_handler

            # =========== FIXED DELETE BUTTON CONNECTION ===========
            # Connect delete button using deleteFunction (not delete_handler)
            if hasattr(card, 'deleteButton'):
                print(f"DEBUG: Setting up delete button for service {service_id}")

                # Store service_id on the card object
                card.delete_service_id = service_id

                # Actual delete handler
                def delete_service_handler():
                    current_service_id = card.delete_service_id
                    print(f"DEBUG: Delete handler triggered for service {current_service_id}")

                    # Use deleteFunction (your Delete class instance)
                    if hasattr(self.main_window, 'deleteFunction'):
                        print(f"DEBUG: Using deleteFunction")

                        # First set the selected_service_id in main window
                        self.main_window.selected_service_id = current_service_id
                        print(f"DEBUG: Set selected_service_id to: {self.main_window.selected_service_id}")

                        # Then call the delete method
                        self.main_window.deleteFunction.delete_selected_service()
                        print(f"DEBUG: Called delete_selected_service()")
                    else:
                        print("ERROR: deleteFunction not found on main_window")

                # Connect the delete handler
                card.deleteButton.clicked.connect(delete_service_handler)
            # ======================================================

            # Add to tracking list
            self.scheduled_cards.append(card)

            return card
        except Exception as e:
            print(f"DEBUG: Error in create_scheduled_card: {e}")
            import traceback
            traceback.print_exc()
            # Return a simple label as fallback
            card = QLabel(f"Error: {str(e)[:50]}")
            return card

    def setup_scheduled_reminder_controls(self):
        """Connect scheduled reminder control buttons"""
        if hasattr(self.main_window, 'schedReminderBtnFrame'):
            self.main_window.schedSelectAll.clicked.connect(self.select_all_scheduled)
            self.main_window.schedClearAll.clicked.connect(self.clear_all_scheduled)
            self.main_window.schedSendReminder.clicked.connect(self.send_selected_scheduled_reminders)

            # Hide by default
            self.main_window.schedReminderBtnFrame.setVisible(False)

    def select_all_scheduled(self):
        """Select all visible scheduled service cards"""
        selected_count = 0

        # Create a new list with only valid cards
        valid_cards = []
        for card in self.scheduled_cards:
            try:
                # Test if card still exists
                if card and hasattr(card, 'checkBox'):
                    # Try to access a property to see if it's alive
                    _ = card.objectName() or card.checkBox.objectName()
                    valid_cards.append(card)
            except RuntimeError:
                # Card was deleted, skip it
                continue

        # Update the main list with only valid cards
        self.scheduled_cards = valid_cards

        # Now select valid cards
        for card in valid_cards:
            try:
                if card.checkBox.isEnabled():
                    card.checkBox.setChecked(True)
                    selected_count += 1
            except RuntimeError:
                continue

        # Update visibility
        self.update_scheduled_controls_visibility()
        print(f"DEBUG: Selected {selected_count} scheduled cards")

    def clear_all_scheduled(self):
        """Deselect all scheduled service cards"""
        for card in self.scheduled_cards:
            if hasattr(card, 'checkBox'):
                card.checkBox.setChecked(False)

        # Clear tracking lists
        self.selected_service_ids = []
        self.persistently_checked_ids = []
        self.update_scheduled_controls_visibility()

    def handle_scheduled_checkbox_change(self, state, service_id):
        """Handle checkbox selection/deselection for scheduled services"""
        if state == 2:  # Checked
            if service_id not in self.selected_service_ids:
                self.selected_service_ids.append(service_id)
            if service_id not in self.persistently_checked_ids:
                self.persistently_checked_ids.append(service_id)
        else:  # Unchecked
            if service_id in self.selected_service_ids:
                self.selected_service_ids.remove(service_id)
            if service_id in self.persistently_checked_ids:
                self.persistently_checked_ids.remove(service_id)

        self.update_scheduled_controls_visibility()
        print(f"Selected Service IDs: {self.selected_service_ids}")

    def update_scheduled_controls_visibility(self):
        """Show/hide scheduled reminder buttons based on selection"""
        if hasattr(self.main_window, 'schedReminderBtnFrame'):
            frame = self.main_window.schedReminderBtnFrame
            should_show = len(self.selected_service_ids) > 0

            # Only change if needed (prevents flickering)
            if frame.isVisible() != should_show:
                frame.setVisible(should_show)

    def send_selected_scheduled_reminders(self):
        """Send reminders for selected scheduled services"""
        if not self.selected_service_ids:
            self.show_toast("Please select at least one scheduled service", "warning")
            return

        count = len(self.selected_service_ids)

        # Use confirmCard
        self.main_window.confirmCard.confirmationMessage.setText(
            f"Send reminders for {count} selected scheduled service(s)?\n\n"
            f"This will remind selected patients about their return dates."
        )
        self.main_window.confirmCard.yesButton.setStyleSheet(reset_yes_style)
        self.main_window.confirmCard.noButton.setStyleSheet(reset_no_style)
        self.main_window.confirmCard.show_card()

        def clicked_yes():
            # Get admin ID
            admin_id = getattr(self.main_window, 'current_admin_id', 1)

            # Prepare data
            data = {
                'admin_id': admin_id,
                'service_ids': self.selected_service_ids,
                'reminder_type': 'service_return_batch'
            }

            # Send reminders
            self.send_scheduled_reminders_simple(data)
            self.main_window.confirmCard.hide()
            self.main_window.confirmCard.yesButton.setStyleSheet(original_yes_style)
            self.main_window.confirmCard.noButton.setStyleSheet(original_no_style)

        def clicked_no():
            self.main_window.confirmCard.hide()
            self.main_window.confirmCard.yesButton.setStyleSheet(original_yes_style)
            self.main_window.confirmCard.noButton.setStyleSheet(original_no_style)

        # Disconnect previous connections
        try:
            self.main_window.confirmCard.yesButton.clicked.disconnect()
        except TypeError:
            pass
        try:
            self.main_window.confirmCard.noButton.clicked.disconnect()
        except TypeError:
            pass

        # Reconnect
        self.main_window.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.main_window.confirmCard.noButton.clicked.connect(clicked_no)

    def send_scheduled_reminders_simple(self, data):
        """Send scheduled service reminders using worker thread"""
        print(f"DEBUG: Starting thread for {len(data['service_ids'])} scheduled services")

        # Create and show loading overlay
        self.loading_overlay = LoadingOverlay(self.main_window)
        self.loading_overlay.set_message(
            f"Sending {len(data['service_ids'])} reminder(s)...",
            "Please wait while we send the emails"
        )
        self.loading_overlay.show()

        # Disable buttons
        self._disable_scheduled_buttons()

        # Create and start worker thread
        self.worker = ScheduledReminderWorker(data)
        self.worker.finished.connect(self._on_scheduled_reminders_finished)
        self.worker.error.connect(self._on_scheduled_reminders_error)
        self.worker.start()

    def _disable_scheduled_buttons(self):
        """Disable all scheduled reminder buttons"""
        if hasattr(self.main_window, 'schedSendReminder'):
            self.main_window.schedSendReminder.setEnabled(False)
        if hasattr(self.main_window, 'schedSelectAll'):
            self.main_window.schedSelectAll.setEnabled(False)
        if hasattr(self.main_window, 'schedClearAll'):
            self.main_window.schedClearAll.setEnabled(False)

    def _reenable_scheduled_buttons(self):
        """Re-enable all scheduled reminder buttons"""
        if hasattr(self.main_window, 'schedSendReminder'):
            self.main_window.schedSendReminder.setEnabled(True)
        if hasattr(self.main_window, 'schedSelectAll'):
            self.main_window.schedSelectAll.setEnabled(True)
        if hasattr(self.main_window, 'schedClearAll'):
            self.main_window.schedClearAll.setEnabled(True)

    def _on_scheduled_reminders_finished(self, successful, failed):
        """Called when worker thread finishes successfully"""
        print(f"DEBUG: Scheduled thread finished: {successful} successful, {failed} failed")

        # Hide loading overlay
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.close()
            self.loading_overlay = None

        # Re-enable buttons
        self._reenable_scheduled_buttons()

        # Show result toast
        message = f"Sent {successful} reminder(s)"
        if failed > 0:
            message += f", {failed} failed"

        self.show_toast(message, "success" if successful > 0 else "warning")

        # Clear selection and hide buttons
        self._cleanup_after_scheduled_sending()

    def _on_scheduled_reminders_error(self, error_message):
        """Called when worker thread has an error"""
        print(f"DEBUG: Scheduled thread error: {error_message}")

        # Hide loading overlay
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.close()
            self.loading_overlay = None

        # Re-enable buttons
        self._reenable_scheduled_buttons()

        # Show error toast
        self.show_toast(f"❌ Error: {error_message}", "error")

        # Clean up
        self._cleanup_after_scheduled_sending()

    def _cleanup_after_scheduled_sending(self):
        """Clean up after sending scheduled reminders"""
        print("DEBUG: Cleaning up after sending scheduled reminders...")

        # 1. Clear the selection
        self.clear_all_scheduled()

        # 2. Hide the reminder buttons frame
        if hasattr(self.main_window, 'schedReminderBtnFrame'):
            self.main_window.schedReminderBtnFrame.setVisible(False)

        # 3. Clear the selected IDs list
        self.selected_service_ids.clear()
        self.persistently_checked_ids.clear()

        # 4. Clean up worker thread
        if hasattr(self, 'worker') and self.worker:
            try:
                self.worker.quit()
                self.worker.wait(1000)
                self.worker = None
            except Exception as e:
                print(f"DEBUG: Error cleaning up scheduled worker: {e}")

        # 5. Update button visibility
        self.update_scheduled_controls_visibility()

        print("DEBUG: Scheduled cleanup complete")

    def show_toast(self, message, type="info"):
        """Show a toast notification"""
        icon_map = {
            "success": "Icons/check.png",
            "warning": "Icons/warning.png",
            "error": "Icons/error.png",
            "info": "Icons/info.png"
        }

        toast = Toast(self.main_window, message, icon_path=icon_map.get(type, "Icons/info.png"))
        toast.show_toast()


class ScheduledReminderWorker(QThread):
    """Worker thread for sending scheduled service reminders"""
    finished = pyqtSignal(int, int)  # successful, failed
    error = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        """Run in background thread - for scheduled service reminders"""
        successful = 0
        failed = 0

        try:
            # Use batch endpoint
            response = requests.post(
                f"{API_BASE_URL}/api/desktop-manual-reminder/",
                json={
                    'admin_id': self.data['admin_id'],
                    'service_ids': self.data['service_ids']
                },
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('success'):
                    # Count successful from results
                    results = response_data.get('results', {})
                    successful = len(results.get('successful', []))
                    failed = len(results.get('failed', []))
                    print(f"DEBUG: Batch scheduled result - {successful} successful, {failed} failed")
                else:
                    failed = len(self.data['service_ids'])
                    print(f"DEBUG: Batch scheduled failed: {response_data.get('message')}")
            else:
                failed = len(self.data['service_ids'])
                print(f"DEBUG: API error {response.status_code}: {response.text}")

            print(f"DEBUG: Scheduled worker finished: {successful} successful, {failed} failed")
            self.finished.emit(successful, failed)

        except Exception as e:
            print(f"DEBUG: Scheduled worker error: {e}")
            self.error.emit(str(e))
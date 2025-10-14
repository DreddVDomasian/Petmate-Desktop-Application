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
        uic.loadUi("addAppointmentCard.ui", self)
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
        self.load_appointments(1,"pending")
        self.setup_status_filters()
        self.web_Appointment()
        self.status_filter_global = None
        self.main_window.websiteBtn.clicked.connect(lambda: self.web_Appointment())

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
        self.timeEdit.setGraphicsEffect(create_card_shadow())

        #other Shadows
        self.addPopUPFrame.setGraphicsEffect(create_card_shadow())
        self.cancelAddAppointment.setGraphicsEffect(create_card_shadow())
        self.addAppointmentBtn.setGraphicsEffect(create_card_shadow())

        self.selectPatientPopUp.currentIndexChanged.connect(self.on_patient_selected)

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
        self.load_appointments(1, "pending")
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
            # add notes or other fields if you have
        }

        # send data to backend
        if add_new_appointment(appointment_data):
            toast = Toast(self.main_window, "Appointment added!", icon_path="Icons/check.png")
            toast.show_toast()
            self.close()
            self.serviceTypeComboBox.setCurrentIndex(-1)
            self.load_appointments(1, "pending")
        else:
            toast = Toast(self.main_window, "Failed to add appointment!", icon_path="Icons/warning.png")
            toast.show_toast()

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
            button.clicked.connect(lambda checked, s=status: self.load_appointments(1, s))
    def load_appointments(self, page=1, status_filter="pending"):
        try:

            self.status_filter_global = status_filter
            current_layout = self.get_layout_for_status(status_filter)
            # Build API URL (page + optional status)
            url = f"http://127.0.0.1:8000/api/walkIn/?page={page}"
            if status_filter:
                url += f"&status={status_filter}"

            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to load appointments: {response.status_code}")
                # Show empty state for the active layout
                if current_layout:
                    self.card_manager.show_empty_state(current_layout)
                return

            data = response.json()

            # If backend returned paginated structure, handle it; otherwise treat as list
            if isinstance(data, dict) and 'results' in data:
                appointments = data.get('results', [])
                total_pages = data.get('total_pages', 1)
                total_count = data.get('count', 0)
                current_page = data.get('current_page', page)
            else:
                appointments = data or []
                # No pagination meta from backend -> assume single page
                total_pages = 1
                total_count = len(appointments)
                current_page = page




            # Update card_manager pagination state
            self.card_manager.current_appointment_page = current_page
            self.card_manager.total_appointment_pages = max(1, total_pages)
            self.card_manager.total_appointment_count = total_count
            self.card_manager.current_status_filter = status_filter


            if current_layout:
                while current_layout.count():
                    child = current_layout.takeAt(0)
                    if child and child.widget():
                        child.widget().deleteLater()





            # Create UI cards for the returned appointments and add to the current layout
            self.distribute_appointment_cards(appointments, target_layout=current_layout)

            # Add pagination controls only to the active layout and only if there's more than 1 page
            if current_layout and self.card_manager.total_appointment_pages > 1:
                self.card_manager.add_appointment_pagination_controls(current_layout, status_filter)
            else:
                # ensure any leftover pagination widget for that layout is removed/hidden
                try:
                    if hasattr(self.card_manager, 'appointment_pagination_widget'):
                        self.card_manager.appointment_pagination_widget.deleteLater()
                except Exception:
                    pass

        except Exception as e:
            print(f"Error loading appointments: {e}")
            # show empty state for active layout on error
            current_layout = self.get_layout_for_status(status_filter)
            if current_layout:
                self.card_manager.show_empty_state(current_layout)
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
            url = f"http://127.0.0.1:8000/api/walkIn/{appointment_id}/"
            response = requests.patch(url, json={"status": "cancelled"})
            if response.status_code in [200, 202]:
                print("Reminder marked as cancelled")
                toast = Toast(self.main_window, "Appointment cancelled!", icon_path="Icons/check.png")
                toast.show_toast()
                self.load_appointments(1, self.status_filter_global)
            else:
                print("Failed:", response.text)
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
        response = requests.get("http://127.0.0.1:8000/api/appointments/")
        if response.status_code == 200:
            data = response.json()
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
            card.ownerName.setText(appoint["client_name"].title())
            raw_datetime = appoint.get("appointment_datetime", "")
            # Split into date and time parts
            parts = raw_datetime.split(" ", 1)  # ["2025-09-18", "9:00 AM"]
            date_only = parts[0]
            time_only = parts[1] if len(parts) > 1 else ""
            # Format the date
            formatted_date = self.main_window.format_date(date_only)
            #date + time
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

            card.ReviewButton.clicked.connect(lambda _, a=appoint, date=dateAndTime: self.show_review_page(a,date))



        for layout in [self.pendingWebLayout, self.acceptedWebLayout, self.declinedWebLayout]:
            if layout.count() == 0:
                self.add_empty_label(layout)
    def show_review_page(self, appoint,date):
        #Owner details
        self.main_window.BookingId.setText(appoint["booking_id"])
        self.main_window.reviewFullname.setText(appoint["client_name"].capitalize())
        self.main_window.reviewPhoneNo.setText(appoint["phone"])
        self.main_window.reviewEmail.setText(appoint["email"].capitalize())
        address = f"{appoint['barangay']}, {appoint['city']}, {appoint['province']}"
        self.main_window.reviewAddress.setText(address.capitalize())
        self.main_window.reviewDetailedAddress.setText(appoint["detailed_address"].capitalize())

        #Pet details
        self.main_window.reviewPetName.setText(appoint["pet_name"].capitalize())
        self.main_window.reviewSpecies.setText(appoint["species"].capitalize())
        self.main_window.reviewBreed.setText(appoint["breed"].capitalize())
        self.main_window.reviewSex.setText(appoint["sex"].capitalize())
        self.main_window.reviewColor.setText(appoint["color"].capitalize())
        self.main_window.reviewDoctor.setText(appoint["provider"].capitalize())
        self.main_window.reviewService.setText(appoint["appointment_reason"].capitalize())
        self.main_window.reviewComments.setText(appoint["comments"].capitalize())
        self.main_window.reviewDateTime.setText(date)
        self.main_window.navigate_to_page(7)

        status = appoint.get("status", "pending")
        if status == "pending":
            self.main_window.AcceptDeclineFrame.setVisible(True)
        else:
            self.main_window.AcceptDeclineFrame.setVisible(False)

        species = appoint.get("species", "").lower()
        if species == "dog":
            icon_path = "Icons/dog.png"
        elif species == "cat":
            icon_path = "Icons/catIcon.png"
        else:
            icon_path = "Icons/otherSpecies.png"
        self.main_window.ReviewPetIcon.setPixmap(QPixmap(icon_path))


        try:
            self.main_window.acceptAppointmentBtn.clicked.disconnect()
            self.main_window.declineAppointmentBtn.clicked.disconnect()
        except TypeError:
            pass


        self.main_window.acceptAppointmentBtn.clicked.connect(lambda _, r_id=appoint['id']: self.accepted_booking(r_id))
        self.main_window.declineAppointmentBtn.clicked.connect(lambda _, r_id=appoint['id']: self.declined_booking(r_id))
    def accepted_booking(self, review_id):
        url = f"http://127.0.0.1:8000/api/appointments/{review_id}/statusUpdate/"
        response = requests.patch(url, json={"status": "accepted"})
        if response.status_code in [200, 202]:
            self.web_Appointment()
            self.main_window.navigate_to_page(3)
            self.main_window.walkInOrWeb.setCurrentIndex(1)
            self.main_window.webAppointmentStackWidget.setCurrentIndex(1)
            self.main_window.AcceptedBtn.setChecked(True)
        else:
            print("Failed:", response.text)
    def declined_booking(self, review_id):
        url = f"http://127.0.0.1:8000/api/appointments/{review_id}/statusUpdate/"
        response = requests.patch(url, json={"status": "declined"})
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
        card = uic.loadUi("appointmentCard.ui")
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
        card.deleteButton.clicked.connect(lambda _, a_id=appointment_id: self.appointment_card.cancelled_appointment(a_id))
        card.mousePressEvent = lambda event, pid=appointment["pet"]: self.appointment_card.open_pet_from_appointment(pid)

        card.setGraphicsEffect(create_card_shadow())
        return card
    def add_appointment_pagination_controls(self, layout, status_filter=None):
        """Add pagination controls for appointments"""
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
            self.appointment_pagination_widget = uic.loadUi("paginationUi.ui")

            # Connect prev/next buttons with status filter
            self.appointment_pagination_widget.PrevPage.clicked.connect(
                partial(self.safe_paginate, self.current_appointment_page - 1, status_filter)
            )
            self.appointment_pagination_widget.NextPage.clicked.connect(
                partial(self.safe_paginate, self.current_appointment_page + 1, status_filter)
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
                # Pass status filter when loading different pages
                page_btn.clicked.connect(partial(self.safe_paginate, page, status_filter))

            page_layout.addWidget(page_btn)
    def safe_paginate(self, page, status_filter):
        """Prevent spamming pagination clicks."""
        if not self._can_paginate:
            print("[DEBUG] Pagination ignored (cooldown active)")
            return

        self._can_paginate = False
        self._pagination_cooldown.start()
        self._pagination_cooldown.timeout.connect(lambda: setattr(self, "_can_paginate", True))

        # Trigger actual loading
        self.appointment_card.load_appointments(page, status_filter)


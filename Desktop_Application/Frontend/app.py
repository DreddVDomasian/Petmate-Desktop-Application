import os
import sys

# ETO ANG SAGGOT
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)      # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QWidget, QComboBox, QButtonGroup, QMessageBox, \
    QCalendarWidget, QToolButton, QTextEdit, QPushButton, QFrame, QHBoxLayout
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QSize, \
    QParallelAnimationGroup, QTimer
from PyQt6.QtGui import QFontDatabase, QPixmap
from uiLogic import UIHandler
from input_styles import *
from toast import Toast
import resources_rc
from Desktop_Application.Backend.api_client import add_new_patient, add_new_pet, add_new_service
from confirm_card import ConfirmCard
from ReminderPopUp import ReminderPopup
from appointmentPopUp import AddAppointmentCard
from functools import partial
from datetime import datetime
from shadowEffects import *
from delete import Delete
from duplicateDialog import DuplicateDialog
from updateFunction import Update
import requests
import webbrowser



class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("Home.ui", self)

        # Initialize delete and update functions
        self.deleteFunction = Delete(self)
        self.updateFunction = Update(self)

        # Nav
        self.sideNav.setVisible(False)

        # Setup methods
        self.setup_calendar()
        self.setup_comboboxes()
        self.setup_layouts()
        self.setup_buttons()
        self.setup_service_tab()
        self.setup_dates()
        self.setup_confirm_card()
        self.setup_add_appintmentPopUp()
        self.setup_pet_buttons()

        #CRITICAL: Initialize state variables ONCE
        self.selected_patient_id = None
        self.selected_service_id = None
        self.selected_pet_id = None

        # Initialize pagination state
        self.patient_currentPage = 1
        self.current_patient_page = 1
        self.total_patient_pages = 1
        self.total_patient_count = 0
        self.patient_cards = []  # Initialize empty list

        # Page navigation state
        self.page_history = []
        self.current_page_index = 0
        self.current_params = {}

        # Duplicate dialog state
        self.duplicateDialog = None
        self.ignore_duplicates = False

        # Search state
        self.current_search_term = ""
        self.is_searching = False

        #Pet species comboBox
        self.setup_species_field()

        # Initial page setup
        self.stackedWidget.setCurrentIndex(0)
        self.set_current_month_in_combobox()

        # Load data AFTER all state is initialized
        self.load_patients(1, search_term=None)
        self.load_scheduled_services()

        # Setup remaining UI elements
        self.setup_shadow()
        self.setup_all_back_buttons()
        self.setup_input_shadows()
        self.monthComboBox.currentTextChanged.connect(self.load_scheduled_services)

        # Setup search
        self.setup_search()

        # Update back button visibility
        self.update_back_button_visibility()

        # Birthday date limits
        self.Bday.setMinimumDate(QDate(1900, 1, 1))
        self.Bday.setMaximumDate(QDate.currentDate())

    #LAYOUT FOR SCROLL AREAS FOR CARDS
    def setup_layouts(self):
        # patient list layout
        self.patientListLayout = self.scrollAreaWidgetContents.layout()
        self.patientListLayout.setSpacing(10)
        self.patientListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # service list layout
        self.serviceListLayout = self.serviceHistoryScrollPage.layout()
        self.serviceListLayout.setSpacing(10)
        self.serviceListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # pet cards grid layout
        self.gridLayout_6.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gridLayout_6.addWidget(self.addPetButton, 0, 0)


        #scheduled services
        # Pending Page
        self.pendingLayout = self.pendingScrollPage.layout()
        self.pendingLayout.setSpacing(10)
        self.pendingLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Completed Page
        self.completedLayout = self.completedScrollPage.layout()
        self.completedLayout.setSpacing(10)
        self.completedLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Overdue Page
        self.overdueLayout = self.overdueScrollPage.layout()
        self.overdueLayout.setSpacing(10)
        self.overdueLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    #BUTTONS FUNCTIONS
    def setup_buttons(self):
        # page navigation
        nav = [
            (self.homeBtn, 0), (self.addPatientBtn, 1), (self.petRecordsBtn, 2),
            (self.appointmentBtn, 3), (self.schedVaxBtn, 4)
        ]
        self.navBtnGroup = QButtonGroup(self)
        self.navBtnGroup.setExclusive(True)
        for btn, index in nav:
            btn.setCheckable(True)
            self.navBtnGroup.addButton(btn)
            btn.clicked.connect(lambda _, i=index: self.navigate_to_page(i))

        self.homeBtn.setChecked(True)

        nav_2 = [
            (self.homeBtn_2, 0), (self.addPatientBtn_2, 1), (self.petRecordsBtn_2, 2),
            (self.appointmentBtn_2, 3), (self.schedVaxBtn_2, 4)
        ]
        self.navBtnGroup_2 = QButtonGroup(self)
        self.navBtnGroup_2.setExclusive(True)
        for btn_2, index in nav_2:
            btn_2.setCheckable(True)
            self.navBtnGroup_2.addButton(btn_2)

        self.homeBtn_2.setChecked(True)

        self.page_to_nav_button = {
            0: self.homeBtn,
            1: self.addPatientBtn,
            2: self.petRecordsBtn,
            3: self.appointmentBtn,
            4: self.schedVaxBtn,
            # Profile and Pet Profile pages should highlight Pet Records
            5: self.petRecordsBtn,
            8: self.petRecordsBtn
        }

        # send data
        self.confirmButton.clicked.connect(self.submit_data)
        self.petConfirmButton.clicked.connect(self.submit_pet_data)
        self.addServiceBtn.clicked.connect(self.submit_service_data)


        # add appointment
        for tb in [self.toolButton_2, self.toolButton_3]:
            tb.clicked.connect(lambda: self.open_addAppointment())
        self.addWalkinButton.mousePressEvent = lambda event: self.open_addAppointment()

        # toggle walk-in/website
        self.walkInBtn.setCheckable(True)
        self.websiteBtn.setCheckable(True)
        self.walkInOrWeb.setCurrentIndex(0)
        self.sourceBtnGroup = QButtonGroup(self)
        self.sourceBtnGroup.setExclusive(True)
        for btn in [self.walkInBtn, self.websiteBtn]:
            self.sourceBtnGroup.addButton(btn)
        self.websiteBtn.setChecked(True)
        self.walkInBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(1))
        self.websiteBtn.clicked.connect(lambda: self.walkInOrWeb.setCurrentIndex(0))

        # toggle walk-in status Btn
        self.pendingBtn.setCheckable(True)
        self.completedBtn.setCheckable(True)
        self.overdueBtn.setCheckable(True)
        self.cancelledBtn.setCheckable(True)
        self.statusStackedWidget.setCurrentIndex(0)
        self.statusBtnGroup = QButtonGroup(self)
        for btn in [self.pendingBtn, self.completedBtn, self.overdueBtn,self.cancelledBtn]:
            self.statusBtnGroup.addButton(btn)
        self.pendingBtn.setChecked(True)
        self.pendingBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(0))
        self.completedBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(1))
        self.overdueBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(2))
        self.cancelledBtn.clicked.connect(lambda: self.statusStackedWidget.setCurrentIndex(3))

        #Web Appointment status BTN
        self.pendingWebBtn.setCheckable(True)
        self.DeclinedBtn.setCheckable(True)
        self.AcceptedBtn.setCheckable(True)
        self.webAppointmentStackWidget.setCurrentIndex(0)
        self.webStatusBtnGroup = QButtonGroup(self)
        for btn in [self.pendingWebBtn, self.DeclinedBtn, self.AcceptedBtn]:
            self.webStatusBtnGroup.addButton(btn)
        self.pendingWebBtn.setChecked(True)
        self.pendingWebBtn.clicked.connect(lambda: self.webAppointmentStackWidget.setCurrentIndex(0))
        self.AcceptedBtn.clicked.connect(lambda: self.webAppointmentStackWidget.setCurrentIndex(1))
        self.DeclinedBtn.clicked.connect(lambda: self.webAppointmentStackWidget.setCurrentIndex(2))

        # toggle sched return status Btn
        self.pendingReturnBtn.setCheckable(True)
        self.completeReurnBtn.setCheckable(True)
        self.overdueReturnBtn.setCheckable(True)
        self.returnStackedWidget.setCurrentIndex(0)
        self.returnStatusBtnGroup = QButtonGroup(self)
        for btn in [self.pendingReturnBtn, self.completeReurnBtn, self.overdueReturnBtn]:
            self.returnStatusBtnGroup.addButton(btn)
        self.pendingReturnBtn.setChecked(True)
        self.pendingReturnBtn.clicked.connect(lambda: self.returnStackedWidget.setCurrentIndex(0))
        self.completeReurnBtn.clicked.connect(lambda: self.returnStackedWidget.setCurrentIndex(1))
        self.overdueReturnBtn.clicked.connect(lambda: self.returnStackedWidget.setCurrentIndex(2))

        #print btn
        self.printBtn.clicked.connect(self.handlePrintButton)

        # cancel
        self.backBtn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(0))
        self.cancelButton.clicked.connect(lambda: self.navigate_to_page(2))
        self.cancelAddServiceBtn.clicked.connect(lambda: self.service_stackedWidget(0))

        #update buttons
        self.updateBasicInfo.hide()
        self.cancelButton.hide()
        self.petUpdateButton.hide()
        self.updateServiceBtn.hide()

        #reminder pop up
        self.make_icon_pulse(self.reminderBtn)

        #nav
        self.miniNavBtn.clicked.connect(self.slide_in_sideNav)
        self.fullNavBtn.clicked.connect(self.slide_out_sideNav)
    def setup_all_back_buttons(self):
        self.all_back_buttons = [
            self.homeBackBtn,
            self.addPatientBackBtn,
            self.RecordsBackBtn,
            self.appointmentBackBtn,
            self.ReturnBackBtn,
            self.profileBackbutton,
            self.petProfileBackBtn,
            self.ReviewBackBtn
        ]
        for btn in self.all_back_buttons:
            btn.clicked.connect(self.go_back)
    def go_back(self):
        if self.page_history:
            index, params = self.page_history.pop()

            self.current_page_index = index
            self.current_params = params
            self.update_back_button_visibility()
            self.stackedWidget.setCurrentIndex(index)
            if index in self.page_to_nav_button:
                self.page_to_nav_button[index].setChecked(True)

                # Load page data if needed
            if index == 5 and "owner_id" in params:
                self.load_pets_for_owner(params["owner_id"])
            elif index == 8 and "pet_id" in params:
                self.load_services_for_pet(params["pet_id"])
    def update_back_button_visibility(self):
        visible = bool(self.page_history)
        for btn in self.all_back_buttons:
            btn.setVisible(visible)
    def navigate_to_page(self, index, is_update=False, **kwargs):
        # Save current page & parameters
        self.page_history.append((self.current_page_index, self.current_params))


        self.current_page_index = index
        self.current_params = kwargs

        self.update_back_button_visibility()
        self.stackedWidget.setCurrentIndex(index)
        self.profileStackedWidget.setCurrentIndex(0)
        if index in self.page_to_nav_button:
            self.page_to_nav_button[index].setChecked(True)
        # Your existing Add Patient logic
        if index == 1:
            if is_update:
                self.updateBasicInfo.show()
                self.cancelButton.show()
                self.confirmButton.hide()
            else:
                self.clearInputs()
                self.updateBasicInfo.hide()
                self.cancelButton.hide()
                self.confirmButton.show()

    #SIDE NAV ANIMATIONS
    def slide_in_sideNav(self):
        # Animate MiniNav sliding out
        mini_anim = QPropertyAnimation(self.MiniNav, b"maximumWidth", self)
        mini_anim.setDuration(500)
        mini_anim.setStartValue(self.MiniNav.width())
        mini_anim.setEndValue(0)
        mini_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # When MiniNav finished sliding out, hide it and slide in SideNav
        def after_mini():
            self.MiniNav.setVisible(False)
            self.sideNav.setVisible(True)

            side_anim = QPropertyAnimation(self.sideNav, b"maximumWidth", self)
            side_anim.setDuration(800)
            side_anim.setStartValue(0)
            side_anim.setEndValue(500)  # full width
            side_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            side_anim.start()
            self._anim_side = side_anim  # keep reference

        mini_anim.finished.connect(after_mini)
        mini_anim.start()
        self._anim_mini = mini_anim  # keep reference
    def slide_out_sideNav(self):
        # Animate SideNav width 500 → 0
        anim = QPropertyAnimation(self.sideNav, b"maximumWidth", self)
        anim.setDuration(800)
        anim.setStartValue(self.sideNav.width())
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def finish():
            # Hide SideNav after animation
            self.sideNav.setVisible(False)
            # Animate MiniNav appearing (0 → 60 for example)
            self.MiniNav.setVisible(True)
            mini_anim = QPropertyAnimation(self.MiniNav, b"maximumWidth", self)
            mini_anim.setDuration(500)
            mini_anim.setStartValue(0)
            mini_anim.setEndValue(100)  # adjust to your mini width
            mini_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            mini_anim.start()
            self._anim2 = mini_anim  # keep reference

        anim.finished.connect(finish)
        anim.start()
        self._anim = anim  # keep reference

    #FOR CLEARING FORMS
    def clearInputs(self):
        # clear fields
        self.firstNameEdit.clear()
        self.middleNameEdit.clear()
        self.lastNameEdit.clear()
        self.phoneNumberEdit.clear()
        self.detailedAddressEdit.clear()
        self.emailEdit.clear()
        self.secondaryPhoneEdit.clear()

        # Reset combo boxes to first index
        self.provinceComboBox.setCurrentIndex(0)
        self.cityComboBox.setCurrentIndex(0)
        self.barangayComboBox.setCurrentIndex(0)

        # clear service inputs
        self.serviceTypeComboBox.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.returnDateEdit.setDate(QDate.currentDate())
        self.addNoteLineEdit.clear()
        self.returnCheckBox.setChecked(False)
        self.returnDateEdit.hide()
        self.returnDatePlaceholder.show()

        #clear pet info
        self.petName.clear()
        self.petColor.clear()
        self.breed.clear()
        self.age.clear()
        self.petRemarks.clear()
        self.speciesComboBox.setCurrentIndex(0)
        self.petSexComboBox.setCurrentIndex(0)
        self.clearSpeciesFunc()
        # reset birthday → back to placeholder
        sentinel = QDate(1900, 1, 1)
        self.Bday.setDate(sentinel)
        self.update_bday_display(sentinel)

    # SET UP SHADOWS
    def setup_input_shadows(self):
        # owner info form
        for line_edit in self.ownerDetailsFrame.findChildren(QLineEdit):
            line_edit.setGraphicsEffect(create_card_shadow())

        for comboBox in self.ownerDetailsFrame.findChildren(QComboBox):
            # Save the internal line edit
            inner_line_edit = comboBox.lineEdit()
            # Temporarily remove it from parent so shadow won't apply to it
            inner_line_edit.setGraphicsEffect(None)
            comboBox.setGraphicsEffect(create_card_shadow())
        #service form
        self.serviceTypeComboBox.setGraphicsEffect(create_card_shadow())
        self.returnDatePlaceholder.setGraphicsEffect(create_card_shadow())
        self.addNoteLineEdit.setGraphicsEffect(create_card_shadow())
        for dates in self.frame_61.findChildren(QDateEdit):
            dates.setGraphicsEffect(create_card_shadow())

        #pet info form
        for petLineEdit in self.petDetailsPage.findChildren(QLineEdit):
            petLineEdit.setGraphicsEffect(create_card_shadow())
        for petComboBox in self.petDetailsPage.findChildren(QComboBox):
            petComboBox.setGraphicsEffect(create_card_shadow())

        for dateEdit in self.petDetailsPage.findChildren(QDateEdit):
            inner_line_edit = dateEdit.findChild(QLineEdit)
            if inner_line_edit:
                inner_line_edit.setGraphicsEffect(None)  # remove shadow from text
            dateEdit.setGraphicsEffect(create_card_shadow())
    def setup_shadow(self):
        self.ProfileCard.setGraphicsEffect(create_card_shadow())
        self.petProfileCard.setGraphicsEffect(create_card_shadow())

        self.reviewClient.setGraphicsEffect(create_card_shadow())
        self.reviewPet.setGraphicsEffect(create_card_shadow())

        self.reviewPet.setGraphicsEffect(create_card_shadow())
        #nav
        self.sideNav.setGraphicsEffect(navShadow())
        self.MiniNav.setGraphicsEffect(navShadow())
        #main content
        self.MainContent.setGraphicsEffect(navShadow())
        #PAGE HEADER
        self.pageHeader1.setGraphicsEffect(create_card_shadow(3,2,2,))
        self.pageHeader2.setGraphicsEffect(create_card_shadow(3,2,2,))
        self.pageHeader3.setGraphicsEffect(create_card_shadow(3,2,2,))
        self.pageHeader4.setGraphicsEffect(create_card_shadow(3,2,2,))
        self.pageHeader5.setGraphicsEffect(create_card_shadow(3,2,2,))
        #ADD PATIENT PAGE
        self.label_4.setGraphicsEffect(create_card_shadow(3,2,2,))
        self.label_15.setGraphicsEffect(create_card_shadow(3,2,2,))

        self.clearSpeciesBtn.setGraphicsEffect(create_card_shadow())

    #FORM INPUT CHECKER
    def collect_and_validate_fields(self, required_fields):
        missing = []

        def apply_style(widget, error=False):
            is_combobox = isinstance(widget, QComboBox)
            if error:
                if is_combobox:
                    widget.setStyleSheet(error_combobox_style)
                else:
                    widget.setStyleSheet(error_style)
            else:
                if is_combobox:
                    widget.setStyleSheet(default_combobox_style)
                else:
                    widget.setStyleSheet(default_style)

        def is_valid_combobox_input(combo):
            text = combo.currentText()
            for i in range(combo.count()):
                if combo.itemText(i).strip().lower() == text.strip().lower():
                    return True
            return False

        data = {}
        for name, widget in required_fields.items():
            if isinstance(widget, QComboBox):
                if widget.currentIndex() == 0 or not is_valid_combobox_input(widget):
                    apply_style(widget, error=True)
                    missing.append(name)
                else:
                    apply_style(widget, error=False)
                    data[name] = widget.currentText()
            else:
                text = widget.text()
                if not text.strip():
                    apply_style(widget, error=True)
                    missing.append(name)
                else:
                    apply_style(widget, error=False)
                    data[name] = text.strip()

        sentinel = QDate(1900, 1, 1)
        if self.Bday.date() != sentinel:
            # real birthday chosen
            bday = self.Bday.date()
            data["birthDay"] = bday.toString("yyyy-MM-dd")
            data["stored_age"] = None
        else:
            # no birthday, only stored_age if entered
            data["birthDay"] = None
            data["stored_age"] = self.age.text().strip() if self.age.text().strip() else None

        return data, missing

    #PATIEN INFO SUBMIT/CHECK DUPLICATE
    def setup_comboboxes(self):
        self.ui_handler = UIHandler(self.provinceComboBox, self.cityComboBox, self.barangayComboBox)
        self.ui_handler.load_provinces()
        combo_boxes = [self.provinceComboBox, self.cityComboBox, self.barangayComboBox]
        placeholders = ["Select Province", "Select City", "Select Barangay"]
        for cb, text in zip(combo_boxes, placeholders):
            cb.setEditable(True)
            cb.lineEdit().setReadOnly(False)
            cb.lineEdit().setPlaceholderText(text)
            cb.lineEdit().setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    def submit_data(self):
        required_fields = {
            "firstName": self.firstNameEdit,
            "lastName": self.lastNameEdit,
            "phoneNumber": self.phoneNumberEdit,
            "province": self.provinceComboBox,
            "city": self.cityComboBox,
            "barangay": self.barangayComboBox,
            "detailedAddress": self.detailedAddressEdit,
            "email": self.emailEdit,
        }

        data, missing = self.collect_and_validate_fields(required_fields)
        data["middleName"] = self.middleNameEdit.text().strip() if self.middleNameEdit.text().strip() else None
        data["SecondaryNumber"] = self.secondaryPhoneEdit.text().strip() if self.secondaryPhoneEdit.text().strip() else None
        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        if not self.ignore_duplicates:
            duplicates = self.check_duplicate_patient(data)
            if duplicates:
                if self.duplicateDialog is None:
                    self.duplicateDialog = DuplicateDialog(duplicates, parent=self, main_window=self)
                    self.duplicateDialog.destroyed.connect(lambda: setattr(self, "duplicateDialog", None))
                else:
                    self.duplicateDialog.populate_cards(duplicates)

                self.duplicateDialog.show_modal()
                return

        self.ignore_duplicates = False

        # proceed to save patient
        if add_new_patient(data):
            self.navigate_to_page(2)
            self.load_patients(1,search_term=None)

            self.clearInputs()

            # Reset styles to default
            for widget in required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

            toast = Toast(self,icon_path="Icons/check.png")
            toast.show_toast()


        else:
            toast = Toast(self, "Failed to add patient!", icon_path="Icons/warning.png")
            toast.show_toast()
    def check_duplicate_patient(self, data):
        try:
            response = requests.post(f"http://127.0.0.1:8000/api/check-duplicate/", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get("duplicates", [])
            else:
                print("Error checking duplicates:", response.status_code, response.text)
                return []
        except Exception as e:
            print("Error:", e)
            return []

    #CLIENT RECORD PAGE
    def load_patients(self, page=1, search_term=None):
        try:
            # ✅ Safe layout clearing - avoid crashes on empty layouts
            items_to_delete = []
            while self.patientListLayout.count():
                child = self.patientListLayout.takeAt(0)
                if child and child.widget():
                    items_to_delete.append(child.widget())

            # Delete after removing from layout
            for widget in items_to_delete:
                try:
                    widget.deleteLater()
                except RuntimeError:
                    pass  # Already deleted

            # Build API URL based on search or normal load
            if search_term and search_term.strip():
                import urllib.parse
                encoded_term = urllib.parse.quote(search_term.strip())
                url = f"http://127.0.0.1:8000/api/patient-search/?page={page}&search={encoded_term}"
            else:
                url = f"http://127.0.0.1:8000/api/patients/?page={page}"

            # Make API request with timeout
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                patients = data.get('results', [])

                # ✅ Update pagination info - ensure valid page number
                self.patient_currentPage = max(1, page)
                self.current_patient_page = self.patient_currentPage
                self.total_patient_pages = data.get('total_pages', 1)
                self.total_patient_count = data.get('count', 0)

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                self.show_empty_state(search_term is not None, error=True)
                return
            except ValueError as e:
                print(f"JSON decode error: {e}")
                self.show_empty_state(search_term is not None, error=True)
                return

            # Handle empty results
            if not patients:
                self.show_empty_state(search_term is not None)
                return

            # Create patient cards
            self.create_patient_cards(patients)

            # Add pagination controls
            self.add_patient_pagination_controls(search_term)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.show_empty_state(False, error=True)
    def show_empty_state(self, is_search, error=False):
        """Show appropriate empty state message"""
        empty_label = QLabel()

        if error:
            empty_label.setText("Error loading patients")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(255, 100, 100);")
        elif is_search:
            empty_label.setText("No patients found")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")
        else:
            empty_label.setText("NO RECORDS")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")

        self.patientListLayout.addStretch()
        self.patientListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.patientListLayout.addStretch()
    def create_patient_cards(self, patients):
        """Create patient cards from patient data"""
        self.patient_cards = []

        for patient in patients:
            card = uic.loadUi("PatientCard.ui")
            self.scale_cards([card], base_h=81)

            # Set patient information
            parts = [patient['firstName'], patient.get('middleName'), patient['lastName']]
            full_name = " ".join(p for p in parts if p)
            card.nameLabel.setText(full_name.title())
            card.emailLabel.setText(patient['email'])

            # Scale fonts
            self.scale_widget_font(card.nameLabel, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")
            self.scale_widget_font(card.emailLabel, base_size=14, min_size=8, max_size=25, family="Montserrat Medium")

            # Connect buttons
            card.deleteButton.clicked.connect(
                lambda _, p_id=patient['id']: self.deleteFunction.set_delete_target("patient", p_id))
            card.editBtn.clicked.connect(lambda _, p_id=patient['id']: self.updateFunction.update_patient_info(p_id))

            # Connect card click
            card.mousePressEvent = lambda event, p=patient: self.show_patient_profile(p)

            card.setGraphicsEffect(create_card_shadow())
            self.patientListLayout.addWidget(card)
            self.patient_cards.append(card)
    def add_patient_pagination_controls(self, search_term=None):
        """Add pagination controls that work with search"""
        # Safely check and delete existing pagination widget
        if hasattr(self, 'patient_pagination_widget'):
            try:
                # Check if widget still exists before deleting
                if self.patient_pagination_widget and self.patient_pagination_widget.isWidgetType():
                    self.patient_pagination_widget.deleteLater()
            except RuntimeError:
                # Widget already deleted, just remove the reference
                pass
            finally:
                # Always remove the reference
                if hasattr(self, 'patient_pagination_widget'):
                    delattr(self, 'patient_pagination_widget')

        if self.total_patient_pages <= 1:
            return

        try:
            self.patient_pagination_widget = uic.loadUi("paginationUi.ui")

            # Connect prev/next buttons with search term
            self.patient_pagination_widget.PrevPage.clicked.connect(
                lambda: self.load_patients(self.current_patient_page - 1, search_term)
            )
            self.patient_pagination_widget.NextPage.clicked.connect(
                lambda: self.load_patients(self.current_patient_page + 1, search_term)
            )

            # Set button states
            self.patient_pagination_widget.PrevPage.setEnabled(self.current_patient_page > 1)
            self.patient_pagination_widget.NextPage.setEnabled(self.current_patient_page < self.total_patient_pages)

            # Create page buttons with search support
            self.create_page_buttons(search_term)

            self.patient_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())
            self.patientListLayout.addWidget(self.patient_pagination_widget)

        except Exception as e:
            print(f"Error creating pagination: {e}")
    def create_page_buttons(self, search_term=None):

        page_layout = self.patient_pagination_widget.pageButtonsLayout

        # Clear existing buttons
        while page_layout.count():
            child = page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_page = self.current_patient_page
        total_pages = self.total_patient_pages
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
                # Pass search term when loading different pages
                page_btn.clicked.connect(lambda checked, p=page: self.load_patients(p, search_term))

            page_layout.addWidget(page_btn)
    def setup_search(self):
        # Connect search bar to search handler
        self.searchBar.textEdited.connect(self.handle_search_input)

        # Setup search timer for debouncing
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self.perform_search)

        # Search state variables
        self.current_search_term = ""
        self.is_searching = False
        self.searchBar.clear()
    def handle_search_input(self, text):
        self.current_search_term = text.strip()
        self._search_timer.start(500)
    def perform_search(self):
        if self.current_search_term:
            self.is_searching = True
            self.load_patients(page=1, search_term=self.current_search_term)
        else:
            # If search is empty, load normal patient list
            self.is_searching = False
            self.load_patients(page=1)

    #DELETE CONFIRMATION MODAL FOR PET/PATIENT PROFILE
    def setup_confirm_card(self):
        self.confirmCard = ConfirmCard(self.findChild(QWidget, "MainContent"))
        self.confirmCard.hide()
        self.confirmCard.setGraphicsEffect(create_card_shadow())
        self.confirmCard.yesButton.clicked.connect(self.deleteFunction.really_delete)
        self.confirmCard.noButton.clicked.connect(self.deleteFunction.cancel_delete)
        self.confirmCard.yesButton.setGraphicsEffect(create_card_shadow())
        self.confirmCard.noButton.setGraphicsEffect(create_card_shadow())
        self.patientToDelete = None

        # delete buttons sa profile patient/pet
        self.profileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_patient)
        self.petProfileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_pet)

    #PATIENT PROFILE PAGE
    def show_patient_profile(self, patient):
        parts = [patient['firstName'], patient.get('middleName'), patient['lastName']]
        full_name = " ".join(p for p in parts if p)
        self.profileNameLabel.setText(full_name)
        self.profileEmailLabel.setText(patient['email'])

        # Combine address parts
        address = f"{patient['barangay']}, {patient['city']}, {patient['province']}"
        contactNumbers = f"{patient['phoneNumber']}  / {patient.get('SecondaryNumber', 'None')}"
        self.addressLabel.setText(address)
        self.detailedAddressLabel.setText(patient['detailedAddress'])
        self.phoneLabel.setText(contactNumbers)

        self.selected_patient_id = patient['id']
        self.profileEditBtn.clicked.connect(lambda: self.updateFunction.update_patient_info(self.selected_patient_id))
        self.load_pets_for_owner(self.selected_patient_id)
        # Navigate to the profile page
        self.navigate_to_page(5, owner_id=patient['id'])

    #PET INFO DATA SUBMIT
    def setup_species_field(self):
        # Hide the "Other" text field initially
        self.otherSpeciesLineEdit.hide()
        self.clearSpeciesBtn.hide()
        # Connect the species combo box change signal
        self.speciesComboBox.currentTextChanged.connect(self.handle_species_selection)
    def handle_species_selection(self, text):
        if text.lower() == "others":
            self.otherSpeciesLineEdit.show()
            self.clearSpeciesBtn.show()
            self.speciesComboBox.hide()
            self.clearSpeciesBtn.clicked.connect(self.clearSpeciesFunc)
        else:
            self.otherSpeciesLineEdit.hide()
            self.otherSpeciesLineEdit.clear()
    def clearSpeciesFunc(self):
        self.otherSpeciesLineEdit.clear()
        self.otherSpeciesLineEdit.hide()
        self.clearSpeciesBtn.hide()
        self.speciesComboBox.show()
        self.speciesComboBox.setCurrentIndex(0)
    def submit_pet_data(self):
        # Only fields that are always required go here:
        required_fields = {
            "petName": self.petName,
            "petColor": self.petColor,
            "breed": self.breed,
            "species": self.speciesComboBox,
            "sex": self.petSexComboBox,
        }

        data, missing = self.collect_and_validate_fields(required_fields)

        if data["species"].lower() == "others":
            custom_species = self.otherSpeciesLineEdit.text().strip()
            if not custom_species:
                toast = Toast(self, "Please specify the species.", icon_path="Icons/warning.png")
                toast.show_toast()
                return
            data["species"] = custom_species

        # optional remarks
        data["remarks"] = self.petRemarks.text().strip() or None

        # ---- Birthday / stored_age logic (exclusive) ----
        sentinel = QDate(1900, 1, 1)
        bday_qdate = self.Bday.date()
        has_birthday = (bday_qdate is not None) and (bday_qdate != sentinel)

        if has_birthday:
            data["birthDay"] = bday_qdate.toString("yyyy-MM-dd")
            data["stored_age"] = None
        else:
            data["birthDay"] = None
            typed_age = self.age.text().strip()
            data["stored_age"] = typed_age if typed_age else None

        # Enforce: at least one of them must be present
        if not has_birthday and not data["stored_age"]:
            toast = Toast(self, "Please provide either Birthday or Age.", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # owner
        data["owner_id"] = self.selected_patient_id

        # (Optional) Debug: confirm payload is clean
        # print("Submitting data:", data)

        if add_new_pet(data):
            self.profileStackedWidget.setCurrentIndex(0)
            self.load_pets_for_owner(self.selected_patient_id)

            self.clearInputs()

            # reset styles for required widgets
            for widget in required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

            toast = Toast(self, icon_path="Icons/check.png")
            toast.show_toast()
        else:
            toast = Toast(self, "Failed to add pet!", icon_path="Icons/warning.png")
            toast.show_toast()
    def setup_pet_buttons(self):
        self.profileStackedWidget.setCurrentIndex(0)
        for btn in [self.addpetQtoolBtn, self.plusSignBtn]:
            btn.clicked.connect(lambda: self.profileStackedWidget.setCurrentIndex(1))
            btn.clicked.connect(lambda: self.clearInputs())
            btn.clicked.connect(lambda: self.petUpdateButton.hide())
            btn.clicked.connect(lambda: self.petConfirmButton.show())
    def update_bday_display(self, date: QDate):
        sentinel = QDate(1900, 1, 1)

        if date == sentinel:
            # No birthday selected → show placeholder and allow manual age
            self.Bday.setDisplayFormat(" ")
            # avoid emitting textChanged if you have handlers
            self.age.blockSignals(True)
            self.age.clear()
            self.age.blockSignals(False)
            self.age.setReadOnly(False)  # user can type stored_age
            return

        # Birthday selected → compute age and lock the field
        self.Bday.setDisplayFormat("MMM d, yyyy")
        today = QDate.currentDate()
        days = date.daysTo(today)

        if days < 0:
            # just in case — shouldn't happen with maxDate set
            days = 0

        if days < 7:
            age_str = f"{days} day{'s' if days != 1 else ''} old"
        elif days < 30:
            weeks = days // 7
            age_str = f"{weeks} week{'s' if weeks != 1 else ''} old"
        elif days < 365:
            months = days // 30
            age_str = f"{months} month{'s' if months != 1 else ''} old"
        else:
            years = days // 365
            age_str = f"{years} year{'s' if years != 1 else ''} old"

        self.age.blockSignals(True)
        self.age.setText(age_str)
        self.age.blockSignals(False)
        self.age.setReadOnly(True)  # computed only

    #PET CARD LOADING IN PATIENT PROFILE
    def load_pets_for_owner(self, owner_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/?owner_id={owner_id}")
        pets = response.json() if response.status_code == 200 else []

        # clear pet cards lang, wag galawin addPetButton
        while self.gridLayout_6.count() > 1:
            item = self.gridLayout_6.takeAt(1)  # skip first item (addPetButton)
            if item and item.widget():
                item.widget().deleteLater()

        container_width = self.scrollAreaWidgetContents.width()
        card_width = 401
        spacing = 10
        max_cols = max(1, (container_width + spacing) // (card_width + spacing))

        row = 0
        col = 1  # start at col=1, col=0 is your addPetButton

        for pet in pets:
            pet_card = uic.loadUi("petRecordCard.ui")
            pet_card.petNameCard.setText(pet["petName"].upper())

            #Dynamic icon by species
            species = pet.get("species", "").lower()
            if species == "dog":
                icon_path = "Icons/dog.png"
            elif species == "cat":
                icon_path = "Icons/catIcon.png"
            else:
                icon_path = "Icons/otherSpecies.png"

            pet_card.petCardIcon.setPixmap(QPixmap(icon_path))
            pet_card.petCardIcon.setScaledContents(True)

            pet_card.mousePressEvent = lambda event, p=pet: self.show_pet_profile(p)
            pet_card.setGraphicsEffect(create_card_shadow())

            self.gridLayout_6.addWidget(pet_card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    #PET PROFILE PAGE
    def show_pet_profile(self, pet):
        self.petProfileNameLabel.setText((pet.get('petName') or "").title())
        self.petColorLabel.setText((pet.get('petColor') or "").title())
        self.petRemarksLabel.setText((pet.get('remarks') or "None"))  # no .capitalize() if None
        self.breedLabel.setText((pet.get('breed') or "").title())
        self.speciesLabel.setText((pet.get('species') or "").title())
        self.petSexLabel.setText((pet.get('sex') or "").title())

        birthday = self.format_date(pet.get("birthDay"))
        self.petBirthdayOptional.setText((birthday or "None"))

        # Show stored/dynamic age, or "Unknown" if missing
        self.petAgeLabel.setText((pet.get('age') or "Unknown"))

        if pet.get("has_reminder", False):
            self.reminderBtn.show()
        else:
            self.reminderBtn.hide()

        species = pet.get("species", "").lower()
        if species == "dog":
            icon_path = "Icons/dog.png"
        elif species == "cat":
            icon_path = "Icons/catIcon.png"
        else:
            icon_path = "Icons/otherSpecies.png"
        self.petProfileIcon.setPixmap(QPixmap(icon_path))

        self.reminderBtn.clicked.connect(lambda: self.open_reminderPopup())
        # Keep track of which pet is selected
        self.selected_pet_id = pet["id"]
        self.petProfileEditBtn.clicked.connect(lambda: self.updateFunction.update_pet_info(self.selected_pet_id))
        # Navigate to pet profile page (adjust index if needed)
        self.navigate_to_page(6, pet_id=pet["id"])
        self.load_services_for_pet(pet["id"])
    def open_reminderPopup(self):
        if not hasattr(self, "reminderPopup") or self.reminderPopup is None:
            self.reminderPopup = ReminderPopup(
                parent=self.findChild(QWidget, "MainContent"),
                main_window=self
            )
        self.reminderPopup.show_reminder()
    def done_reminder(self):
        self.reminderPopup.hide()
    def setup_service_tab(self):
        # toggle service history / add new
        self.addNewServiceBtn.setCheckable(True)
        self.serviceHistoryBtn.setCheckable(True)
        self.serviceShadow.setGraphicsEffect(create_card_shadow())
        self.addServiceShadow.setGraphicsEffect(create_card_shadow())
        self.searchServiceFrame.setGraphicsEffect(create_card_shadow())
        self.serviceHistoryStackedWidget.setCurrentIndex(0)
        self.sourceBtnGroup = QButtonGroup(self)
        self.sourceBtnGroup.setExclusive(True)
        for btn in [self.addNewServiceBtn, self.serviceHistoryBtn]:
            self.sourceBtnGroup.addButton(btn)
        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryBtn.clicked.connect(lambda: self.service_stackedWidget(0))
        self.addNewServiceBtn.clicked.connect(lambda: self.serviceHistoryStackedWidget.setCurrentIndex(1))
    def load_services_for_pet(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/services/?pet_id={pet_id}")
        services = response.json() if response.status_code == 200 else []

        header = self.findChild(QWidget, "serviceTableHeader")


        # Clear existing service cards
        while self.serviceListLayout.count():
            item = self.serviceListLayout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        if not services:
            header.setVisible(False)
            empty_label = QLabel("EMPTY")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            self.serviceListLayout.addStretch()
            self.serviceListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.serviceListLayout.addStretch()
            return

        else:
            header.setVisible(True)

        for service in services:
            service_card = uic.loadUi("serviceCard.ui")

            # Always cast to str to avoid None crashing
            service_type = str(service.get("service_type", "N/A"))
            done_on = self.format_date(service.get("date")) or "N/A"
            return_date = self.format_date(service.get("return_date"))
            notes = str(service.get("notes"))
            # Fill data
            service_card.findChild(QLabel, "serviceLabel").setText(service_type)
            service_card.findChild(QLabel, "doneOnLabel").setText(done_on)
            return_label = service_card.findChild(QLabel, "returnDateLabel")
            return_label.setText(f"{return_date}" if return_date else "       None")

            note_label = service_card.findChild(QTextEdit, "noteLabel")
            note_label.setPlainText(f"{notes}" if notes else "No Notes")

            upper_frame = service_card.findChild(QWidget, "upperFrame")
            lower_frame = service_card.findChild(QWidget, "lowerFrame")
            lower_frame.setVisible(False)

            # Find buttons safely
            open_btn = service_card.findChild(QToolButton, "OpenNoteBtn")
            close_btn = service_card.findChild(QToolButton, "closeNotesBtn")

            service_card.serviceDeleteBtn.clicked.connect(lambda _, service_id=service['id']: self.deleteFunction.set_delete_target("service", service_id))
            service_card.updateServiceCardBtn.clicked.connect(lambda _, service_id=service["id"]: self.updateFunction.update_service_info(service_id))
            service_card.wholeFrameCard.setGraphicsEffect(create_card_shadow())
            # Connect buttons safely
            if open_btn and close_btn and lower_frame:
                open_btn.setVisible(True)
                close_btn.setVisible(False)

                open_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, True,upper_frame))
                close_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, False,upper_frame))

            self.serviceListLayout.addWidget(service_card)
    def make_icon_pulse(self, button):
        # Lock button size so layout won’t move
        button.setFixedSize(button.size())

        rect = button.iconSize()

        grow = QPropertyAnimation(button, b"iconSize")
        grow.setDuration(500)
        grow.setStartValue(rect)
        grow.setEndValue(rect + QSize(4, 4))
        grow.setEasingCurve(QEasingCurve.Type.OutCubic)

        shrink = QPropertyAnimation(button, b"iconSize")
        shrink.setDuration(500)
        shrink.setStartValue(rect + QSize(4, 4))
        shrink.setEndValue(rect)
        shrink.setEasingCurve(QEasingCurve.Type.InCubic)

        self.pulse_anim = QSequentialAnimationGroup(self)
        self.pulse_anim.addAnimation(grow)
        self.pulse_anim.addAnimation(shrink)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.start()
    def toggle_note(self, frame, open_btn, close_btn, show, upper_frame=None):
        frame.setVisible(show)
        open_btn.setVisible(not show)
        close_btn.setVisible(show)
        if upper_frame:
            if show:
                # remove bottom radius para magmukhang dikit sa lower_frame
                upper_frame.setStyleSheet(upper_Frame_Noborrad)
            else:
                # ibalik original radius
                upper_frame.setStyleSheet(upper_Frame_borrad)
    def handlePrintButton(self):
        if self.selected_patient_id and self.selected_pet_id:
            print_url = f"http://127.0.0.1:8000/api/print/{self.selected_patient_id}/{self.selected_pet_id}/"
            webbrowser.open(print_url)
        else:
            QMessageBox.warning(self, "Missing Info", "Please select a patient and a pet first.")

    #PET SERVICE SUBMIT/EDIT
    def submit_service_data(self):
        service_type = self.serviceTypeComboBox.currentText().strip()
        date = self.dateEdit.date().toString("yyyy-MM-dd")

        if self.returnCheckBox.isChecked():
            return_date = self.returnDateEdit.date().toString("yyyy-MM-dd")
        else:
            return_date = None

        notes = self.addNoteLineEdit.toPlainText().strip()

        required_fields = {
            "service_type": self.serviceTypeComboBox
        }

        # Basic validation lang para sa service type
        data, missing = self.collect_and_validate_fields(required_fields)

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        if not self.selected_patient_id or not self.selected_pet_id:
            toast = Toast(self, "No selected owner or pet!", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # Prepare data to send
        service_data = {
            "owner": self.selected_patient_id,
            "pet": self.selected_pet_id,
            "service_type": service_type,
            "date": date,
            "return_date": return_date,
            "notes": notes
        }

        if add_new_service(service_data):
            toast = Toast(self, "Service added!", icon_path="Icons/check.png")
            toast.show_toast()

            self.serviceHistoryBtn.setChecked(True)
            self.serviceHistoryStackedWidget.setCurrentIndex(0)
            self.load_services_for_pet(self.selected_pet_id)
            self.load_scheduled_services()
            # Clear fields or reset
            self.clearInputs()

        else:
            toast = Toast(self, "Failed to add service!", icon_path="Icons/warning.png")
            toast.show_toast()
    def service_stackedWidget(self,index):
        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryStackedWidget.setCurrentIndex(index)
        self.addNewServiceBtn.setText("Add New service")
        self.clearInputs()
        self.addServiceBtn.show()
        self.updateServiceBtn.hide()
    def toggle_return_date(self, checked):
        if checked:
            self.returnDateEdit.show()
            min_date = self.dateEdit.date().addDays(1)
            today_plus_1 = QDate.currentDate().addDays(1)
            # piliin ang mas malayo sa dalawa
            default_date = min_date if min_date > today_plus_1 else today_plus_1
            self.returnDateEdit.setDate(default_date)
            self.returnDatePlaceholder.hide()
        else:
            self.returnDateEdit.hide()
            self.returnDatePlaceholder.show()

    #WALKIN PAGE
    def setup_add_appintmentPopUp(self):
        self.appointmentCard = AddAppointmentCard(
            parent=self.findChild(QWidget, "MainContent"),
            main_window=self  # pass the MainUI instance
        )
        self.appointmentCard.hide()
        self.appointmentCard.closePopUpBtn.clicked.connect(self.cancel_appointment)
        self.appointmentCard.cancelAddAppointment.clicked.connect(self.cancel_appointment)
    def cancel_appointment(self):
        self.appointmentCard.hide()
    def open_addAppointment(self):
        self.appointmentCard.load_patients_to_combobox()
        self.appointmentCard.show_card()

    #SCHEDULED RETURN VIST PAGE
    def set_current_month_in_combobox(self):
        self.monthComboBox.setGraphicsEffect(create_card_shadow())
        current_month = datetime.now().strftime("%B")
        index = self.monthComboBox.findText(current_month)
        if index >= 0:
            self.monthComboBox.setCurrentIndex(index)
    def load_scheduled_services(self):
        response = requests.get("http://127.0.0.1:8000/api/scheduled-services/")
        scheduled_services = response.json() if response.status_code == 200 else []

        # get selected month from combobox
        selected_month = self.monthComboBox.currentText()  # e.g., 'August'

        # clear all layouts before repopulating
        for layout in [self.pendingLayout, self.completedLayout, self.overdueLayout]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # filter by return_date month
        filtered_services = []
        for service in scheduled_services:
            return_date_str = service.get("return_date")
            if return_date_str:
                try:
                    date_obj = datetime.strptime(return_date_str, "%Y-%m-%d")
                    month_name = date_obj.strftime("%B")
                    if month_name == selected_month:  # match month
                        filtered_services.append(service)
                except ValueError:
                    pass  # skip invalid dates

        if not filtered_services:
            # show empty in each page if no services at all for the month
            for layout in [self.pendingLayout, self.completedLayout, self.overdueLayout]:
                empty_label = QLabel("EMPTY")
                empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
                layout.addStretch()
                layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
                layout.addStretch()
            return

        # segregate by status after filtering
        for service in filtered_services:
            card = uic.loadUi("schedCard.ui")
            card.ReturnNameLabel.setText(service['owner_full_name'].title())
            card.petName.setText(service['pet_name'].capitalize())
            card.ReturnServiceLabel.setText(service['service_type'])
            return_date = self.format_date(service.get("return_date"))
            card.ReturnDateCardLabel.setText(return_date)
            card.setGraphicsEffect(create_card_shadow())

            status = service.get("status")
            if status == "pending":
                self.pendingLayout.addWidget(card)
            elif status == "completed":
                self.completedLayout.addWidget(card)
            elif status == "overdue":
                self.overdueLayout.addWidget(card)
            card.mousePressEvent = lambda event, pid=service["pet"]: self.open_pet_from_service(pid)
    def open_pet_from_service(self, pet_id):
        response = requests.get(f"http://127.0.0.1:8000/api/pets/{pet_id}/")
        if response.status_code == 200:
            pet = response.json()
            self.selected_pet_id = pet["id"]
            self.selected_patient_id = pet["owner"]["id"]
            self.show_pet_profile(pet)

    #DATE PICK AND DATE FORMATING LOGIC
    def setup_dates(self):
        self.activeDateEdit = None
        self.dateEdit.mousePressEvent = lambda event: self.show_custom_calendar(self.dateEdit)
        self.returnDateEdit.mousePressEvent = lambda event: self.show_custom_calendar(self.returnDateEdit)
        self.dateEdit.setDate(QDate.currentDate())

        # return date checkbox
        self.returnDatePlaceholder.setReadOnly(True)
        self.returnDateEdit.hide()
        self.returnCheckBox.toggled.connect(self.toggle_return_date)

        # --- Pet birthday setup ---
        sentinel = QDate(1900, 1, 1)
        self.Bday.setSpecialValueText("Birthday (optional)")
        self.Bday.setDisplayFormat(" ")  # start blank
        self.Bday.setDate(sentinel)  # sentinel means "no birthday"
        self.Bday.setMinimumDate(sentinel)
        self.Bday.setMaximumDate(QDate.currentDate())  # no future birthdays

        # open your custom calendar
        self.Bday.mousePressEvent = lambda event: self.show_custom_calendar(self.Bday)

        # recompute age when birthday changes
        self.Bday.dateChanged.connect(self.update_bday_display)

        # make sure age is editable only when no birthday
        self.age.setReadOnly(True)  # will be flipped in update_bday_display
    def format_date(self, raw):
        if raw:
            try:
                dt = datetime.strptime(raw, "%Y-%m-%d")
                return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
            except Exception:
                return raw
        return None
    def setup_calendar(self):
        self.customCalendar = uic.loadUi("customCalendar.ui")
        self.customCalendar.setParent(None)
        self.customCalendar.setWindowFlags(Qt.WindowType.Popup)
        self.calendarWidget = self.customCalendar.findChild(QCalendarWidget, "calendarWidget")
        self.calendarWidget.clicked.connect(self.set_date_from_calendar)
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.setStyleSheet(QframeStyle)
    def show_custom_calendar(self, dateEdit):
        self.activeDateEdit = dateEdit
        pos = dateEdit.mapToGlobal(QPoint(0, dateEdit.height()))
        self.customCalendar.move(pos)

        sentinel = QDate(1900, 1, 1)
        current_date = dateEdit.date()
        if dateEdit == self.Bday and current_date == sentinel:
            current_date = QDate.currentDate()

        # Limit max date for birthday to today
        if dateEdit == self.Bday:
            self.calendarWidget.setMaximumDate(QDate.currentDate())
            self.calendarWidget.setMinimumDate(QDate(1900, 1, 1))  # optional, if you want a realistic range
        elif dateEdit == self.returnDateEdit:
            min_date = self.dateEdit.date().addDays(1)
            self.calendarWidget.setMinimumDate(min_date)
            self.calendarWidget.setMaximumDate(QDate(7999, 12, 31))  # some far future max
        elif dateEdit == self.appointmentCard.popUpDateEdit:
            # 💼 Appointment date: no past allowed
            self.calendarWidget.setMinimumDate(QDate.currentDate())
            self.calendarWidget.setMaximumDate(QDate(7999, 12, 31))
        else:
            self.calendarWidget.setMinimumDate(QDate(1752, 9, 14))
            self.calendarWidget.setMaximumDate(QDate(7999, 12, 31))  # default max

        self.calendarWidget.setSelectedDate(current_date)
        self.customCalendar.show()
        QApplication.processEvents()
        self.calendarWidget.repaint()
    def set_date_from_calendar(self, date):
        if self.activeDateEdit:
            self.activeDateEdit.setDate(date)
        self.customCalendar.hide()

    #WIDGET AND FONT SCALING FOR RESPONSIVENESS
    def scale_widget_font(self, widget, base_size, min_size=8, max_size=20, family=None):
        w_scale = self.width() / 1280
        h_scale = self.height() / 720
        scale = min(w_scale, h_scale)

        scaled_size = int(base_size * scale)
        final_size = max(min_size, min(scaled_size, max_size))

        f = widget.font()
        if family:  # if provided, override
            f.setFamily(family)
        f.setPointSize(final_size)
        widget.setFont(f)
    def scale_label_pixmap(self, label, min_size=32, max_size=256):
        """
        Scale a QLabel pixmap relative to window size.
        Uses the Designer's original size as baseline.
        """
        # cache the base size once
        if not hasattr(label, "_base_size"):
            base_w = label.maximumWidth() if label.maximumWidth() > 0 else label.width()
            base_h = label.maximumHeight() if label.maximumHeight() > 0 else label.height()
            label._base_size = (base_w, base_h)

        base_w, base_h = label._base_size

        # scale relative to baseline window size
        w_scale = self.width() / 1280
        h_scale = self.height() / 720
        scale = min(w_scale, h_scale)

        new_w = int(base_w * scale)
        new_h = int(base_h * scale)

        # clamp
        new_w = max(min_size, min(new_w, max_size))
        new_h = max(min_size, min(new_h, max_size))

        label.setFixedSize(new_w, new_h)
        label.setScaledContents(True)
    def scale_cards(self, cards, base_h=90, design_height=720):
        """Scale the height of a list of cards based on the main window size."""
        if not cards:
            return

        h_scale = self.height() / design_height
        new_h = int(base_h * h_scale)

        for i, card in enumerate(cards, start=1):
            card.setFixedHeight(new_h)
            # Debug
    def resizeEvent(self, event):
        super().resizeEvent(event)


        self.scale_label_pixmap(self.clinicIconP1, min_size=64, max_size=256)
        self.scale_label_pixmap(self.clinicIconP2, min_size=64, max_size=256)
        self.scale_label_pixmap(self.clinicIconP3, min_size=64, max_size=256)
        self.scale_label_pixmap(self.clinicIconP4, min_size=64, max_size=256)
        self.scale_label_pixmap(self.PetmateLogo, min_size=81, max_size=356)
        self.scale_label_pixmap(self.profileIcon, min_size=120, max_size=200)

        # for Qline Edits
        for line_edit in self.findChildren(QLineEdit):
            self.scale_widget_font(line_edit, base_size=12, min_size=8, max_size=25,family="Montserrat Medium")
        #for comboBox
        for comboBox in self.findChildren(QComboBox):
            self.scale_widget_font(comboBox, base_size=12, min_size=8, max_size=25,family="Montserrat Medium")
        # for date
        for dateEdit in self.findChildren(QDateEdit):
            self.scale_widget_font(dateEdit, base_size=12, min_size=8, max_size=25,family="Montserrat Medium")
        #owner details title label
        for title_label in self.ownerDetailsFrame.findChildren(QLabel):
            self.scale_widget_font(title_label, base_size=16, min_size=12, max_size=35,family="Rubik Mono One")
        #owner details header
        self.scale_widget_font(self.pageHeader1, base_size=25, min_size=12, max_size=35,family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader2, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader3, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader4, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader5, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")

        # pet details title
        self.scale_widget_font(self.label_27, base_size=16, min_size=14, max_size=35, family="Rubik Mono One")
        for submitBtns in self.findChildren(QPushButton):
            self.scale_widget_font(submitBtns, base_size=14, min_size=8, max_size=25,family="Rubik Mono One")
        #for nav Btns
        for navBtns in self.Buttons.findChildren(QToolButton):
            self.scale_widget_font(navBtns, base_size=12, min_size=8, max_size=55, family="Montserrat Black")

        #Appointment page
        for pushBtns in self.AppointmentPage.findChildren(QPushButton):
            self.scale_widget_font(pushBtns, base_size=12, min_size=10, max_size=35, family="Montserrat SemiBold")
        for toolBtn in self.addWalkinButton.findChildren(QToolButton):
            self.scale_widget_font(toolBtn, base_size=25, min_size=25, max_size=45, family="Montserrat ExtraBold")

        #Sched page
        for pushBtns in self.schedFrame.findChildren(QPushButton):
            self.scale_widget_font(pushBtns, base_size=12, min_size=10, max_size=35, family="Montserrat SemiBold")

        #Profile card
        for ownerDetail in self.frame_13.findChildren(QLabel):
            self.scale_widget_font(ownerDetail, base_size=12, min_size=10, max_size=35, family="Montserrat Light")
        self.scale_widget_font(self.profileNameLabel, base_size=16, min_size=12, max_size=45, family="Montserrat ExtraBold")

        #patientCard
        self.scale_cards(self.patient_cards, base_h=90)
        for i, card in enumerate(getattr(self, "patient_cards", []), start=1):
            for nameLabel in card.findChildren(QLabel, "nameLabel"):
                self.scale_widget_font(nameLabel, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")

            for emailLabel in card.findChildren(QLabel, "emailLabel"):
                self.scale_widget_font(emailLabel, base_size=14, min_size=8, max_size=25, family="Montserrat Medium")

            if card.profileIcon:
                self.scale_label_pixmap(card.profileIcon, min_size=50, max_size=120)



if __name__ == "__main__":
    app = QApplication(sys.argv)


    font_path = os.path.join(os.path.dirname(__file__), "font/Montserrat/Montserrat-VariableFont_wght.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    ui = MainUI()
    ui.show()
    app.exec()

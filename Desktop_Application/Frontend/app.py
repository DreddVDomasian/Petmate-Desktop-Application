import os
import sys
from http.client import responses

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
    QParallelAnimationGroup, QTimer, QRegularExpression, QSettings, QTime
from PyQt6.QtGui import QFontDatabase, QPixmap,QIntValidator, QRegularExpressionValidator
from uiLogic import UIHandler
from input_styles import *
from toast import Toast
import resources_rc
from Desktop_Application.Backend.api_client import add_new_patient, add_new_pet, add_new_service,desktop_login
from confirm_card import ConfirmCard
from ReminderPopUp import ReminderPopup
from appointmentPopUp import AddAppointmentCard
from addServicePopUp import AddServicePopUp
from functools import partial
from datetime import datetime
from shadowEffects import *
from delete import Delete
from duplicateDialog import DuplicateDialog
from updateFunction import Update
from config_loader import API_BASE_URL
import requests
import webbrowser

from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QVBoxLayout
from analytics import fetch_json



class MainUI(QMainWindow):
    def __init__(self,user_data=None):
        super(MainUI, self).__init__()
        uic.loadUi("ui-files/Home.ui", self)


        # Initialize delete and update functions
        self.deleteFunction = Delete(self)
        self.updateFunction = Update(self)

        #users
        self.current_user = user_data
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
        self.setup_add_service()
        self.setup_pet_buttons()

        #Settings
        self.UserManagementTabBtn.hide()
        self.role_base()
        self.load_user_profile(self.current_user)
        self.setup_security_tab()
        self.setup_user_management_tab()

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
        self.accountCards = []
        # Page navigation state
        self.page_history = []
        self.current_page_index = 0
        self.current_params = {}

        self.setup_phone_validator()
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
        self.load_staff_accounts()

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

        self.temp_passwords = {}

        # Analytics/Homepage
        self.stackedWidget.setCurrentIndex(0)
        self.setup_bar_graph()
        self.setup_pie_graph()

        self.analyticsTimer = QTimer()
        self.analyticsTimer.timeout.connect(self.refresh_analytics)
        self.analyticsTimer.start(15000)

        self.setup_office_hours()

        #LAYOUT FOR SCROLL AREAS FOR CARDS
    def setup_layouts(self):
        self.accountUserLayout = self.accountUserScrollAreaContents.layout()
        self.accountUserLayout.setSpacing(10)
        self.accountUserLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
            (self.appointmentBtn, 3), (self.schedVaxBtn, 4),(self.settingsBtn, 8),(self.webContentBtn, 10)
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
            (self.appointmentBtn_2, 3), (self.schedVaxBtn_2, 4),(self.settings_2, 8),(self.webContentBtn_2, 10)
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
            8: self.settingsBtn,
            10:self.webContentBtn,
            # Profile and Pet Profile pages should highlight Pet Records
            5: self.petRecordsBtn,
            6: self.petRecordsBtn
        }

        # send data
        self.confirmButton.clicked.connect(self.submit_data)
        self.petConfirmButton.clicked.connect(self.submit_pet_data)
        self.addServiceBtn.clicked.connect(self.submit_service_data)

        #add service
        self.addNewServices.mousePressEvent = lambda event: self.open_add_service()

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

        #Web management stackwidget
        self.serviceTab.setChecked(True)
        self.officeHoursTab.setChecked(True)
        self.webManagementStackedWidget.setCurrentIndex(0)
        self.webManagementStatusBtnGroup = QButtonGroup(self)
        for btn in [ self.serviceTab, self.officeHoursTab]:
            self.webManagementStatusBtnGroup.addButton(btn)
        self.serviceTab.setChecked(True)
        self.serviceTab.clicked.connect(lambda: self.webManagementStackedWidget.setCurrentIndex(0))
        self.officeHoursTab.clicked.connect(lambda: self.webManagementStackedWidget.setCurrentIndex(1))


        #Settings Stack widget
        # toggle walk-in status Btn
        self.profileTabBtn.setCheckable(True)
        self.securityTabBtn.setCheckable(True)
        self.UserManagementTabBtn.setCheckable(True)
        self.settingsStactWidget.setCurrentIndex(0)
        self.settingsBtnGroup = QButtonGroup(self)
        for btn in [self.profileTabBtn, self.securityTabBtn, self.UserManagementTabBtn]:
            self.settingsBtnGroup.addButton(btn)
        self.profileTabBtn.setChecked(True)
        self.profileTabBtn.clicked.connect(lambda: self.settingsStactWidget.setCurrentIndex(0))
        self.securityTabBtn.clicked.connect(lambda: self.settingsStactWidget.setCurrentIndex(1))
        self.UserManagementTabBtn.clicked.connect(lambda: self.settingsStactWidget.setCurrentIndex(3))

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
        self.settingsProfileSaveBtn.hide()
        self.settingsProfileCancelBtn.hide()

        #reminder pop up
        self.make_icon_pulse(self.reminderBtn)

        #nav
        self.miniNavBtn.clicked.connect(self.slide_in_sideNav)
        self.fullNavBtn.clicked.connect(self.slide_out_sideNav)

        #profile settings
        self.settingsProfileEditBtn.clicked.connect(self.enableProfileEdit)


    def setup_all_back_buttons(self):
        self.all_back_buttons = [
            self.homeBackBtn,
            self.addPatientBackBtn,
            self.RecordsBackBtn,
            self.appointmentBackBtn,
            self.ReturnBackBtn,
            self.profileBackbutton,
            self.petProfileBackBtn,
            self.ReviewBackBtn,
            self.settingsBackBtn
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
                self.updateFunction.is_email_enable(self.selected_patient_id)
                self.updateBasicInfo.show()
                self.cancelButton.show()
                self.confirmButton.hide()
            else:
                self.emailEdit.setReadOnly(False)
                self.clearInputs()
                self.updateBasicInfo.hide()
                self.cancelButton.hide()
                self.confirmButton.show()
        if index == 2:
            self.emailEdit.setReadOnly(False)


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

        for settingsLineEdit in self.profileInfoFrame.findChildren(QLineEdit):
            settingsLineEdit.setGraphicsEffect(create_card_shadow())

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

        #settings shadow
        self.changePassFrame.setGraphicsEffect(create_card_shadow())
        self.profileInfoFrame.setGraphicsEffect(create_card_shadow())

    #FORM INPUT CHECKER
    def setup_phone_validator(self):
        # Set up phone number validators - numbers only
        phone_validator = QRegularExpressionValidator(QRegularExpression(r'^[0-9]{0,11}$'))
        self.phoneNumberEdit.setValidator(phone_validator)
        self.secondaryPhoneEdit.setValidator(phone_validator)

        # Connect the text change signals
        self.phoneNumberEdit.textChanged.connect(self.on_phone_number_changed)
        self.secondaryPhoneEdit.textChanged.connect(self.on_secondary_phone_changed)
    def validate_phone_number(self, phone):
        """Validate and format Philippine phone numbers"""
        # Remove any non-digit characters except +
        cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')

        # Check if it's a valid Philippine mobile number
        if len(cleaned_phone) == 11 and cleaned_phone.startswith('09'):  # 09 + 9 digits = 11
            # Convert 09XXXXXXXXX to +639XXXXXXXXX
            return '+63' + cleaned_phone[1:]
        elif len(cleaned_phone) == 12 and cleaned_phone.startswith('639'):  # 639 + 9 digits = 12
            return '+' + cleaned_phone
        elif len(cleaned_phone) == 13 and cleaned_phone.startswith('+639'):  # +639 + 9 digits = 13
            return cleaned_phone

        return None
    def validate_email(self, email):
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    def collect_and_validate_fields(self, required_fields):
        missing = []
        invalid_fields = []

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
                    # Special validation for phone numbers and email
                    if name == "phoneNumber":
                        formatted_phone = self.validate_phone_number(text)
                        if formatted_phone:
                            apply_style(widget, error=False)
                            data[name] = formatted_phone
                        else:
                            apply_style(widget, error=True)
                            invalid_fields.append("Phone number (must be 09XXXXXXXXX or +63XXXXXXXXXX)")

                    elif name == "email":
                        if self.validate_email(text):
                            apply_style(widget, error=False)
                            data[name] = text.strip()
                        else:
                            apply_style(widget, error=True)
                            invalid_fields.append("Email address (must be valid format)")

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

        return data, missing, invalid_fields

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

        data, missing, invalid_fields = self.collect_and_validate_fields(required_fields)
        data["middleName"] = self.middleNameEdit.text().strip() if self.middleNameEdit.text().strip() else None

        # Validate secondary phone number if provided
        secondary_phone = self.secondaryPhoneEdit.text().strip()
        if secondary_phone:
            formatted_secondary = self.validate_phone_number(secondary_phone)
            if formatted_secondary:
                data["SecondaryNumber"] = formatted_secondary
            else:
                invalid_fields.append("Secondary phone number (must be 09XXXXXXXXX or +63XXXXXXXXXX)")
        else:
            data["SecondaryNumber"] = None

        # Show error messages if any
        if missing or invalid_fields:
            messages = []
            if missing:
                messages.append("The following fields are required:\n• " + "\n• ".join(missing))
            if invalid_fields:
                messages.append("The following fields are invalid:\n• " + "\n• ".join(invalid_fields))

            message = "\n\n".join(messages)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        if not self.ignore_duplicates:
            duplicate_result = self.check_duplicate_patient(data)
            duplicates = duplicate_result.get("duplicates", [])
            email_conflict = duplicate_result.get("email_conflict", None)
            if email_conflict:
                Toast(self, "This email is already used by another patient.",
                      icon_path="Icons/warning.png").show_toast()
                return

            if duplicates:
                if self.duplicateDialog is None:
                    self.duplicateDialog = DuplicateDialog(
                        duplicates, parent=self, main_window=self
                    )
                    self.duplicateDialog.destroyed.connect(
                        lambda: setattr(self, "duplicateDialog", None)
                    )
                else:
                    self.duplicateDialog.populate_cards(duplicates)

                self.duplicateDialog.show_modal()
                return

        self.ignore_duplicates = False

        # proceed to save patient
        if add_new_patient(data):
            self.navigate_to_page(2)
            self.load_patients(1, search_term=None)

            self.clearInputs()

            # Reset styles to default
            for widget in required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

            toast = Toast(self, icon_path="Icons/check.png")
            toast.show_toast()
        else:
            toast = Toast(self, "Failed to add patient!", icon_path="Icons/warning.png")
            toast.show_toast()
    def on_phone_number_changed(self, text):
        """Real-time phone number formatting with numbers-only input and length limits"""
        # If text is empty, return
        if not text:
            return

        # Store cursor position
        cursor_pos = self.phoneNumberEdit.cursorPosition()

        # Auto-format from 09 to +639 in real-time
        if text.startswith('09') and len(text) >= 2:
            if len(text) == 11:  # 09 + 9 digits = complete number
                formatted = '+63' + text[1:]
                if formatted != text:
                    # Temporarily disconnect to avoid recursion
                    self.phoneNumberEdit.textChanged.disconnect(self.on_phone_number_changed)
                    self.phoneNumberEdit.setText(formatted)
                    # Reconnect the signal
                    self.phoneNumberEdit.textChanged.connect(self.on_phone_number_changed)
                    # Move cursor to end
                    self.phoneNumberEdit.setCursorPosition(len(formatted))

            # If user tries to type beyond 11 digits, truncate
            elif len(text) > 11:
                # Temporarily disconnect to avoid recursion
                self.phoneNumberEdit.textChanged.disconnect(self.on_phone_number_changed)
                self.phoneNumberEdit.setText(text[:11])
                # Reconnect the signal
                self.phoneNumberEdit.textChanged.connect(self.on_phone_number_changed)
                self.phoneNumberEdit.setCursorPosition(cursor_pos)
    def on_secondary_phone_changed(self, text):
        """Real-time secondary phone number formatting with numbers-only input and length limits"""
        # If text is empty, return
        if not text:
            return

        # Store cursor position
        cursor_pos = self.secondaryPhoneEdit.cursorPosition()

        # Auto-format from 09 to +639 in real-time
        if text.startswith('09') and len(text) >= 2:
            if len(text) == 11:  # 09 + 9 digits = complete number
                formatted = '+63' + text[1:]
                if formatted != text:
                    # Temporarily disconnect to avoid recursion
                    self.secondaryPhoneEdit.textChanged.disconnect(self.on_secondary_phone_changed)
                    self.secondaryPhoneEdit.setText(formatted)
                    # Reconnect the signal
                    self.secondaryPhoneEdit.textChanged.connect(self.on_secondary_phone_changed)
                    # Move cursor to end
                    self.secondaryPhoneEdit.setCursorPosition(len(formatted))

            # If user tries to type beyond 11 digits, truncate
            elif len(text) > 11:
                # Temporarily disconnect to avoid recursion
                self.secondaryPhoneEdit.textChanged.disconnect(self.on_secondary_phone_changed)
                self.secondaryPhoneEdit.setText(text[:11])
                # Reconnect the signal
                self.secondaryPhoneEdit.textChanged.connect(self.on_secondary_phone_changed)
                self.secondaryPhoneEdit.setCursorPosition(cursor_pos)

    def check_duplicate_patient(self, data):
        try:
            response = requests.post(f"{API_BASE_URL}/api/check-duplicate/", json=data)
            if response.status_code == 200:
                result = response.json()
                return {
                    "duplicates": result.get("duplicates", []),
                    "email_conflict": result.get("email_conflict", None)
                }
            else:
                print("Error checking duplicates:", response.status_code, response.text)
                return {"duplicates": [], "email_conflict": None}
        except Exception as e:
            print("Error:", e)
            return {"duplicates": [], "email_conflict": None}

    #CLIENT RECORD PAGE
    def load_patients(self, page=1, search_term=None):
        try:

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
                url = f"{API_BASE_URL}/api/patient-search/?page={page}&search={encoded_term}"
            else:
                url = f"{API_BASE_URL}/api/patients/?page={page}"

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

            if not patients and page > 1:
                return self.load_patients(page - 1, search_term)

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
            card = uic.loadUi("ui-files/PatientCard.ui")
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
            self.patient_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

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

        # Store the default delete action
        self.confirmCard.yesButton.clicked.connect(self.deleteFunction.really_delete)
        self.confirmCard.noButton.clicked.connect(self.deleteFunction.cancel_delete)

        self.confirmCard.yesButton.setGraphicsEffect(create_card_shadow())
        self.confirmCard.noButton.setGraphicsEffect(create_card_shadow())
        self.patientToDelete = None

        # Store original configuration
        self.confirmCard_original_config = {
            'message': "Are you sure you want to delete this record?",
            'yes_text': "YES",
            'no_text': "NO",
            'yes_style': "rgb(220, 90, 90)",
            'no_style': "#FCD597"
        }

        # delete buttons sa profile patient/pet
        self.profileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_patient)
        self.petProfileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_pet)

    #PATIENT PROFILE PAGE
    def show_patient_profile(self, patient):
        parts = [patient['firstName'], patient.get('middleName'), patient['lastName']]
        full_name = " ".join(p for p in parts if p)
        self.profileNameLabel.setText(full_name.title())
        self.profileEmailLabel.setText(patient['email'])

        # Combine address parts
        address = f"{patient['barangay']}, {patient['city']}, {patient['province']}"
        contactNumbers = f"{patient['phoneNumber']}  / {patient.get('SecondaryNumber', 'None')}"
        self.addressLabel.setText(address.title())
        self.detailedAddressLabel.setText(patient['detailedAddress'].title())
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

        data, missing, invalid_fields = self.collect_and_validate_fields(required_fields)

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
        response = requests.get(f"{API_BASE_URL}/api/pets/?owner_id={owner_id}")
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
            pet_card = uic.loadUi("ui-files/petRecordCard.ui")
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
        response = requests.get(f"{API_BASE_URL}/api/services/?pet_id={pet_id}")
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
            service_card = uic.loadUi("ui-files/serviceCard.ui")

            # Always cast to str to avoid None crashing
            service_type = str(service.get("service_type", "N/A"))
            done_on = self.format_date(service.get("date")) or "N/A"
            return_date = self.format_date(service.get("return_date"))
            service_status = str(service.get("status", "N/A"))
            notes = str(service.get("notes"))
            # Fill data
            service_card.findChild(QLabel, "serviceLabel").setText(service_type)
            service_card.findChild(QLabel, "doneOnLabel").setText(done_on)
            return_label = service_card.findChild(QLabel, "returnDateLabel")
            return_label.setText(f"               {return_date}" if return_date else "                       None")
            service_card.findChild(QLabel, "serviceStatusLabel").setText(service_status.upper())

            if service_status.lower() == "completed":
                service_card.serviceStatusFrame.setStyleSheet(completedServiceStatus)
            elif service_status.lower() == "pending":
                service_card.serviceStatusFrame.setStyleSheet(pendingServiceStatus)
            elif service_status.lower() == "overdue":
                service_card.serviceStatusFrame.setStyleSheet(overdueServiceStatus)

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

            self.serviceListLayout.insertWidget(0, service_card)
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
            print_url = f"{API_BASE_URL}/api/print/{self.selected_patient_id}/{self.selected_pet_id}/"
            webbrowser.open(print_url)
        else:
            QMessageBox.warning(self, "Missing Info", "Please select a patient and a pet first.")
    #PET PROFILE RELOAD
    def refresh_current_pet_profile(self):
        """Refresh the current pet profile without affecting navigation history"""
        if hasattr(self, 'selected_pet_id') and self.selected_pet_id:
            try:
                response = requests.get(f"{API_BASE_URL}/api/pets/{self.selected_pet_id}/")
                if response.status_code == 200:
                    pet = response.json()
                    # Update the UI elements directly without navigation
                    self.update_pet_profile_ui(pet)
            except Exception as e:
                print(f"Error refreshing pet profile: {e}")
    def update_pet_profile_ui(self, pet):
        """Update pet profile UI elements without navigation"""
        self.petProfileNameLabel.setText((pet.get('petName') or "").title())
        self.petColorLabel.setText((pet.get('petColor') or "").title())
        self.petRemarksLabel.setText((pet.get('remarks') or "None"))
        self.breedLabel.setText((pet.get('breed') or "").title())
        self.speciesLabel.setText((pet.get('species') or "").title())
        self.petSexLabel.setText((pet.get('sex') or "").title())

        birthday = self.format_date(pet.get("birthDay"))
        self.petBirthdayOptional.setText((birthday or "None"))
        self.petAgeLabel.setText((pet.get('age') or "Unknown"))

        # Update reminder button visibility
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
        data, missing, invalid_fields = self.collect_and_validate_fields(required_fields)

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

            if hasattr(self, 'selected_pet_id') and self.selected_pet_id:
                self.refresh_current_pet_profile()
                self.load_services_for_pet(self.selected_pet_id)

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
        self.dateEdit.setEnabled(True)
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

    #add service
    def setup_add_service(self):
        self.addServiceCard = AddServicePopUp(
            parent=self.findChild(QWidget, "MainContent"),
            main_window=self  # pass the MainUI instance
        )
        self.addServiceCard.hide()
        self.addServiceCard.closePopUpBtn.clicked.connect(self.cancel_add_service)
        self.addServiceCard.cancelAddServiceBtn.clicked.connect(self.cancel_add_service)
    def cancel_add_service(self):
        self.addServiceCard.hide()
    def open_add_service(self):
        self.addServiceCard.show_card()
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
            card = uic.loadUi("ui-files/schedCard.ui")
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
        response = requests.get(f"{API_BASE_URL}/api/pets/{pet_id}/")
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
        if not raw:
            return None

        try:
            # Use dateutil parser for more flexibility
            from dateutil import parser
            dt = parser.isoparse(raw)  # Handles ISO 8601 format
            return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
        except ImportError:
            # Fallback if dateutil is not available
            try:
                if 'T' in raw:
                    # Handle ISO format manually
                    date_part = raw.split('T')[0]
                    dt = datetime.strptime(date_part, "%Y-%m-%d")
                    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
                else:
                    # Handle regular date format
                    dt = datetime.strptime(raw, "%Y-%m-%d")
                    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
            except Exception as e:
                print(f"Date formatting error: {e}")
                return raw
        except Exception as e:
            print(f"Date formatting error: {e}")
            return raw
    def setup_calendar(self):
        self.customCalendar = uic.loadUi("ui-files/customCalendar.ui")
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


    #SETTINGS PAGE
    #Role base settings
    def role_base(self):
        UserRole = self.current_user['role']
        if UserRole == "admin":
            self.UserManagementTabBtn.show()

    #    PROFILE TAB
    def enableProfileEdit(self):
        self.profileFullName.setEnabled(True)
        self.profileEmail.setEnabled(True)
        self.profilePhone.setEnabled(True)

        # Setup validation and apply edit styles
        self.setup_profile_validation()
        self.apply_profile_edit_style()
        self.passwordFrame.show()
        self.spacer.hide()
        self.settingsProfileEditBtn.hide()
        self.settingsProfileSaveBtn.show()
        self.settingsProfileCancelBtn.show()

        self.settingsProfileSaveBtn.clicked.connect(self.save_profile_changes)
        self.settingsProfileCancelBtn.clicked.connect(self.profileEdit_cancel)
    def setup_profile_validation(self):
        """Setup validation for profile form fields"""
        # Phone number validator (numbers only, max 11 digits)
        phone_validator = QRegularExpressionValidator(QRegularExpression(r'^[0-9]{0,11}$'))
        self.profilePhone.setValidator(phone_validator)

        # Connect phone formatting
        self.profilePhone.textChanged.connect(self.on_profile_phone_changed)

        # Email validation will be handled in the save method
    def on_profile_phone_changed(self, text):
        """Real-time phone number formatting for profile phone"""
        if not text:
            return

        cursor_pos = self.profilePhone.cursorPosition()

        # Auto-format from 09 to +639 in real-time
        if text.startswith('09') and len(text) >= 2:
            if len(text) == 11:  # 09 + 9 digits = complete number
                formatted = '+63' + text[1:]
                if formatted != text:
                    self.profilePhone.textChanged.disconnect(self.on_profile_phone_changed)
                    self.profilePhone.setText(formatted)
                    self.profilePhone.textChanged.connect(self.on_profile_phone_changed)
                    self.profilePhone.setCursorPosition(len(formatted))

            # If user tries to type beyond 11 digits, truncate
            elif len(text) > 11:
                self.profilePhone.textChanged.disconnect(self.on_profile_phone_changed)
                self.profilePhone.setText(text[:11])
                self.profilePhone.textChanged.connect(self.on_profile_phone_changed)
                self.profilePhone.setCursorPosition(cursor_pos)
    def validate_profile_fields(self):
        """Validate profile form fields"""
        errors = []

        # Validate required fields
        if not self.profileFullName.text().strip():
            errors.append("Full name is required")
            self.profileFullName.setStyleSheet(error_style)
        else:
            self.profileFullName.setStyleSheet(default_style)

        if not self.profileUserName.text().strip():
            errors.append("Username is required")
            self.profileUserName.setStyleSheet(error_style)
        else:
            self.profileUserName.setStyleSheet(default_style)

        # Validate email
        email = self.profileEmail.text().strip()
        if not email:
            errors.append("Email is required")
            self.profileEmail.setStyleSheet(error_style)
        elif not self.validate_email(email):
            errors.append("Please enter a valid email address")
            self.profileEmail.setStyleSheet(error_style)
        else:
            self.profileEmail.setStyleSheet(default_style)

        # Validate phone
        phone = self.profilePhone.text().strip()
        if not phone:
            errors.append("Phone number is required")
            self.profilePhone.setStyleSheet(error_style)
        elif not self.validate_phone_number(phone):
            errors.append("Phone number must be 09XXXXXXXXX or +63XXXXXXXXXX format")
            self.profilePhone.setStyleSheet(error_style)
        else:
            self.profilePhone.setStyleSheet(default_style)

        return errors
    def verify_password(self, password):
        try:
            # Get current username from your logged-in user data
            username = self.current_user['username']

            success, response = desktop_login(username, password)
            return success

        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    def save_profile_changes(self):
        """Save the updated profile data"""
        # Validate fields
        errors = self.validate_profile_fields()

        if errors:
            message = "Please fix the following errors:\n• " + "\n• ".join(errors)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return
            # Validate password
        password = self.passForConfirm.text().strip()
        if not password:
            toast = Toast(self, "Please enter your password to confirm changes", icon_path="Icons/warning.png")
            toast.show_toast()
            self.passForConfirm.setStyleSheet(error_style)
            return
        else:
            self.passForConfirm.setStyleSheet(default_style)

        # Verify password using the SAME login logic
        if not self.verify_password(password):
            toast = Toast(self, "Incorrect password! Please try again.", icon_path="Icons/warning.png")
            toast.show_toast()
            self.passForConfirm.setStyleSheet(error_style)
            self.passForConfirm.clear()
            self.passForConfirm.setFocus()
            return
        # Prepare data for API
        profile_data = {
            "full_name": self.profileFullName.text().strip(),
            "email": self.profileEmail.text().strip(),
            "phone": self.profilePhone.text().strip()
        }

        # Send update request
        if self.update_user_profile(profile_data):
            toast = Toast(self, "Profile updated successfully!", icon_path="Icons/check.png")
            toast.show_toast()
            self.profileEdit_cancel()  # Return to view mode
        else:
            toast = Toast(self, "Failed to update profile!", icon_path="Icons/warning.png")
            toast.show_toast()
    def update_user_profile(self, profile_data):
        """Send PATCH request to update user profile"""
        try:
            user_id = self.current_user['id']
            response = requests.patch(
                f"{API_BASE_URL}/api/desktop-users/{user_id}/",
                json=profile_data
            )

            if response.status_code == 200:
                # Update current user data
                updated_user = response.json()
                self.current_user.update(updated_user)
                return True
            else:
                print(f"Update failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    def profileEdit_cancel(self):
        """Cancel editing and revert to original data"""
        self.settingsProfileEditBtn.show()
        self.settingsProfileSaveBtn.hide()
        self.settingsProfileCancelBtn.hide()

        # Disable fields
        self.profileFullName.setEnabled(False)
        self.profileEmail.setEnabled(False)
        self.profilePhone.setEnabled(False)

        self.passwordFrame.hide()
        self.spacer.show()
        # Reset styles to default
        self.profileFullName.setStyleSheet(default_style)
        self.profileEmail.setStyleSheet(default_style)
        self.profilePhone.setStyleSheet(default_style)

        # Reload original data
        self.load_user_profile(self.current_user)

        # Disconnect signals to prevent multiple connections
        try:
            self.settingsProfileSaveBtn.clicked.disconnect()
            self.settingsProfileCancelBtn.clicked.disconnect()
        except:
            pass
    def load_user_profile(self, current_user):
        self.passwordFrame.hide()
        self.spacer.show()
        id = current_user['id']
        response = requests.get(f"{API_BASE_URL}/api/desktop-users/{id}")
        userData = response.json()

        self.profileFullName.setText(userData["full_name"])
        self.profileUserName.setText(userData["username"])
        self.profileEmail.setText(userData["email"])
        self.profilePhone.setText(userData["phone"])
        self.accountRole.setText(f"Role: {userData['role']}")
        date = self.format_date(userData["created_at"])
        self.MemberSince.setText(f"Member Since: {date}")

        # Apply view style when loading
        self.apply_profile_view_style()
    def apply_profile_view_style(self):
        """Apply the view style to profile fields"""
        for field in [self.profileFullName, self.profileEmail,self.profilePhone]:
            field.setStyleSheet(profile_view_style)
    def apply_profile_edit_style(self):
        """Apply the edit style to profile fields"""
        for field in [self.profileFullName, self.profileEmail, self.profilePhone, self.passForConfirm]:
            field.setStyleSheet(profile_edit_style)
    #    SECURITY TAB
    def setup_security_tab(self):
        """Initialize security tab connections"""
        self.changeUsernameBtn.clicked.connect(self.change_username)
        self.changePasswordBtn.clicked.connect(self.change_password)

        # Clear fields when tab is shown (optional)
        self.securityTab = self.findChild(QWidget, "securityTab")  # Adjust name as needed
        if self.securityTab:
            self.securityTab.installEventFilter(self)
    def change_username(self):
        """Handle username change"""
        new_username = self.profileUserName.text().strip()
        password = self.changeUsernamePass.text().strip()

        # Validate fields
        errors = self.validate_username_fields(new_username, password)
        if errors:
            self.show_security_error("\n• ".join(errors))
            return

        # Verify password
        if not self.verify_password(password):
            self.show_security_error("Incorrect password!")
            self.changeUsernamePass.setStyleSheet(error_style)
            self.changeUsernamePass.clear()
            self.changeUsernamePass.setFocus()
            return

        # Update username via API
        if self.update_username(new_username):
            self.show_security_success("Username updated successfully!")
            self.clear_security_fields()
            self.logout_after_update()
        else:
            self.show_security_error("Failed to update username!")
    def change_password(self):
        """Handle password change"""
        current_password = self.currentPassEdit.text().strip()
        new_password = self.newPassEdit.text().strip()
        confirm_password = self.confirmPassEdit.text().strip()

        # Validate fields
        errors = self.validate_password_fields(current_password, new_password, confirm_password)
        if errors:
            self.show_security_error("\n• ".join(errors))
            return

        # Verify current password is now done in the API, but you can keep frontend verification too
        # Update password via API
        if self.update_password(new_password):
            self.show_security_success("Password updated successfully!")
            self.clear_security_fields()
            self.logout_after_update()
        else:
            self.show_security_error("Failed to update password! Current password may be incorrect.")
    def validate_username_fields(self, new_username, password):
        """Validate username change fields"""
        errors = []

        if not new_username:
            errors.append("New username is required")
            self.profileUserName.setStyleSheet(error_style)
        else:
            self.profileUserName.setStyleSheet(default_style)

        if not password:
            errors.append("Password is required")
            self.changeUsernamePass.setStyleSheet(error_style)
        else:
            self.changeUsernamePass.setStyleSheet(default_style)

        return errors
    def validate_password_fields(self, current_password, new_password, confirm_password):
        """Validate password change fields"""
        errors = []

        if not current_password:
            errors.append("Current password is required")
            self.currentPassEdit.setStyleSheet(error_style)
        else:
            self.currentPassEdit.setStyleSheet(default_style)

        if not new_password:
            errors.append("New password is required")
            self.newPassEdit.setStyleSheet(error_style)
        else:
            self.newPassEdit.setStyleSheet(default_style)

        if not confirm_password:
            errors.append("Please confirm your new password")
            self.confirmPassEdit.setStyleSheet(error_style)
        else:
            self.confirmPassEdit.setStyleSheet(default_style)

        if new_password and confirm_password and new_password != confirm_password:
            errors.append("New passwords do not match")
            self.newPassEdit.setStyleSheet(error_style)
            self.confirmPassEdit.setStyleSheet(error_style)

        if new_password and len(new_password) < 6:  # Minimum password length
            errors.append("New password must be at least 6 characters long")
            self.newPassEdit.setStyleSheet(error_style)

        return errors
    def update_username(self, new_username):
        """Send PATCH request to update username"""
        try:
            user_id = self.current_user['id']
            username_data = {
                "username": new_username
            }

            response = requests.patch(
                f"{API_BASE_URL}/api/desktop-users/{user_id}/",
                json=username_data
            )

            if response.status_code == 200:
                # Update current user data
                updated_user = response.json()
                self.current_user.update(updated_user)
                return True
            else:
                print(f"Username update failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error updating username: {e}")
            return False
    def update_password(self, new_password):
        """Send POST request to change password using the dedicated endpoint"""
        try:
            user_id = self.current_user['id']
            current_password = self.currentPassEdit.text().strip()  # Get current password from field

            password_data = {
                "user_id": user_id,
                "current_password": current_password,
                "new_password": new_password
            }

            response = requests.post(
                f"{API_BASE_URL}/api/desktop-change-password/",  # Use the dedicated endpoint
                json=password_data
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return True
                else:
                    print(f"Password update failed: {data.get('error')}")
                    return False
            else:
                data = response.json()
                print(f"Password update failed: {response.status_code} - {data.get('error')}")
                return False

        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    def clear_security_fields(self):
        """Clear all security tab input fields"""
        self.changeUsernamePass.clear()
        self.currentPassEdit.clear()
        self.newPassEdit.clear()
        self.confirmPassEdit.clear()

        # Reset styles
        for field in [self.changeUsernamePass, self.currentPassEdit, self.newPassEdit, self.confirmPassEdit]:
            field.setStyleSheet(default_style)
    def show_security_success(self, message):
        """Show success message for security operations"""
        toast = Toast(self, message, icon_path="Icons/check.png")
        toast.show_toast()
    def show_security_error(self, message):
        """Show error message for security operations"""
        toast = Toast(self, f"Please fix the following:\n• {message}", icon_path="Icons/warning.png")
        toast.show_toast()
    def logout_after_update(self):
        """Logout user after successful security update"""
        # Clear all input fields
        self.clear_security_fields()
        # Show logout confirmation message
        self.show_security_success("Please login again with your updated credentials")

        # Add a small delay before logout
        QTimer.singleShot(2000, self.perform_logout)
    def perform_logout(self):
        """Perform logout using the provided handler"""
        if hasattr(self, 'handle_logout'):
            self.handle_logout()  # This calls main.py's handle_logout which restarts the app
        else:
            # Fallback - just close
            self.close()

    # USER MANAGEMENT TAB
    def setup_user_management_tab(self):
        """Initialize user management tab"""
        self.addAccountBtn.clicked.connect(self.generate_staff_account)
        self.load_staff_accounts()
    def generate_staff_account(self):
        """Generate a new staff account"""
        try:
            if not self.current_user or self.current_user.get('role') != 'admin':
                toast = Toast(self, "Only administrators can create staff accounts", icon_path="Icons/warning.png")
                toast.show_toast()
                return

            # Generate account via API
            response = requests.post(
                f"{API_BASE_URL}/api/desktop-create-staff/",
                json={
                    'admin_id': self.current_user['id'],
                    'full_name': f"Staff User"  # Generic name, can be changed later
                }
            )

            if response.status_code == 201:
                data = response.json()
                staff_account = data['staff_account']
                self.temp_passwords[staff_account['id']] = staff_account['temp_password']
                # Show success message with credentials
                toast = Toast(self, f"Staff account created!\nUsername: {staff_account['username']}\nPassword: {staff_account['temp_password']}", icon_path="Icons/check.png")
                toast.show_toast()

                # Refresh the accounts list
                self.load_staff_accounts()
            else:
                toast = Toast(self, "Failed to create staff account!", icon_path="Icons/warning.png")
                toast.show_toast()


        except Exception as e:
            print(f"Error generating staff account: {e}")
            toast = Toast(self, "Failed to create staff account!", icon_path="Icons/warning.png")
            toast.show_toast()
    def load_staff_accounts(self):
        """Load all staff accounts into the scroll area"""
        try:
            # Clear existing content
            scroll_layout = self.accountUserLayout
            if scroll_layout:
                while scroll_layout.count():
                    child = scroll_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # Fetch staff accounts from API
            response = requests.get(f"{API_BASE_URL}/api/desktop-users/")

            if response.status_code == 200:
                data = response.json()
                staff_accounts = [user for user in data.get('users', []) if user['role'] == 'staff']

                # Create all staff cards at once (like patient cards)
                self.create_staff_cards(staff_accounts)

            else:
                toast = Toast(self, "Failed to load staff accounts!", icon_path="Icons/warning.png")
                toast.show_toast()

        except Exception as e:
            print(f"Error loading staff accounts: {e}")
            toast = Toast(self, "Error loading staff accounts", icon_path="Icons/warning.png")
            toast.show_toast()
    def create_staff_cards(self, accounts):
        """Create multiple staff cards from account data"""
        self.accountCards = []

        for account in accounts:
            card_ui = uic.loadUi("ui-files/accountUsers.ui")
            self.scale_cards([card_ui], base_h=81)
            if not card_ui:
                print("Failed to load staff card UI")
                continue

            # Set account data
            card_ui.userNameLabel.setText(account.get('username', 'Unknown'))

            # ✅ USE THE temp_password FROM BACKEND
            if account.get('show_temp_password', False) and account.get('temp_password'):
                card_ui.passwordLabel.setText(account['temp_password'])
                card_ui.status.setText("Pending Setup")
            elif account.get('force_password_change', True):
                card_ui.passwordLabel.setText("Setup required")
                card_ui.status.setText("Pending Setup")
            else:
                # Account is active
                card_ui.passwordLabel.setText("••••••••")
                card_ui.status.setText("Active")
                card_ui.tempUser.setText("(Active Username)")
                card_ui.tempPass.setText("(Active Password)")

            self.scale_widget_font(card_ui.userNameLabel, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")
            self.scale_widget_font(card_ui.passwordLabel, base_size=14, min_size=8, max_size=25, family="Montserrat Medium")
            self.scale_widget_font(card_ui.status, base_size=14, min_size=8, max_size=25, family="Montserrat Medium")
            # Set up action buttons
            card_ui.resetPassBtn.clicked.connect(lambda checked, acc=account: self.reset_staff_password(acc))
            card_ui.deleteUser.clicked.connect(lambda checked, acc=account: self.delete_staff_account(acc))
            card_ui.setGraphicsEffect(create_card_shadow())

            # Add to scroll area
            scroll_layout = self.accountUserLayout
            scroll_layout.addWidget(card_ui)
            self.accountCards.append(card_ui)
    def reset_staff_password(self, account):
        """Reset staff account password"""
        try:
            if not self.current_user or self.current_user.get('role') != 'admin':
                toast = Toast(self, "Only administrators can reset passwords", icon_path="Icons/warning.png")
                toast.show_toast()
                return

            reply = QMessageBox.question(
                self,
                "Reset Password",
                f"Reset password for {account['username']}? This will generate new temporary credentials.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Call reset API (you'll need to create this endpoint)
                response = requests.post(
                    f"{API_BASE_URL}/api/desktop-reset-password/",  # You'll need to create this
                    json={
                        'admin_id': self.current_user['id'],
                        'staff_id': account['id']
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    toast = Toast(self, f"Password reset!\nNew password: {data['new_password']}", icon_path="Icons/check.png")
                    toast.show_toast()
                    self.load_staff_accounts()  # Refresh
                else:
                    toast = Toast(self, "Reset failed",icon_path="Icons/warning.png")
                    toast.show_toast()

        except Exception as e:
            toast = Toast(self, "Failed to reset password", icon_path="Icons/warning.png")
            toast.show_toast()
            print(f"Error resetting password: {e}")
    def delete_staff_account(self, account):
        """Delete staff account"""
        try:
            if not self.current_user or self.current_user.get('role') != 'admin':
                toast = Toast(self, "Only administrators can delete accounts", icon_path="Icons/warning.png")
                toast.show_toast()
                return

            reply = QMessageBox.question(
                self,
                "Delete Account",
                f"Delete {account['username']}? This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                response = requests.delete(f"{API_BASE_URL}/api/desktop-users/{account['id']}/")

                if response.status_code == 204:
                    toast = Toast(self, "Account deleted successfully", icon_path="Icons/check.png")
                    toast.show_toast()
                    self.load_staff_accounts()  # Refresh
                else:
                    toast = Toast(self, "Delete Failed", icon_path="Icons/warning.png")
                    toast.show_toast()

        except Exception as e:
            print(f"Error deleting account: {e}")
            toast = Toast(self, "Failed to delete account", icon_path="Icons/warning.png")
            toast.show_toast()

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
        self.scale_label_pixmap(self.clinicIconP5, min_size=64, max_size=256)
        self.scale_label_pixmap(self.clinicIconP6, min_size=64, max_size=256)
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
        self.scale_widget_font(self.pageHeader6, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader8, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
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

        self.scale_cards(self.accountCards, base_h=90)
        for i, card in enumerate(getattr(self, "accountCards", []), start=1):
            for userNameLabel in card.findChildren(QLabel, "userNameLabel"):
                self.scale_widget_font(userNameLabel,base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")

            for passwordLabel in card.findChildren(QLabel, "passwordLabel"):
                self.scale_widget_font(passwordLabel, base_size=14, min_size=8, max_size=35, family="Montserrat Medium")

            for status in card.findChildren(QLabel, "status"):
                self.scale_widget_font(status, base_size=14, min_size=8, max_size=35, family="Montserrat Medium")

            if card.profileIcon:
                self.scale_label_pixmap(card.profileIcon, min_size=50, max_size=120)

    def refresh_analytics(self):
        print("Refreshing analytics...")
        self.setup_bar_graph()
        self.setup_pie_graph()
    def setup_bar_graph(self):

        data = fetch_json(f"{API_BASE_URL}/api/serviceCounts")
        if data is None:
            print("BAR GRAPH ERROR — No data")
            return

        set0 = QBarSet("Services")
        values = list(data.values())
        categories = list(data.keys())
        for v in values:
            set0.append(v)

        series = QBarSeries()
        series.append(set0)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Total every service")

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = self.ServiceBarGraph.layout()
        if layout is None:
            layout = QVBoxLayout(self.ServiceBarGraph)

        # Remove previous charts
        while layout.count():
            old = layout.takeAt(0)
            if old.widget():
                old.widget().deleteLater()

        layout.addWidget(chart_view)
    def setup_pie_graph(self):

        data = fetch_json(f"{API_BASE_URL}/api/speciesCounts")
        if data is None:
            print("PIE GRAPH ERROR — No data")
            return

        series = QPieSeries()
        series.append(f"Dogs: {data.get('dogs', 0)}", data.get("dogs", 0))
        series.append(f"Cats: {data.get('cats', 0)}", data.get("cats", 0))
        series.append(f"Others: {data.get('others', 0)}", data.get("others", 0))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Species Distribution")

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)


        layout = self.SpeciesPieGraph.layout()
        if layout is None:
            layout = QVBoxLayout(self.SpeciesPieGraph)

        # Remove previous charts
        while layout.count():
            old = layout.takeAt(0)
            if old.widget():
                old.widget().deleteLater()

        layout.addWidget(chart_view)



    def setup_day_radio_groups(self):
        """Setup radio button groups for each day with 3 options"""
        # NEW: Map of day prefixes to their 3 radio buttons
        day_radio_mapping = {
            'mon': [self.radioButton_open_mon, self.radioButton_appt_mon, self.radioButton_closed_mon],
            'teus': [self.radioButton_open_teus, self.radioButton_appt_teus, self.radioButton_closed_teus],
            'wed': [self.radioButton_open_wed, self.radioButton_appt_wed, self.radioButton_closed_wed],
            'thurs': [self.radioButton_open_thurs, self.radioButton_appt_thurs, self.radioButton_closed_thurs],
            'fri': [self.radioButton_open_fri, self.radioButton_appt_fri, self.radioButton_closed_fri],
            'sat': [self.radioButton_open_sat, self.radioButton_appt_sat, self.radioButton_closed_sat],
            'sun': [self.radioButton_open_sun, self.radioButton_appt_sun, self.radioButton_closed_sun]
        }

        for day_prefix, radio_buttons in day_radio_mapping.items():
            btn_group = QButtonGroup(self)
            btn_group.setExclusive(True)  # CHANGE: Set to True for proper radio behavior
            for radio_btn in radio_buttons:
                if radio_btn:
                    btn_group.addButton(radio_btn)
                    # Connect to update time picker state
                    radio_btn.toggled.connect(lambda checked, prefix=day_prefix:
                                              self.on_day_status_changed(prefix, checked))
    def on_day_status_changed(self, day_prefix, checked):
        """Update time picker state when day status changes"""
        if checked:
            # Enable/disable time pickers based on status
            status = self.get_day_status(day_prefix)
            if status == 'open':
                self.set_time_pickers_enabled(day_prefix, True)
            else:
                self.set_time_pickers_enabled(day_prefix, False)
    def load_office_hours(self):
        """Load office hours from API"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/office-hours/",
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                office_hours = response.json()
                self.populate_office_hours(office_hours)
            else:
                # Show error toast
                toast = Toast(self, "Failed to load office hours",
                              icon_path="Icons/error.png", is_error=True)
                toast.show_toast()

        except Exception as e:
            # Show error toast
            toast = Toast(self, f"Failed to load office hours: {str(e)}",
                          icon_path="Icons/error.png", is_error=True)
            toast.show_toast()
    def setup_office_hours(self):
        """Initialize office hours tab"""
        # Connect buttons
        self.saveHrsBtn.clicked.connect(self.save_office_hours)
        self.resetHrsBtn.clicked.connect(self.show_reset_confirmation)  # Changed to show confirmation

        # Setup radio button groups for each day
        self.setup_day_radio_groups()

        # Setup QTimeEdit display format for all days
        self.setup_time_edit_formats()

        # Load current office hours
        self.load_office_hours()
    def setup_time_edit_formats(self):
        """Set display format for all QTimeEdit widgets"""
        days = ['mon', 'teus', 'wed', 'thurs', 'fri', 'sat', 'sun']

        for day in days:
            start_edit = getattr(self, f'{day}Start', None)
            end_edit = getattr(self, f'{day}End', None)

            for time_edit in [start_edit, end_edit]:
                if time_edit:
                    # Set 12-hour format with AM/PM
                    time_edit.setDisplayFormat("h:mm AP")
                    # Set time range (optional)
                    time_edit.setMinimumTime(QTime(0, 0))
                    time_edit.setMaximumTime(QTime(23, 59))
    def populate_office_hours(self, office_hours):
        """Populate UI with office hours data"""
        day_mapping = {
            'monday': 'mon',
            'tuesday': 'teus',
            'wednesday': 'wed',
            'thursday': 'thurs',
            'friday': 'fri',
            'saturday': 'sat',
            'sunday': 'sun'
        }

        for day_data in office_hours:
            day_code = day_data.get('day')
            ui_prefix = day_mapping.get(day_code)

            if not ui_prefix:
                continue

            # Set status
            status = day_data.get('status', 'open')

            # Get all 3 radio buttons for this day
            open_btn = getattr(self, f'radioButton_open_{ui_prefix}', None)
            appt_btn = getattr(self, f'radioButton_appt_{ui_prefix}', None)
            closed_btn = getattr(self, f'radioButton_closed_{ui_prefix}', None)

            # Uncheck all first
            for btn in [open_btn, appt_btn, closed_btn]:
                if btn:
                    btn.setChecked(False)

            # Check the appropriate radio button based on status
            if status == 'open' and open_btn:
                open_btn.setChecked(True)
                self.set_time_pickers_enabled(ui_prefix, True)
            elif status == 'appointment_only' and appt_btn:
                appt_btn.setChecked(True)
                self.set_time_pickers_enabled(ui_prefix, False)
            elif status == 'closed' and closed_btn:
                closed_btn.setChecked(True)
                self.set_time_pickers_enabled(ui_prefix, False)

            # Set time values if status is open
            if status == 'open':
                start_time = day_data.get('start_time')
                end_time = day_data.get('end_time')
                if start_time and end_time:
                    self.set_time_values(ui_prefix, start_time, end_time)
    def set_time_values(self, day_prefix, start_time, end_time):
        """Set time values in the UI QTimeEdit widgets"""
        # Get QTimeEdit widgets
        start_time_edit = getattr(self, f'{day_prefix}Start', None)
        end_time_edit = getattr(self, f'{day_prefix}End', None)

        if start_time_edit and end_time_edit:
            # Parse time strings to QTime
            start_qtime = self.time_from_string(start_time)
            end_qtime = self.time_from_string(end_time)

            # Set the times
            start_time_edit.setTime(start_qtime)
            end_time_edit.setTime(end_qtime)
    def time_from_string(self, time_str):
        """Convert time string (HH:MM:SS) to QTime"""
        if not time_str:
            return QTime(8, 0)  # Default 8:00 AM

        try:
            # Parse HH:MM:SS
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts) >= 2:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    return QTime(hours, minutes)
        except (ValueError, TypeError):
            pass

        return QTime(8, 0)  # Default fallback
    def get_time_from_widgets(self, day_prefix):
        """Get start and end times from QTimeEdit widgets"""
        start_time_edit = getattr(self, f'{day_prefix}Start', None)
        end_time_edit = getattr(self, f'{day_prefix}End', None)

        if not start_time_edit or not end_time_edit:
            return None, None

        start_time = start_time_edit.time()
        end_time = end_time_edit.time()

        return start_time, end_time
    def set_time_pickers_enabled(self, day_prefix, enabled):
        """Enable or disable time pickers for a day"""
        # Get QTimeEdit widgets
        start_time_edit = getattr(self, f'{day_prefix}Start', None)
        end_time_edit = getattr(self, f'{day_prefix}End', None)

        for widget in [start_time_edit, end_time_edit]:
            if widget:
                widget.setEnabled(enabled)
                # Visual feedback
                if enabled:
                    widget.setStyleSheet("")
                else:
                    widget.setStyleSheet("background-color: #f0f0f0; color: #888;")
    def collect_office_hours_data(self):
        """Collect office hours data from UI"""
        day_mapping = {
            'mon': 'monday',
            'teus': 'tuesday',
            'wed': 'wednesday',
            'thurs': 'thursday',
            'fri': 'friday',
            'sat': 'saturday',
            'sun': 'sunday'
        }

        office_hours = []

        for ui_prefix, day_name in day_mapping.items():
            # Determine status based on radio buttons
            status = self.get_day_status(ui_prefix)

            day_data = {
                'day': day_name,
                'status': status,
                'start_time': None,
                'end_time': None
            }

            # If status is open, get times from QTimeEdit widgets
            if status == 'open':
                start_time, end_time = self.get_time_from_widgets(ui_prefix)

                if start_time and end_time:
                    # Convert QTime to string format HH:MM:SS
                    day_data['start_time'] = start_time.toString('HH:mm:ss')
                    day_data['end_time'] = end_time.toString('HH:mm:ss')

            office_hours.append(day_data)

        return office_hours
    def reset_office_hours(self):
        """Perform the actual reset of office hours"""
        try:
            # Define default hours
            default_hours = [
                {'day': 'monday', 'status': 'open', 'start_time': '08:00:00', 'end_time': '18:00:00'},
                {'day': 'tuesday', 'status': 'open', 'start_time': '08:00:00', 'end_time': '18:00:00'},
                {'day': 'wednesday', 'status': 'open', 'start_time': '08:00:00', 'end_time': '18:00:00'},
                {'day': 'thursday', 'status': 'open', 'start_time': '08:00:00', 'end_time': '18:00:00'},
                {'day': 'friday', 'status': 'open', 'start_time': '08:00:00', 'end_time': '18:00:00'},
                {'day': 'saturday', 'status': 'open', 'start_time': '09:00:00', 'end_time': '16:00:00'},
                {'day': 'sunday', 'status': 'appointment_only', 'start_time': None, 'end_time': None}
            ]

            # Populate UI with default values
            self.populate_office_hours(default_hours)

            # Save defaults to database
            response = requests.post(
                f"{API_BASE_URL}/api/office-hours/update/",
                json=default_hours,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                # SUCCESS TOAST - No buttons, auto-dismiss
                toast = Toast(self, "Office hours reset to default values!", icon_path="Icons/check.png")
                toast.show_toast()
            else:
                # ERROR TOAST - Use whatever error styling you have
                toast = Toast(self, "Failed to reset office hours")
                toast.show_toast()

        except Exception as e:
            # ERROR TOAST
            toast = Toast(self, "Failed to reset office hours")
            toast.show_toast()

        # Always restore card and close it
        self.restore_confirm_card_default()
        self.confirmCard.close()
    def save_office_hours(self):
        """Save office hours to API"""
        try:
            office_hours_data = self.collect_office_hours_data()

            response = requests.post(
                f"{API_BASE_URL}/api/office-hours/update/",
                json=office_hours_data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                # SUCCESS TOAST
                toast = Toast(self, "Office hours saved successfully!", icon_path="Icons/check.png")
                toast.show_toast()
                self.load_office_hours()  # Reload to confirm
            else:
                # ERROR TOAST
                toast = Toast(self, "Failed to save office hours")
                toast.show_toast()

        except Exception as e:
            # ERROR TOAST
            toast = Toast(self, "Failed to save office hours")
            toast.show_toast()
    def get_day_status(self, day_prefix):
        """Get status for a specific day from radio buttons"""
        # NEW: Get all 3 radio buttons
        open_btn = getattr(self, f'radioButton_open_{day_prefix}', None)
        appt_btn = getattr(self, f'radioButton_appt_{day_prefix}', None)
        closed_btn = getattr(self, f'radioButton_closed_{day_prefix}', None)

        if open_btn and open_btn.isChecked():
            return 'open'
        elif appt_btn and appt_btn.isChecked():
            return 'appointment_only'
        elif closed_btn and closed_btn.isChecked():
            return 'closed'
        else:
            return 'open'  # Default if nothing is checked
    def show_reset_confirmation(self):
        """Show confirmation for resetting office hours"""
        # Configure for reset
        self.confirmCard.confirmationMessage.setText(
            "Are you sure you want to reset office hours to default values?"
        )

        # Change button texts
        self.confirmCard.yesButton.setText("RESET")
        self.confirmCard.noButton.setText("CANCEL")


        self.confirmCard.yesButton.setStyleSheet(reset_yes_style)
        self.confirmCard.noButton.setStyleSheet(reset_no_style)

        # Disconnect old signals
        try:
            self.confirmCard.yesButton.clicked.disconnect()
            self.confirmCard.noButton.clicked.disconnect()
        except:
            pass

        # Connect reset actions
        self.confirmCard.yesButton.clicked.connect(self.reset_office_hours)
        self.confirmCard.noButton.clicked.connect(self.cancel_reset_and_restore)

        # Show the card
        self.confirmCard.show_card()
    def cancel_reset_and_restore(self):
        """Cancel reset and restore original configuration"""
        self.confirmCard.close()
        self.restore_confirm_card_default()
    def restore_confirm_card_default(self):
        """Restore confirm card to default delete configuration"""
        # Restore message
        self.confirmCard.confirmationMessage.setText(
            self.confirmCard_original_config['message']
        )

        # Restore button texts
        self.confirmCard.yesButton.setText(self.confirmCard_original_config['yes_text'])
        self.confirmCard.noButton.setText(self.confirmCard_original_config['no_text'])


        self.confirmCard.yesButton.setStyleSheet(original_yes_style)
        self.confirmCard.noButton.setStyleSheet(original_no_style)

        # Reconnect original delete actions
        try:
            self.confirmCard.yesButton.clicked.disconnect()
            self.confirmCard.noButton.clicked.disconnect()
        except:
            pass

        self.confirmCard.yesButton.clicked.connect(self.deleteFunction.really_delete)
        self.confirmCard.noButton.clicked.connect(self.deleteFunction.cancel_delete)


import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller (.exe)"""
    import sys, os
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles files to _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Use the project root as base in dev
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# Ensure PyQt6.uic is explicitly imported so PyInstaller includes it
from http.client import responses

# ETO ANG SAGGOT
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)      # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QWidget, QComboBox, QButtonGroup, QMessageBox, \
    QCalendarWidget, QToolButton, QTextEdit, QPushButton, QFrame, QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QSize, \
    QParallelAnimationGroup, QTimer, QRegularExpression, QSettings, QTime, QEvent, QObject, pyqtSignal
from PyQt6.QtGui import QFontDatabase, QPixmap,QIntValidator, QRegularExpressionValidator
from uiLogic import UIHandler
from input_styles import *
from toast import Toast
import resources_rc
from Desktop_Application.Frontend.api_client import add_new_patient, add_new_pet, add_new_service, desktop_login, update_site_about
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
from async_helper import AsyncHelper
from loading_overlay import LoadingOverlay
from ui_utils import setup_password_toggle
import requests
import webbrowser
import json
import threading

from PyQt6.QtGui import QColor, QPainter, QFont, QBrush
from PyQt6.QtWidgets import QVBoxLayout
from analytics import fetch_json




class _UiInvoker(QObject):
    """Executes callables on the Qt main thread via queued signals."""

    run = pyqtSignal(object)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.run.connect(self._on_run)

    def _on_run(self, fn):
        try:
            if callable(fn):
                fn()
        except Exception:
            # Never crash the UI thread for best-effort updates.
            pass


class MainUI(QMainWindow):
    def __init__(self, user_data=None, startup_progress=None):
        super(MainUI, self).__init__()

        # Thread-safe UI callback bridge (used by worker threads).
        self._ui_invoker = _UiInvoker(self)

        # Optional callback for startup progress reporting (value 0-100, title, subtitle)
        self._startup_progress = startup_progress

        def _sp(value: int, title: str = None, subtitle: str = None):
            try:
                if callable(self._startup_progress):
                    self._startup_progress(int(value), title, subtitle)
            except Exception:
                pass

        _sp(72, "Opening PetMate...", "Loading dashboard UI")
        uic.loadUi("ui-files/Home.ui", self)

        _sp(76, "Opening PetMate...", "Initializing helpers")

        # ⭐ Initialize Async Helper for smooth API calls
        self.api = AsyncHelper(self, base_url=API_BASE_URL)

        # Initialize delete and update functions
        self.deleteFunction = Delete(self)
        self.updateFunction = Update(self)

        _sp(80, "Opening PetMate...", "Wiring UI components")

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
        self.setup_about_us_editor()

        # Ensure deleteClientsSearch is assigned for search logic
        from PyQt6.QtWidgets import QLineEdit
        self.deleteClientsSearch = self.findChild(QLineEdit, "deleteClientsSearch")

        _sp(86, "Opening PetMate...", "Loading user settings")

        #Settings
        self.UserManagementTabBtn.hide()
        self.role_base()
        self.load_user_profile(self.current_user)
        self.setup_security_tab()
        self.setup_user_management_tab()

        _sp(90, "Opening PetMate...", "Preparing initial data")

        #CRITICAL: Initialize state variables ONCE
        self.selected_patient_id = None
        self.selected_service_id = None
        self.selected_pet_id = None

        # Profile cache signatures (used to avoid re-render if refresh returns same data)
        self._pets_sig_by_owner: dict[int, str] = {}
        self._services_sig_by_pet: dict[int, str] = {}
        self._pet_sig_by_id: dict[int, str] = {}

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
        # Add pagination state for scheduled services
        self.scheduled_current_page = 1
        self.scheduled_total_pages = 1
        self.scheduled_total_count = 0
        self.scheduled_search_term = ""
        self.scheduled_current_filter = None

        # Search state
        self.current_search_term = ""
        self.is_searching = False

        self.setup_scheduled_search()

        #Pet species comboBox
        self.setup_species_field()

        # Deleted patients pagination state
        self.deleted_patient_currentPage = 1
        self.deleted_total_patient_pages = 1
        self.deleted_total_patient_count = 0

        # Initial page setup
        self.stackedWidget.setCurrentIndex(0)
        self.set_current_month_in_combobox()

        # Defer data loading to after window is shown - don't block initialization!
        # These will load in background after UI is displayed
        QTimer.singleShot(0, lambda: self.load_patients(1, search_term=None, force_refresh=True))
        QTimer.singleShot(0, lambda: self.load_scheduled_services())
        QTimer.singleShot(0, lambda: self.load_staff_accounts())

        _sp(94, "Opening PetMate...", "Finalizing")

        # Setup remaining UI elements
        self.setup_shadow()
        self.setup_all_back_buttons()
        self.setup_input_shadows()
        self.monthComboBox.currentTextChanged.connect(
            lambda: self.load_scheduled_services(1, self.scheduled_search_term)
        )

        # Setup search
        self.setup_search()

        # Update back button visibility
        self.update_back_button_visibility()

        # Birthday date limits
        self.Bday.setMinimumDate(QDate(1900, 1, 1))
        self.Bday.setMaximumDate(QDate.currentDate())

        self.temp_passwords = {}

        # Analytics/Homepage - defer to not block startup
        self.stackedWidget.setCurrentIndex(0)
        QTimer.singleShot(0, lambda: self.appointments_today())
        QTimer.singleShot(0, lambda: self.setup_bar_graph())
        QTimer.singleShot(0, lambda: self.setup_pie_graph())

        self.homeBtn.clicked.connect(self.refresh_analytics)
        self.homeBtn_2.clicked.connect(self.refresh_analytics)

        self.setup_office_hours()
        QTimer.singleShot(0, lambda: self.load_service_types_to_main_combobox())

        _sp(97, "Opening PetMate...", "Almost ready")

    # -------------------- ABOUT US EDITOR (Home.ui) --------------------
    def setup_about_us_editor(self):
        """Wire About section controls on the Home screen.

        Uses:
          - titleTextEdit (headline)
          - descriptionTextEdit (body)
          - imageLabel (preview)
          - chooseImage (pick file)
          - saveChanges (POST update)
        """
        self._about_selected_image_path: str | None = None
        self._about_current_image_url: str | None = None
        # No loading modal for About saves; use Toast only.

        if hasattr(self, 'imageLabel'):
            self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if hasattr(self, 'chooseImage'):
            self.chooseImage.clicked.connect(self.on_choose_about_image)

        if hasattr(self, 'saveChanges'):
            self.saveChanges.clicked.connect(self.on_save_about_changes)

        # Load existing about content from backend (non-blocking)
        try:
            self.api.get(
                '/api/about/',
                on_success=self._on_about_loaded,
                on_error=lambda err: Toast(self, "Failed to load About content", icon_path="Icons/warning.png").show_toast(),
                use_cache=False,
                timeout=15,
            )
        except Exception:
            # If async helper isn't ready for any reason, silently keep defaults
            pass

    def _on_about_loaded(self, data):
        try:
            title = (data or {}).get('title') or ''
            body = (data or {}).get('body') or ''
            image_url = (data or {}).get('image_url')

            if hasattr(self, 'titleTextEdit'):
                self.titleTextEdit.setPlainText(title)
            if hasattr(self, 'descriptionTextEdit'):
                self.descriptionTextEdit.setPlainText(body)

            self._about_current_image_url = image_url
            if image_url:
                self._load_about_image_from_url(image_url)
            else:
                if hasattr(self, 'imageLabel'):
                    self.imageLabel.setText('No Image')
                    self.imageLabel.setPixmap(QPixmap())
        except Exception:
            Toast(self, "Failed to render About content", icon_path="Icons/warning.png").show_toast()

    def on_choose_about_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select About Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp *.gif)"
        )

        if not file_path:
            return

        self._about_selected_image_path = file_path
        self._set_about_image_preview_from_file(file_path)

    def _set_about_image_preview_from_file(self, file_path: str):
        if not hasattr(self, 'imageLabel'):
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.imageLabel.setText('Failed to load image')
            self.imageLabel.setPixmap(QPixmap())
            return

        # Respect the size set in Qt Designer (min/max). Use maximumSize when it's meaningful.
        target_size = self.imageLabel.maximumSize()
        if target_size.width() >= 16777215 or target_size.height() >= 16777215:
            target_size = self.imageLabel.size()
        scaled = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.imageLabel.setPixmap(scaled)
        self.imageLabel.setText('')

    def _load_about_image_from_url(self, url: str):
        """Download and preview the current image_url (non-blocking)."""
        if not hasattr(self, 'imageLabel'):
            return

        # If backend stores a relative path (e.g. /media/about/x.png), prefix with API base.
        if isinstance(url, str) and not url.startswith('http'):
            url = f"{API_BASE_URL}{url}"

        def worker():
            try:
                res = requests.get(url, timeout=15)
                if res.status_code != 200:
                    raise Exception(f"HTTP {res.status_code}")
                content = res.content
            except Exception:
                # Ensure UI update runs on the main thread.
                self._ui_invoker.run.emit(lambda: self.imageLabel.setText('No Image'))
                return

            def apply_pixmap():
                pixmap = QPixmap()
                if not pixmap.loadFromData(content):
                    self.imageLabel.setText('No Image')
                    self.imageLabel.setPixmap(QPixmap())
                    return

                target_size = self.imageLabel.maximumSize()
                if target_size.width() >= 16777215 or target_size.height() >= 16777215:
                    target_size = self.imageLabel.size()

                scaled = pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.imageLabel.setPixmap(scaled)
                self.imageLabel.setText('')

            # Ensure UI update runs on the main thread.
            self._ui_invoker.run.emit(apply_pixmap)

        threading.Thread(target=worker, daemon=True).start()

    def on_save_about_changes(self):
        title = self.titleTextEdit.toPlainText().strip() if hasattr(self, 'titleTextEdit') else ''
        body = self.descriptionTextEdit.toPlainText().strip() if hasattr(self, 'descriptionTextEdit') else ''

        # Only send fields that are non-empty; keeps existing values when left blank.
        title_payload = title if title else None
        body_payload = body if body else None
        image_path = self._about_selected_image_path

        if not title_payload and not body_payload and not image_path:
            Toast(self, "Nothing to save", icon_path="Icons/warning.png").show_toast()
            return

        # Disable controls while saving.
        if hasattr(self, 'saveChanges'):
            self.saveChanges.setEnabled(False)
        if hasattr(self, 'chooseImage'):
            self.chooseImage.setEnabled(False)

        # Optional immediate feedback.
        Toast(self, "Saving changes...", icon_path="Icons/check.png").show_toast()

        def worker():
            try:
                ok, resp = update_site_about(title=title_payload, body=body_payload, image_path=image_path)
            except Exception as e:
                ok, resp = False, {"error": str(e)}

            def finish():
                if hasattr(self, 'saveChanges'):
                    self.saveChanges.setEnabled(True)
                if hasattr(self, 'chooseImage'):
                    self.chooseImage.setEnabled(True)

                if ok:
                    Toast(self, "About section updated", icon_path="Icons/check.png").show_toast()
                    # If server returns new image_url, show it (and clear local pending image)
                    new_url = (resp or {}).get('image_url')
                    if new_url:
                        self._about_current_image_url = new_url
                        self._about_selected_image_path = None
                        self._load_about_image_from_url(new_url)
                else:
                    err = (resp or {}).get('error') or 'Failed to update'
                    Toast(self, err, icon_path="Icons/warning.png").show_toast()

            # Always run UI cleanup on the main thread.
            self._ui_invoker.run.emit(finish)

        threading.Thread(target=worker, daemon=True).start()

    #LAYOUT FOR SCROLL AREAS FOR CARDS
    def setup_layouts(self):
        self.accountUserLayout = self.accountUserScrollAreaContents.layout()
        self.accountUserLayout.setSpacing(10)
        self.accountUserLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # patient list layout
        self.patientListLayout = self.scrollAreaWidgetContents.layout()
        self.patientListLayout.setSpacing(10)
        self.patientListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # deleted patients layout
        if hasattr(self, 'DeletedClientWidgetContents_2'):
            self.deletedPatientListLayout = self.DeletedClientWidgetContents_2.layout()
            self.deletedPatientListLayout.setSpacing(10)
            self.deletedPatientListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self.pendingWebBtn.clicked.connect(lambda: (self.webAppointmentStackWidget.setCurrentIndex(0),
                                                    self.appointmentCard.web_Appointment(1,"pending")))

        self.AcceptedBtn.clicked.connect(lambda: (self.webAppointmentStackWidget.setCurrentIndex(1),
                                                  self.appointmentCard.web_Appointment(1,"accepted")))

        self.DeclinedBtn.clicked.connect(lambda: (self.webAppointmentStackWidget.setCurrentIndex(2),
                                                  self.appointmentCard.web_Appointment(1,"declined")))

        # toggle sched return status Btn
        self.pendingReturnBtn.setCheckable(True)
        self.completeReurnBtn.setCheckable(True)
        self.overdueReturnBtn.setCheckable(True)
        self.returnStackedWidget.setCurrentIndex(0)
        self.returnStatusBtnGroup = QButtonGroup(self)
        for btn in [self.pendingReturnBtn, self.completeReurnBtn, self.overdueReturnBtn]:
            self.returnStatusBtnGroup.addButton(btn)
        self.pendingReturnBtn.setChecked(True)
        self.pendingReturnBtn.clicked.connect(lambda: (
            self.returnStackedWidget.setCurrentIndex(0),
            self.show_loading_label(self.pendingLayout, "Loading scheduled services..."),
            QTimer.singleShot(0, lambda: self.load_scheduled_services(1, self.scheduled_search_term))
        ))
        self.completeReurnBtn.clicked.connect(lambda: (
            self.returnStackedWidget.setCurrentIndex(1),
            self.show_loading_label(self.completedLayout, "Loading scheduled services..."),
            QTimer.singleShot(0, lambda: self.load_scheduled_services(1, self.scheduled_search_term))
        ))
        self.overdueReturnBtn.clicked.connect(lambda: (
            self.returnStackedWidget.setCurrentIndex(2),
            self.show_loading_label(self.overdueLayout, "Loading scheduled services..."),
            QTimer.singleShot(0, lambda: self.load_scheduled_services(1, self.scheduled_search_term))
        ))

        #Web management stackwidget
        self.aboutUsTab.setChecked(True)
        self.serviceTab.setChecked(True)
        self.officeHoursTab.setChecked(True)
        self.webManagementStackedWidget.setCurrentIndex(2)
        self.webManagementStatusBtnGroup = QButtonGroup(self)
        for btn in [ self.serviceTab, self.officeHoursTab,self.aboutUsTab]:
            self.webManagementStatusBtnGroup.addButton(btn)
        self.aboutUsTab.setChecked(True)
        self.aboutUsTab.clicked.connect(lambda: self.webManagementStackedWidget.setCurrentIndex(2))
        self.serviceTab.clicked.connect(lambda: self.webManagementStackedWidget.setCurrentIndex(0))
        self.officeHoursTab.clicked.connect(lambda: self.webManagementStackedWidget.setCurrentIndex(1))


        #Settings Stack widget
        # toggle walk-in status Btn
        self.profileTabBtn.setCheckable(True)
        self.securityTabBtn.setCheckable(True)
        self.UserManagementTabBtn.setCheckable(True)
        
        # Deleted clients tab button (pushButton_2 from UI)
        if hasattr(self, 'pushButton_2'):
            self.deletedClientsTabBtn = self.pushButton_2
            self.deletedClientsTabBtn.setCheckable(True)
        
        self.settingsStactWidget.setCurrentIndex(0)
        self.settingsBtnGroup = QButtonGroup(self)
        
        # Add all tab buttons to the group
        tab_buttons = [self.profileTabBtn, self.securityTabBtn, self.UserManagementTabBtn]
        if hasattr(self, 'deletedClientsTabBtn'):
            tab_buttons.append(self.deletedClientsTabBtn)
        
        for btn in tab_buttons:
            self.settingsBtnGroup.addButton(btn)
        
        self.profileTabBtn.setChecked(True)
        self.profileTabBtn.clicked.connect(lambda: self.settingsStactWidget.setCurrentIndex(0))
        self.securityTabBtn.clicked.connect(lambda: self.settingsStactWidget.setCurrentIndex(1))
        
        # Connect deleted clients tab button
        if hasattr(self, 'deletedClientsTabBtn'):
            self.deletedClientsTabBtn.clicked.connect(lambda: self.on_deleted_clients_tab_clicked())
        
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
        
        # Load data when navigating to appointment page - deferred to not block UI
        if index == 3:  # Appointment page
            if hasattr(self, 'appointmentCard'):
                # Use QTimer to defer loading until after page is shown
                QTimer.singleShot(0, lambda: self.appointmentCard.load_appointments(1, "pending", search_term=None))
        
        # Load fresh patient data when navigating to Patient Records page
        if index == 2:  # Patient Records page
            # Clear search bar and reset search state
            if hasattr(self, 'searchBar'):
                self.searchBar.clear()
            self.current_search_term = ""
            self.is_searching = False
            # Defer loading to not block UI, always force refresh to show new registrations
            QTimer.singleShot(0, lambda: self.load_patients(1, search_term=None, force_refresh=True))
        
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
        self.prescriptionTextedit.setGraphicsEffect(create_card_shadow())
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

        self.reminderBtn.setGraphicsEffect(create_card_shadow())
        self.profileInfoPassShow.setGraphicsEffect(create_card_shadow())
        #settings shadow
        self.changePassFrame.setGraphicsEffect(create_card_shadow())
        self.profileInfoFrame.setGraphicsEffect(create_card_shadow())

        self.appointmentTodayBar.setGraphicsEffect(create_card_shadow())

    #FORM INPUT CHECKER
    def setup_phone_validator(self):
        # Allow common PH formats while typing:
        # - 09XXXXXXXXX (11 digits)
        # - 9XXXXXXXXX (10 digits)
        # - 63XXXXXXXXXX (12 digits)
        # - +63XXXXXXXXXX (13 chars)
        phone_validator = QRegularExpressionValidator(
            QRegularExpression(r'^(?:0\d{0,10}|9\d{0,9}|63\d{0,10}|\+63\d{0,10})$')
        )
        self.phoneNumberEdit.setMaxLength(13)
        self.secondaryPhoneEdit.setMaxLength(13)
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
        # Avoid blocking startup: load AddressJSON asynchronously, then populate provinces.
        self.provinceComboBox.setEnabled(False)
        self.cityComboBox.setEnabled(False)
        self.barangayComboBox.setEnabled(False)

        self.ui_handler.load_address_data_async(
            on_ready=self._on_address_data_ready,
            on_error=lambda err: Toast(self, "Failed to load address data", icon_path="Icons/warning.png").show_toast()
        )
        combo_boxes = [self.provinceComboBox, self.cityComboBox, self.barangayComboBox]
        placeholders = ["Select Province", "Select City", "Select Barangay"]
        for cb, text in zip(combo_boxes, placeholders):
            cb.setEditable(True)
            cb.lineEdit().setReadOnly(False)
            cb.lineEdit().setPlaceholderText(text)
            cb.lineEdit().setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _on_address_data_ready(self):
        try:
            self.ui_handler.load_provinces()
            self.provinceComboBox.setEnabled(True)
        except Exception as e:
            print(f"Failed to populate provinces: {e}")
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

        # Show loading overlay
        self.patient_loading_overlay = LoadingOverlay(self)
        self.patient_loading_overlay.set_message(
            "Adding Patient...",
            "Please wait while we save the patient information"
        )
        self.patient_loading_overlay.show()

        # Store for callback
        self._patient_required_fields = required_fields

        # Use async helper for non-blocking POST request
        self.api.post(
            url="/api/patients/",
            data=data,
            on_success=self._on_patient_added,
            on_error=self._on_patient_error
        )

    def _on_patient_added(self, response):
        """Callback when patient is successfully added"""
        # Hide loading overlay
        if hasattr(self, 'patient_loading_overlay') and self.patient_loading_overlay:
            self.patient_loading_overlay.close()
            self.patient_loading_overlay = None

        # CRITICAL: Invalidate patient cache to ensure fresh data
        self.api.invalidate_cache('/api/patients')
        self.api.invalidate_cache('/api/patient-search')

        self.navigate_to_page(2)
        # Force refresh to ensure new patient appears (bypasses any cache)
        self.load_patients(1, search_term=None, force_refresh=True)

        self.clearInputs()

        # Reset styles to default
        if hasattr(self, '_patient_required_fields'):
            for widget in self._patient_required_fields.values():
                if isinstance(widget, QLineEdit):
                    widget.setStyleSheet(default_style)
                elif isinstance(widget, QComboBox):
                    widget.setStyleSheet(default_combobox_style)

        toast = Toast(self, icon_path="Icons/check.png")
        toast.show_toast()

    def _on_patient_error(self, error_msg):
        """Callback when patient addition fails"""
        # Hide loading overlay
        if hasattr(self, 'patient_loading_overlay') and self.patient_loading_overlay:
            self.patient_loading_overlay.close()
            self.patient_loading_overlay = None

        toast = Toast(self, "Failed to add patient!", icon_path="Icons/warning.png")
        toast.show_toast()

    def show_loading_label(self, layout, message="Loading..."):
        """Show a loading label in the given layout"""
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
    
    def clear_loading_label(self, layout):
        """Clear loading label if present"""
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget and widget.objectName() == "loadingLabel":
                widget.deleteLater()
                break
    def on_phone_number_changed(self, text):
        """Real-time phone number formatting with numbers-only input and length limits"""
        # If text is empty, return
        if not text:
            return

        # Store cursor position
        cursor_pos = self.phoneNumberEdit.cursorPosition()

        # Normalize as user types and enforce max lengths.
        # Important: once it becomes +63..., do NOT allow adding extra digits.
        if text.startswith('+63'):
            digits_after = ''.join(ch for ch in text[3:] if ch.isdigit())
            if len(digits_after) > 10:
                digits_after = digits_after[:10]
            normalized = '+63' + digits_after
            if normalized != text:
                self.phoneNumberEdit.blockSignals(True)
                self.phoneNumberEdit.setText(normalized)
                self.phoneNumberEdit.blockSignals(False)
                self.phoneNumberEdit.setCursorPosition(len(normalized))
            return

        # If user typed 63... without plus, convert to +63... and cap to 10 digits after 63
        if text.startswith('63'):
            rest = ''.join(ch for ch in text[2:] if ch.isdigit())
            if len(rest) > 10:
                rest = rest[:10]
            normalized = '+63' + rest
            if normalized != text:
                self.phoneNumberEdit.blockSignals(True)
                self.phoneNumberEdit.setText(normalized)
                self.phoneNumberEdit.blockSignals(False)
                self.phoneNumberEdit.setCursorPosition(len(normalized))
            return

        # Auto-format from 09XXXXXXXXX → +639XXXXXXXXX (when complete)
        if text.startswith('09'):
            if len(text) == 11:
                normalized = '+63' + text[1:]
                if normalized != text:
                    self.phoneNumberEdit.blockSignals(True)
                    self.phoneNumberEdit.setText(normalized)
                    self.phoneNumberEdit.blockSignals(False)
                    self.phoneNumberEdit.setCursorPosition(len(normalized))
            elif len(text) > 11:
                self.phoneNumberEdit.blockSignals(True)
                self.phoneNumberEdit.setText(text[:11])
                self.phoneNumberEdit.blockSignals(False)
                self.phoneNumberEdit.setCursorPosition(cursor_pos)
            return

        # If user typed 9XXXXXXXXX (10 digits), convert to +63... when complete
        if text.startswith('9'):
            digits_only = ''.join(ch for ch in text if ch.isdigit())
            if len(digits_only) == 10:
                normalized = '+63' + digits_only
                self.phoneNumberEdit.blockSignals(True)
                self.phoneNumberEdit.setText(normalized)
                self.phoneNumberEdit.blockSignals(False)
                self.phoneNumberEdit.setCursorPosition(len(normalized))
            elif len(digits_only) > 10:
                self.phoneNumberEdit.blockSignals(True)
                self.phoneNumberEdit.setText(digits_only[:10])
                self.phoneNumberEdit.blockSignals(False)
                self.phoneNumberEdit.setCursorPosition(min(cursor_pos, 10))
            return
    def on_secondary_phone_changed(self, text):
        """Real-time secondary phone number formatting with numbers-only input and length limits"""
        # If text is empty, return
        if not text:
            return

        # Store cursor position
        cursor_pos = self.secondaryPhoneEdit.cursorPosition()

        if text.startswith('+63'):
            digits_after = ''.join(ch for ch in text[3:] if ch.isdigit())
            if len(digits_after) > 10:
                digits_after = digits_after[:10]
            normalized = '+63' + digits_after
            if normalized != text:
                self.secondaryPhoneEdit.blockSignals(True)
                self.secondaryPhoneEdit.setText(normalized)
                self.secondaryPhoneEdit.blockSignals(False)
                self.secondaryPhoneEdit.setCursorPosition(len(normalized))
            return

        if text.startswith('63'):
            rest = ''.join(ch for ch in text[2:] if ch.isdigit())
            if len(rest) > 10:
                rest = rest[:10]
            normalized = '+63' + rest
            if normalized != text:
                self.secondaryPhoneEdit.blockSignals(True)
                self.secondaryPhoneEdit.setText(normalized)
                self.secondaryPhoneEdit.blockSignals(False)
                self.secondaryPhoneEdit.setCursorPosition(len(normalized))
            return

        if text.startswith('09'):
            if len(text) == 11:
                normalized = '+63' + text[1:]
                if normalized != text:
                    self.secondaryPhoneEdit.blockSignals(True)
                    self.secondaryPhoneEdit.setText(normalized)
                    self.secondaryPhoneEdit.blockSignals(False)
                    self.secondaryPhoneEdit.setCursorPosition(len(normalized))
            elif len(text) > 11:
                self.secondaryPhoneEdit.blockSignals(True)
                self.secondaryPhoneEdit.setText(text[:11])
                self.secondaryPhoneEdit.blockSignals(False)
                self.secondaryPhoneEdit.setCursorPosition(cursor_pos)
            return

        if text.startswith('9'):
            digits_only = ''.join(ch for ch in text if ch.isdigit())
            if len(digits_only) == 10:
                normalized = '+63' + digits_only
                self.secondaryPhoneEdit.blockSignals(True)
                self.secondaryPhoneEdit.setText(normalized)
                self.secondaryPhoneEdit.blockSignals(False)
                self.secondaryPhoneEdit.setCursorPosition(len(normalized))
            elif len(digits_only) > 10:
                self.secondaryPhoneEdit.blockSignals(True)
                self.secondaryPhoneEdit.setText(digits_only[:10])
                self.secondaryPhoneEdit.blockSignals(False)
                self.secondaryPhoneEdit.setCursorPosition(min(cursor_pos, 10))
            return

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
    def load_patients(self, page=1, search_term=None, force_refresh=True):
        """Load patients list asynchronously (non-blocking)
        
        IMPORTANT: Always loads fresh data to show new website registrations!
        
        Args:
            page: Page number to load
            search_term: Optional search query
            force_refresh: Always True by default to ensure fresh data
        """
        try:
            # 1. ALWAYS clear patient cache first to ensure fresh data
            self.api.invalidate_cache('/api/patients')
            self.api.invalidate_cache('/api/patient-search')
            
            # 2. Show loading label immediately
            self.show_loading_label(self.patientListLayout, "Loading patients...")
            
            # 3. Build URL with cache-busting timestamp (always add to prevent any caching)
            from datetime import datetime
            timestamp = int(datetime.now().timestamp() * 1000)
            
            if search_term and search_term.strip():
                import urllib.parse
                encoded_term = urllib.parse.quote(search_term.strip())
                url = f"/api/patient-search/?page={page}&search={encoded_term}&_t={timestamp}"
                print(f"[load_patients] Loading search results: {url}")
            else:
                url = f"/api/patients/?page={page}&_t={timestamp}"
                print(f"[load_patients] Loading all patients (fresh): {url}")
            
            # 4. Make async request (non-blocking!)
            self.api.get(
                url,
                on_success=lambda data: self._on_patients_loaded(data, page, search_term),
                on_error=lambda error: self._on_patients_error(error, search_term),
                timeout=10
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.show_empty_state(False, error=True)
    
    def _on_patients_loaded(self, data, page, search_term):
        """Callback when patients data is received"""
        # Debug logging
        patients = data.get('results', [])
        print(f"[_on_patients_loaded] Page {page}, got {len(patients)} patients, total_count={data.get('count', 0)}")
        if patients:
            print(f"[_on_patients_loaded] First patient: {patients[0].get('firstName', '')} {patients[0].get('lastName', '')}")
        
        # Clear the layout first (removes loading label)
        while self.patientListLayout.count():
            child = self.patientListLayout.takeAt(0)
            if child and child.widget():
                child.widget().deleteLater()
        
        # Update pagination info
        self.patient_currentPage = max(1, page)
        self.current_patient_page = self.patient_currentPage
        self.total_patient_pages = data.get('total_pages', 1)
        self.total_patient_count = data.get('count', 0)
        
        # Handle empty results
        if not patients and page > 1:
            return self.load_patients(page - 1, search_term)
        
        if not patients:
            self.show_empty_state(search_term is not None)
            return
        
        # Create patient cards
        self.create_patient_cards(patients)
        
        # Add pagination controls
        self.add_patient_pagination_controls(search_term)
    
    def _on_patients_error(self, error_msg, search_term):
        """Callback when patient loading fails"""
        print(f"Error loading patients: {error_msg}")
        self.show_empty_state(search_term is not None, error=True)
    
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
                # Pass search term when loading different pages (always force refresh)
                page_btn.clicked.connect(lambda checked, p=page: self.load_patients(p, search_term, force_refresh=True))

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

    # DELETED PATIENTS (HIDDEN RECORDS)
    def load_deleted_patients(self, page=1, search_term=None):
        """Load patients marked as deleted (desktop_record='hide'), with optional search"""
        try:
            # Show loading label
            if hasattr(self, 'deletedPatientListLayout'):
                self.show_loading_label(self.deletedPatientListLayout, "Loading deleted patients...")
            from datetime import datetime
            timestamp = int(datetime.now().timestamp() * 1000)
            if search_term and search_term.strip():
                import urllib.parse
                encoded_term = urllib.parse.quote(search_term.strip())
                url = f"/api/deleted-patients/?page={page}&search={encoded_term}&_t={timestamp}"
            else:
                url = f"/api/deleted-patients/?page={page}&_t={timestamp}"
            self.api.get(
                url,
                on_success=lambda data: self._on_deleted_patients_loaded(data, page, search_term),
                on_error=lambda error: self._on_deleted_patients_error(error),
                timeout=10
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._on_deleted_patients_error(str(e))

    def _on_deleted_patients_loaded(self, data, page, search_term=None):
        """Callback when deleted patients data is received"""
        patients = data.get('results', [])
        print(f"[_on_deleted_patients_loaded] Page {page}, got {len(patients)} deleted patients")
        
        # Clear the layout first
        if hasattr(self, 'deletedPatientListLayout'):
            while self.deletedPatientListLayout.count():
                child = self.deletedPatientListLayout.takeAt(0)
                if child and child.widget():
                    child.widget().deleteLater()
        
        # Update pagination info
        self.deleted_patient_currentPage = max(1, page)
        self.deleted_total_patient_pages = data.get('total_pages', 1)
        self.deleted_total_patient_count = data.get('count', 0)
        
        # Handle empty results
        if not patients:
            self.show_deleted_empty_state()
            return
        
        # Create patient cards with restore button
        self.create_deleted_patient_cards(patients)
        
        # Add pagination controls
        self.add_deleted_patient_pagination_controls(search_term)

    def _on_deleted_patients_error(self, error_msg):
        """Callback when deleted patient loading fails"""
        print(f"Error loading deleted patients: {error_msg}")
        self.show_deleted_empty_state(error=True)

    def show_deleted_empty_state(self, error=False):
        """Show appropriate empty state message for deleted patients"""
        if not hasattr(self, 'deletedPatientListLayout'):
            return
            
        empty_label = QLabel()
        if error:
            empty_label.setText("Error loading deleted patients")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(255, 100, 100);")
        else:
            empty_label.setText("NO DELETED RECORDS")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")
        
        self.deletedPatientListLayout.addStretch()
        self.deletedPatientListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.deletedPatientListLayout.addStretch()

    def create_deleted_patient_cards(self, patients):
        """Create patient cards for deleted patients with restore button"""
        if not hasattr(self, 'deletedPatientListLayout'):
            return
            
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
            
            # Hide delete button
            card.deleteButton.hide()
            
            # Change edit button to a restore button
            restore_btn = card.findChild(QToolButton, "editBtn")
            if restore_btn:
                # Use custom restore icon - replace 'Icons/restore.png' with your icon path
                from PyQt6.QtGui import QIcon
                restore_btn.setIcon(QIcon("Icons/restore.png"))  # Or use :/Icons/Icons/restore.png if in resources
                restore_btn.setToolTip("Restore Patient")
                # Safely disconnect existing signals
                try:
                    restore_btn.clicked.disconnect()
                except TypeError:
                    pass  # No connections to disconnect
                restore_btn.clicked.connect(
                    lambda _, p_id=patient['id'], name=full_name: self.restore_patient(p_id, name)
                )
            
            # Enable card click to open profile (like main patient list)
            card.mousePressEvent = lambda event, p=patient: self.show_patient_profile(p)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            
            card.setGraphicsEffect(create_card_shadow())
            self.deletedPatientListLayout.addWidget(card)

    def add_deleted_patient_pagination_controls(self, search_term=None):
        """Add pagination controls for deleted patients, with search support"""
        if self.deleted_total_patient_pages <= 1:
            return

        try:
            self.deleted_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

            # Connect prev/next buttons
            self.deleted_pagination_widget.PrevPage.clicked.connect(
                lambda: self.load_deleted_patients(self.deleted_patient_currentPage - 1, search_term)
            )
            self.deleted_pagination_widget.NextPage.clicked.connect(
                lambda: self.load_deleted_patients(self.deleted_patient_currentPage + 1, search_term)
            )

            # Set button states
            self.deleted_pagination_widget.PrevPage.setEnabled(self.deleted_patient_currentPage > 1)
            self.deleted_pagination_widget.NextPage.setEnabled(self.deleted_patient_currentPage < self.deleted_total_patient_pages)

            # Create page buttons
            page_layout = self.deleted_pagination_widget.pageButtonsLayout
            while page_layout.count():
                child = page_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            current_page = self.deleted_patient_currentPage
            total_pages = self.deleted_total_patient_pages
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

            # Add page buttons
            for page in range(start_page, end_page + 1):
                page_btn = QPushButton(str(page))
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
                    page_btn.clicked.connect(lambda checked, p=page: self.load_deleted_patients(p, search_term))

                page_layout.addWidget(page_btn)

            self.deleted_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())
            self.deletedPatientListLayout.addWidget(self.deleted_pagination_widget)

        except Exception as e:
            print(f"Error creating deleted patient pagination: {e}")
    def setup_deleted_patients_search(self):
        # Connect deleted patients search bar to handler
        if hasattr(self, 'deleteClientsSearch'):
            self.deleteClientsSearch.textEdited.connect(self.handle_deleted_patients_search_input)
            self._deleted_search_timer = QTimer()
            self._deleted_search_timer.setSingleShot(True)
            self._deleted_search_timer.timeout.connect(self.perform_deleted_patients_search)
            self.deleted_patients_search_term = ""
            self.deleteClientsSearch.clear()

    def handle_deleted_patients_search_input(self, text):
        self.deleted_patients_search_term = text.strip()
        self._deleted_search_timer.start(500)

    def perform_deleted_patients_search(self):
        if self.deleted_patients_search_term:
            self.load_deleted_patients(page=1, search_term=self.deleted_patients_search_term)
        else:
            self.load_deleted_patients(page=1)

    def restore_patient(self, patient_id, patient_name):
        """Restore a deleted patient by updating desktop_record to 'show'"""
        # Store original confirm card config
        original_config = self.confirmCard_original_config.copy()
        
        # Set custom config for restore confirmation
        self.confirmCard.confirmationMessage.setText(f"Restore {patient_name}?\nThis patient will reappear in your Client Records.")
        self.confirmCard.yesButton.setText("RESTORE")
        self.confirmCard.noButton.setText("CANCEL")
        self.confirmCard.yesButton.setStyleSheet(original_config['yes_style'])
        self.confirmCard.noButton.setStyleSheet(original_config['no_style'])
        
        # Disconnect previous signal connections
        try:
            self.confirmCard.yesButton.clicked.disconnect()
            self.confirmCard.noButton.clicked.disconnect()
        except TypeError:
            pass
        
        # Define restore callbacks
        def _on_restore_confirmed():
            self.confirmCard.hide()
            # Restore original config
            self.confirmCard.confirmationMessage.setText(original_config['message'])
            self.confirmCard.yesButton.setText(original_config['yes_text'])
            self.confirmCard.noButton.setText(original_config['no_text'])
            self.confirmCard.yesButton.setStyleSheet(original_config['yes_style'])
            self.confirmCard.noButton.setStyleSheet(original_config['no_style'])
            
            def _on_restore_success(_data):
                Toast(self, "Patient restored successfully!", icon_path="Icons/check.png").show_toast()
                # Reload deleted patients list
                self.load_deleted_patients(1)
                # Invalidate patient cache to refresh main list
                self.api.invalidate_cache('/api/patients')
                self.api.invalidate_cache('/api/patient-search')
            
            def _on_restore_error(err):
                Toast(self, "Failed to restore patient.", icon_path="Icons/warning.png").show_toast()
                print(f"Restore patient failed: {err}")
            
            self.api.patch(
                url=f"/api/patients/{patient_id}/",
                data={"desktop_record": "show"},
                on_success=_on_restore_success,
                on_error=_on_restore_error,
                timeout=15,
                show_loading=True,
                loading_title="Restoring patient...",
                loading_subtitle="Please wait"
            )
        
        def _on_restore_cancelled():
            self.confirmCard.hide()
            # Restore original config
            self.confirmCard.confirmationMessage.setText(original_config['message'])
            self.confirmCard.yesButton.setText(original_config['yes_text'])
            self.confirmCard.noButton.setText(original_config['no_text'])
            self.confirmCard.yesButton.setStyleSheet(original_config['yes_style'])
            self.confirmCard.noButton.setStyleSheet(original_config['no_style'])
        
        # Connect new handlers
        self.confirmCard.yesButton.clicked.connect(_on_restore_confirmed)
        self.confirmCard.noButton.clicked.connect(_on_restore_cancelled)
        
        # Show the confirmation card centered
        self.confirmCard.show_card()

    def on_deleted_clients_tab_clicked(self):
        """Handler for when deleted clients tab is clicked"""
        self.settingsStactWidget.setCurrentIndex(2)
        # Setup search bar for deleted patients (only once)
        if not hasattr(self, '_deleted_search_timer'):
            self.setup_deleted_patients_search()
        # Load deleted patients with current search term
        QTimer.singleShot(0, lambda: self.load_deleted_patients(1, getattr(self, 'deleted_patients_search_term', None)))

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
        from input_styles import original_yes_style, original_no_style
        self.confirmCard_original_config = {
            'message': "Are you sure you want to delete this record?",
            'yes_text': "YES",
            'no_text': "NO",
            'yes_style': original_yes_style,
            'no_style': original_no_style
        }

        # delete buttons sa profile patient/pet
        self.profileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_patient)
        self.petProfileDeleteBtn.clicked.connect(self.deleteFunction.delete_selected_pet)

    #PATIENT PROFILE PAGE
    def show_patient_profile(self, patient):
        """Show patient profile with loading modal for pets"""
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
        
        # Navigate to the profile page FIRST (shows skeleton loaders)
        self.navigate_to_page(5, owner_id=patient['id'])
        
        # THEN load pets with async call + loading modal
        self.load_pets_for_owner(self.selected_patient_id)

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

        # Store for callback
        self._pet_required_fields = required_fields
        self._pet_owner_id = self.selected_patient_id

        # Non-blocking POST with loading overlay
        self.api.post(
            url="/api/pets/",
            data=data,
            on_success=self._on_pet_added,
            on_error=self._on_pet_add_error,
            timeout=20,
            show_loading=True,
            loading_title="Adding Pet...",
            loading_subtitle="Please wait while we save the pet information"
        )

    def _on_pet_added(self, response):
        owner_id = getattr(self, '_pet_owner_id', None)

        # Invalidate + refresh cache for this owner's pets
        if owner_id:
            self.api.invalidate_cache(f"/api/pets/?owner_id={owner_id}")
            self._pets_sig_by_owner.pop(owner_id, None)

        self.profileStackedWidget.setCurrentIndex(0)
        # Force refresh, but avoid modal flash since this is an immediate UI update
        if owner_id:
            self.load_pets_for_owner(owner_id, force_refresh=True, show_loading_on_miss=False)

        self.clearInputs()

        # reset styles for required widgets
        required_fields = getattr(self, '_pet_required_fields', {})
        for widget in required_fields.values():
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet(default_style)
            elif isinstance(widget, QComboBox):
                widget.setStyleSheet(default_combobox_style)

        toast = Toast(self, icon_path="Icons/check.png")
        toast.show_toast()

        self._pet_required_fields = None
        self._pet_owner_id = None

    def _on_pet_add_error(self, error_msg):
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
    def load_pets_for_owner(self, owner_id, force_refresh: bool = False, show_loading_on_miss: bool = True):
        """Cache-first pet list load.

        Behavior:
            - If cached: render immediately (no modal), then refresh in background.
            - If not cached: fetch with loading modal, then cache result.
        """
        url = f'/api/pets/?owner_id={owner_id}'
        cache_ttl = 120

        cached = None if force_refresh else self.api.get_cached(url, cache_ttl=cache_ttl)
        if cached is not None and not force_refresh:
            self._on_pets_loaded(cached, owner_id=owner_id)
            # Refresh quietly in background; update UI only if changed
            self.api.get(
                url,
                on_success=lambda fresh: self._refresh_pets_if_changed(owner_id, fresh),
                on_error=lambda _e: None,
                show_loading=False,
                use_cache=False,
                timeout=10
            )
            return

        # No cache yet (or forced refresh): fetch, then cache
        self.api.get(
            url,
            on_success=lambda data: self._on_pets_loaded(data, owner_id=owner_id),
            on_error=self._on_pets_load_error,
            show_loading=bool(show_loading_on_miss and not force_refresh),
            loading_title="Loading pets...",
            loading_subtitle="Please wait while we fetch your pets",
            use_cache=True,
            cache_ttl=cache_ttl,
            timeout=10
        )

    def _on_pets_loaded(self, response, owner_id: int | None = None):
        """Callback when pets data is received"""
        # Handle API response format
        if isinstance(response, dict):
            pets = response.get('results', response.get('data', []))
        else:
            pets = response if isinstance(response, list) else []

        if owner_id is not None:
            self._pets_sig_by_owner[owner_id] = self._data_signature(pets)

        # clear pet cards lang, wag galawin addPetButton
        while self.gridLayout_6.count() > 1:
            item = self.gridLayout_6.takeAt(1)  # skip first item (addPetButton)
            if item and item.widget():
                item.widget().deleteLater()

        if not pets:
            return

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

    def _on_pets_load_error(self, error_msg):
        """Handle error loading pets"""
        print(f"Error loading pets: {error_msg}")
        Toast(self, f"Error loading pets: {error_msg}", icon_path="Icons/warning.png").show_toast()

    def _refresh_pets_if_changed(self, owner_id: int, response):
        """Background refresh: update pet cards only if server data changed."""
        if isinstance(response, dict):
            pets = response.get('results', response.get('data', []))
        else:
            pets = response if isinstance(response, list) else []

        new_sig = self._data_signature(pets)
        if self._pets_sig_by_owner.get(owner_id) == new_sig:
            return

        self._on_pets_loaded(pets, owner_id=owner_id)

    #PET PROFILE PAGE
    def show_pet_profile(self, pet):
        """Show pet profile with loading modal for services"""
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
        
        # Navigate to pet profile page FIRST (shows skeleton loaders)
        self.navigate_to_page(6, pet_id=pet["id"])
        
        # THEN load services with async call + loading modal
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
    def load_services_for_pet(self, pet_id, force_refresh: bool = False, show_loading_on_miss: bool = True):
        """Cache-first service history load.

        Behavior:
            - If cached: render immediately (no modal), then refresh in background.
            - If not cached: fetch with loading modal, then cache result.
        """
        url = f'/api/services/?pet_id={pet_id}'
        cache_ttl = 120

        cached = None if force_refresh else self.api.get_cached(url, cache_ttl=cache_ttl)
        if cached is not None and not force_refresh:
            self._on_services_loaded(cached, pet_id=pet_id)
            self.api.get(
                url,
                on_success=lambda fresh: self._refresh_services_if_changed(pet_id, fresh),
                on_error=lambda _e: None,
                show_loading=False,
                use_cache=False,
                timeout=10
            )
            return

        self.api.get(
            url,
            on_success=lambda data: self._on_services_loaded(data, pet_id=pet_id),
            on_error=self._on_services_load_error,
            show_loading=bool(show_loading_on_miss and not force_refresh),
            loading_title="Loading services...",
            loading_subtitle="Please wait while we fetch the service history",
            use_cache=True,
            cache_ttl=cache_ttl,
            timeout=10
        )
    
    def _on_services_loaded(self, services, pet_id: int | None = None):
        """Callback when services data is received"""
        if isinstance(services, dict):  # API returns dict with results
            services = services.get('results', services)
        if not isinstance(services, list):
            services = []

        if pet_id is not None:
            self._services_sig_by_pet[pet_id] = self._data_signature(services)

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
            prescription = str(service.get("prescription"))
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

            prescription_label = service_card.findChild(QTextEdit, "prescriptionLabel")
            prescription_label.setPlainText(f"{prescription}" if prescription else "No Notes")

            upper_frame = service_card.findChild(QWidget, "upperFrame")
            lower_frame = service_card.findChild(QWidget, "lowerFrame")
            lower_frame.setVisible(False)

            # Find buttons safely
            open_btn = service_card.findChild(QToolButton, "OpenNoteBtn")
            close_btn = service_card.findChild(QToolButton, "closeNotesBtn")

            service_card.serviceDeleteBtn.clicked.connect(lambda _, service_id=service['id']: self.deleteFunction.set_delete_target("service", service_id))
            service_card.updateServiceCardBtn.clicked.connect(lambda _, service_id=service["id"]: self.updateFunction.update_service_info(service_id))
            service_card.wholeFrameCard.setGraphicsEffect(create_card_shadow())

            service_card.printPrescription.clicked.connect(lambda _, service_id=service['id']: self.print_prescription(service_id))
            # Connect buttons safely
            if open_btn and close_btn and lower_frame:
                open_btn.setVisible(True)
                close_btn.setVisible(False)

                open_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, True,upper_frame))
                close_btn.clicked.connect(partial(self.toggle_note, lower_frame, open_btn, close_btn, False,upper_frame))

            self.serviceListLayout.insertWidget(0, service_card)

    def _on_services_load_error(self, error_msg):
        """Handle error loading services"""
        print(f"Error loading services: {error_msg}")
        # Show empty state instead of breaking
        header = self.findChild(QWidget, "serviceTableHeader")
        header.setVisible(False)
        empty_label = QLabel("EMPTY")
        empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
        self.serviceListLayout.addStretch()
        self.serviceListLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.serviceListLayout.addStretch()
        Toast(self, f"Could not load services", icon_path="Icons/warning.png").show_toast()

    def _refresh_services_if_changed(self, pet_id: int, response):
        """Background refresh: update service cards only if server data changed."""
        services = response
        if isinstance(services, dict):
            services = services.get('results', services)
        if not isinstance(services, list):
            services = []

        new_sig = self._data_signature(services)
        if self._services_sig_by_pet.get(pet_id) == new_sig:
            return

        self._on_services_loaded(services, pet_id=pet_id)

    def _data_signature(self, data_obj) -> str:
        """Stable signature for change detection (order-independent for dict keys)."""
        try:
            return json.dumps(data_obj, sort_keys=True, default=str, ensure_ascii=False)
        except Exception:
            return str(data_obj)

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
    def print_prescription(self, service_id):
        if self.selected_patient_id and self.selected_pet_id:
            print_url = f"{API_BASE_URL}/api/print-prescription/{self.selected_patient_id}/{self.selected_pet_id}/{service_id}/"
            webbrowser.open(print_url)
        else:
            QMessageBox.warning(self, "Missing Info", "Please select a patient and a pet first.")
    #PET PROFILE RELOAD
    def refresh_current_pet_profile(self):
        """Refresh the current pet profile without affecting navigation history (cache-first)."""
        pet_id = getattr(self, 'selected_pet_id', None)
        if not pet_id:
            return

        self._load_pet_detail_cache_first(pet_id, on_ready=self.update_pet_profile_ui, show_loading_on_miss=False)

    def _load_pet_detail_cache_first(self, pet_id: int, on_ready, show_loading_on_miss: bool = True):
        """Load a pet detail dict cache-first, then refresh in background if changed."""
        url = f"/api/pets/{pet_id}/"
        cache_ttl = 120

        cached = self.api.get_cached(url, cache_ttl=cache_ttl)
        if cached is not None:
            try:
                self._pet_sig_by_id[pet_id] = self._data_signature(cached)
                on_ready(cached)
            except Exception as e:
                print(f"Error using cached pet detail: {e}")

            # Quiet refresh; only apply if changed
            self.api.get(
                url,
                on_success=lambda fresh: self._refresh_pet_detail_if_changed(pet_id, fresh, on_ready),
                on_error=lambda _e: None,
                show_loading=False,
                use_cache=False,
                timeout=10
            )
            return

        # No cache yet
        self.api.get(
            url,
            on_success=lambda fresh: self._apply_pet_detail(pet_id, fresh, on_ready),
            on_error=lambda e: print(f"Failed to load pet {pet_id}: {e}"),
            show_loading=bool(show_loading_on_miss),
            loading_title="Loading pet profile...",
            loading_subtitle="Please wait",
            use_cache=True,
            cache_ttl=cache_ttl,
            timeout=10
        )

    def _apply_pet_detail(self, pet_id: int, pet, on_ready):
        try:
            self._pet_sig_by_id[pet_id] = self._data_signature(pet)
            on_ready(pet)
        except Exception as e:
            print(f"Error applying pet detail: {e}")

    def _refresh_pet_detail_if_changed(self, pet_id: int, pet, on_ready):
        new_sig = self._data_signature(pet)
        if self._pet_sig_by_id.get(pet_id) == new_sig:
            return
        self._apply_pet_detail(pet_id, pet, on_ready)
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
    def load_service_types_to_main_combobox(self):
        """Load service types into the main UI's serviceTypeComboBox asynchronously"""
        try:
            # Initialize combobox with placeholder
            service_combo = self.findChild(QComboBox, "serviceTypeComboBox")
            if service_combo:
                service_combo.clear()
                service_combo.addItem("Select Service", None)  # Add placeholder

            # Fetch service types asynchronously
            self.api.get(
                "/api/service-types/?is_active=true&no_pagination=true",
                on_success=self._on_service_types_loaded,
                on_error=self._on_service_types_error
            )

        except Exception as e:
            print(f"Error loading service types for main UI combobox: {e}")
            service_combo = self.findChild(QComboBox, "serviceTypeComboBox")
            if service_combo:
                service_combo.clear()
                service_combo.addItem("Select Service", None)

    def _on_service_types_loaded(self, data):
        """Callback when service types data is received"""
        try:
            # Parse response
            if isinstance(data, list):
                service_types = data  # Direct list from no_pagination
            elif isinstance(data, dict) and 'results' in data:
                service_types = data['results']  # Paginated response
            else:
                service_types = []

            # Get the combobox from your main UI
            service_combo = self.findChild(QComboBox, "serviceTypeComboBox")

            if service_combo:
                service_combo.clear()
                service_combo.addItem("Select Service", None)  # Add placeholder

                # Add service types to combobox
                for service_type in service_types:
                    if service_type.get('is_active', True):
                        name = service_type.get('name', '')
                        if name:  # Only add if name exists
                            service_combo.addItem(name, service_type.get('id'))

                # If no service types were added (only placeholder)
                if service_combo.count() == 1:
                    service_combo.addItem("No service types available", None)

                print(f"Loaded {service_combo.count() - 1} service types to main combobox")

        except Exception as e:
            print(f"Error processing service types: {e}")

    def _on_service_types_error(self, error_msg):
        """Callback when service types loading fails"""
        print(f"Failed to load service types: {error_msg}")
        service_combo = self.findChild(QComboBox, "serviceTypeComboBox")
        if service_combo:
            service_combo.clear()
            service_combo.addItem("Select Service", None)
            service_combo.addItem("Error loading services", None)

    def submit_service_data(self):
        service_type_id = self.serviceTypeComboBox.currentData()

        if not service_type_id:
            toast = Toast(self, "Please select a valid service type", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        date = self.dateEdit.date().toString("yyyy-MM-dd")

        if self.returnCheckBox.isChecked():
            return_date = self.returnDateEdit.date().toString("yyyy-MM-dd")
        else:
            return_date = None

        notes = self.addNoteLineEdit.toPlainText().strip()
        prescription = self.prescriptionTextedit.toPlainText().strip()

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
            "service_type_id": service_type_id,  # CHANGED: Send ID
            "date": date,
            "return_date": return_date,
            "notes": notes,
            "prescription": prescription
        }

        # Store for callback
        self._service_required_fields = required_fields
        self._service_pet_id = self.selected_pet_id

        # Non-blocking POST with loading overlay
        self.api.post(
            url="/api/services/",
            data=service_data,
            on_success=self._on_service_added,
            on_error=self._on_service_add_error,
            timeout=25,
            show_loading=True,
            loading_title="Adding Service...",
            loading_subtitle="Please wait while we save the service"
        )

    def _on_service_added(self, response):
        toast = Toast(self, "Service added!", icon_path="Icons/check.png")
        toast.show_toast()

        pet_id = getattr(self, '_service_pet_id', None)

        # Invalidate + refresh cache for this pet's services
        if pet_id:
            self.api.invalidate_cache(f"/api/services/?pet_id={pet_id}")
            self._services_sig_by_pet.pop(pet_id, None)

        if hasattr(self, 'selected_pet_id') and self.selected_pet_id:
            self.refresh_current_pet_profile()
            self.load_services_for_pet(self.selected_pet_id, force_refresh=True, show_loading_on_miss=False)

        self.serviceHistoryBtn.setChecked(True)
        self.serviceHistoryStackedWidget.setCurrentIndex(0)
        if self.selected_pet_id:
            self.load_services_for_pet(self.selected_pet_id, force_refresh=True, show_loading_on_miss=False)
        self.load_scheduled_services()
        self.clearInputs()

        self._service_required_fields = None
        self._service_pet_id = None

    def _on_service_add_error(self, error_msg):
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
        self.appointmentCard.load_service_types_to_combobox()
        self.appointmentCard.show_card()

    #SCHEDULED RETURN VIST PAGE
    def setup_scheduled_search(self):
        """Setup search functionality for scheduled services"""
        # Connect search bar to search handler
        self.scheduledSearchBar.textEdited.connect(self.handle_scheduled_search_input)

        # Setup search timer for debouncing
        self._scheduled_search_timer = QTimer()
        self._scheduled_search_timer.setSingleShot(True)
        self._scheduled_search_timer.timeout.connect(self.perform_scheduled_search)

        # Clear search bar initially
        self.scheduledSearchBar.clear()
    def handle_scheduled_search_input(self, text):
        """Handle scheduled services search input with debouncing"""
        self.scheduled_search_term = text.strip()
        self._scheduled_search_timer.start(500)
    def perform_scheduled_search(self):
        """Perform the actual search for scheduled services"""
        print(f"DEBUG: Performing search for: '{self.scheduled_search_term}'")
        if self.scheduled_search_term:
            self.load_scheduled_services(page=1, search_term=self.scheduled_search_term)
        else:
            # If search is empty, load normal scheduled services list
            self.load_scheduled_services(page=1)
    def set_current_month_in_combobox(self):
        self.monthComboBox.setGraphicsEffect(create_card_shadow())
        current_month = datetime.now().strftime("%B")
        index = self.monthComboBox.findText(current_month)
        if index >= 0:
            self.monthComboBox.setCurrentIndex(index)
    def load_scheduled_services(self, page=1, search_term=None):
        """Load scheduled services with pagination and search support"""
        try:
            # Debug print to see what's happening
            print(f"DEBUG: load_scheduled_services called with page={page}, search_term='{search_term}'")
            if hasattr(self, 'appointmentCard') and hasattr(self.appointmentCard, 'scheduled_card_manager'):
                print(f"DEBUG: Clearing scheduled card manager")
                # Clear cards list but keep persistent IDs for restoration
                self.appointmentCard.scheduled_card_manager.scheduled_cards.clear()
                # Clear selected IDs (they'll be restored if persistent)
                self.appointmentCard.scheduled_card_manager.selected_service_ids.clear()
                # Hide reminder buttons
                if hasattr(self, 'schedReminderBtnFrame'):
                    self.schedReminderBtnFrame.setVisible(False)
            # Determine current status filter based on which status button is checked
            if self.pendingReturnBtn.isChecked():
                self.scheduled_current_filter = "pending"
                target_layout = self.pendingLayout
                print(f"DEBUG: Status filter = pending")
            elif self.completeReurnBtn.isChecked():
                self.scheduled_current_filter = "completed"
                target_layout = self.completedLayout
                print(f"DEBUG: Status filter = completed")
            elif self.overdueReturnBtn.isChecked():
                self.scheduled_current_filter = "overdue"
                target_layout = self.overdueLayout
                print(f"DEBUG: Status filter = overdue")
            else:
                self.scheduled_current_filter = "pending"
                target_layout = self.pendingLayout
                print(f"DEBUG: Status filter = pending (default)")

            # Update state
            self.scheduled_current_page = page
            self.scheduled_search_term = search_term or ""

            # Clear ALL layouts and pagination widget
            print(f"DEBUG: Clearing layouts")
            for layout in [self.pendingLayout, self.completedLayout, self.overdueLayout]:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # Clear pagination widget
            if hasattr(self, 'scheduled_pagination_widget'):
                try:
                    if self.scheduled_pagination_widget and self.scheduled_pagination_widget.isWidgetType():
                        self.scheduled_pagination_widget.deleteLater()
                except:
                    pass
                finally:
                    if hasattr(self, 'scheduled_pagination_widget'):
                        delattr(self, 'scheduled_pagination_widget')

            # Show loading label after clearing everything so it stays visible
            self.show_loading_label(target_layout, "Loading scheduled services...")

            # Get selected month from combobox
            selected_month = self.monthComboBox.currentText()  # e.g., 'August'
            print(f"DEBUG: Selected month = {selected_month}")

            # Build API URL with pagination and filters
            # First try the new endpoint with all parameters
            url = "/api/scheduled-services/"
            params = {
                'page': page,
                'month': selected_month,
                'status': self.scheduled_current_filter  # Always include status
            }

            # Add search term if provided
            if search_term and search_term.strip():
                params['search'] = search_term.strip()

            print(f"DEBUG: API params = {params}")

            # Make async API request (non-blocking!)
            self.api.get(
                url,
                on_success=lambda data: self._on_scheduled_loaded(data, target_layout, page, search_term),
                on_error=lambda e: self._on_scheduled_error(e, target_layout),
                params=params,
                timeout=10
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.show_scheduled_empty_state(target_layout, error=True)
    
    def _on_scheduled_loaded(self, data, target_layout, page, search_term):
        """Callback when scheduled services data is received"""
        try:
            print(f"DEBUG: API response data type = {type(data)}")
            
            # Remove loading label/stretches before rendering data
            while target_layout.count():
                child = target_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Check if the API supports pagination
            if isinstance(data, dict) and 'results' in data:
                # Paginated response
                scheduled_services = data.get('results', [])
                self.scheduled_total_pages = data.get('total_pages', 1)
                self.scheduled_total_count = data.get('count', 0)
                print(f"DEBUG: Got paginated response: {len(scheduled_services)} services, {self.scheduled_total_pages} pages")
            else:
                # Non-paginated response or direct list
                scheduled_services = data or []
                self.scheduled_total_pages = 1
                self.scheduled_total_count = len(scheduled_services)
                print(f"DEBUG: Got direct list response: {len(scheduled_services)} services")

                # If we got a list but expected status filter, we need to filter manually
                if self.scheduled_current_filter and scheduled_services:
                    # Check if items have status field
                    if 'status' in scheduled_services[0]:
                        scheduled_services = [s for s in scheduled_services if
                                              s.get('status', '').lower() == self.scheduled_current_filter]
                        print(f"DEBUG: After manual status filtering: {len(scheduled_services)} services")

            print(f"DEBUG: Final service count = {len(scheduled_services)}")

            # If no results and we're not on page 1, go back to page 1
            if not scheduled_services and page > 1:
                print(f"DEBUG: No results, going back to page 1")
                self.load_scheduled_services(page=1, search_term=search_term)
                return

            # Show empty state if no results
            if not scheduled_services:
                print(f"DEBUG: Showing empty state")
                self.show_scheduled_empty_state(target_layout, is_search=bool(search_term))
                return

            # Create and add cards
            print(f"DEBUG: Creating {len(scheduled_services)} cards")
            for service in scheduled_services:
                card = self.create_scheduled_card(service)
                target_layout.addWidget(card)

            # Add pagination controls if needed
            if self.scheduled_total_pages > 1:
                print(f"DEBUG: Adding pagination controls")
                self.add_scheduled_pagination_controls(target_layout, search_term)
            else:
                print(f"DEBUG: No pagination needed (only 1 page)")

        except Exception as e:
            print(f"DEBUG: Error in _on_scheduled_loaded: {e}")
            import traceback
            traceback.print_exc()
            self.show_scheduled_empty_state(target_layout, error=True)
    
    def _on_scheduled_error(self, error_msg, target_layout):
        """Callback when scheduled services loading fails"""
        print(f"DEBUG: Error loading scheduled services: {error_msg}")
        # Clear loading label
        while target_layout.count():
            child = target_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.show_scheduled_empty_state(target_layout, error=True)
    
    def show_scheduled_empty_state(self, layout, is_search=False, error=False):
        """Show appropriate empty state message for scheduled services"""
        # Clear existing items (including loading label)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        empty_label = QLabel()

        if error:
            empty_label.setText("Error loading scheduled services")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(255, 100, 100);")
        elif is_search:
            empty_label.setText("No scheduled services found")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")
        else:
            empty_label.setText("NO SCHEDULED SERVICES")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")

        layout.addStretch()
        layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
    def create_scheduled_card(self, service):
        """Create a scheduled service card - simplified version"""
        try:
            # Delegate card creation to the scheduled_card_manager
            card = self.appointmentCard.scheduled_card_manager.create_scheduled_card(service)

            # The pet click event is already set up in the manager's method
            # No additional setup needed here

            return card
        except Exception as e:
            print(f"DEBUG: Error creating scheduled card: {e}")
            import traceback
            traceback.print_exc()
            # Return a placeholder card if creation fails
            card = QLabel(f"Error creating card: {e}")
            return card
    def add_scheduled_pagination_controls(self, layout, search_term=None):
        """Add pagination controls for scheduled services"""
        # Safely remove existing pagination widget
        if hasattr(self, 'scheduled_pagination_widget'):
            try:
                if self.scheduled_pagination_widget and self.scheduled_pagination_widget.isWidgetType():
                    self.scheduled_pagination_widget.deleteLater()
            except RuntimeError:
                pass

        if self.scheduled_total_pages <= 1:
            return

        try:
            self.scheduled_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

            # Connect prev/next buttons
            self.scheduled_pagination_widget.PrevPage.clicked.connect(
                lambda: self.load_scheduled_services(self.scheduled_current_page - 1, search_term)
            )
            self.scheduled_pagination_widget.NextPage.clicked.connect(
                lambda: self.load_scheduled_services(self.scheduled_current_page + 1, search_term)
            )

            # Set button states
            self.scheduled_pagination_widget.PrevPage.setEnabled(self.scheduled_current_page > 1)
            self.scheduled_pagination_widget.NextPage.setEnabled(
                self.scheduled_current_page < self.scheduled_total_pages
            )

            # Create page buttons
            self.create_scheduled_page_buttons(search_term)

            self.scheduled_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())
            layout.addWidget(self.scheduled_pagination_widget)

        except Exception as e:
            print(f"Error creating scheduled pagination: {e}")
    def create_scheduled_page_buttons(self, search_term=None):
        """Create page buttons for scheduled services pagination"""
        page_layout = self.scheduled_pagination_widget.pageButtonsLayout

        # Clear existing buttons
        while page_layout.count():
            child = page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_page = self.scheduled_current_page
        total_pages = self.scheduled_total_pages
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
                page_btn.clicked.connect(lambda checked, p=page:
                                         self.load_scheduled_services(p, search_term))

            page_layout.addWidget(page_btn)
    def open_pet_from_service(self, pet_id):
        def open_profile_with_pet(pet):
            try:
                self.selected_pet_id = pet.get("id")
                owner = pet.get("owner") or {}
                if isinstance(owner, dict):
                    self.selected_patient_id = owner.get("id")
                self.show_pet_profile(pet)
            except Exception as e:
                print(f"Failed to open pet profile from service: {e}")

        self._load_pet_detail_cache_first(int(pet_id), on_ready=open_profile_with_pet, show_loading_on_miss=True)

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
        # Snapshot current values so Cancel can revert instantly (no API call / no lag)
        self._capture_profile_snapshot()

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

    def _capture_profile_snapshot(self):
        """Capture current profile UI values so we can restore them on Cancel without fetching."""
        try:
            self._profile_snapshot = {
                "full_name": self.profileFullName.text(),
                "username": self.profileUserName.text(),
                "email": self.profileEmail.text(),
                "phone": self.profilePhone.text(),
                "role_text": self.accountRole.text() if hasattr(self, "accountRole") else "",
                "member_since": self.MemberSince.text() if hasattr(self, "MemberSince") else "",
            }
        except Exception:
            self._profile_snapshot = None

    def _restore_profile_snapshot(self) -> bool:
        """Restore previously captured profile UI values. Returns True if restored."""
        snap = getattr(self, "_profile_snapshot", None)
        if not isinstance(snap, dict):
            return False

        try:
            self.profileFullName.setText(snap.get("full_name", ""))
            self.profileUserName.setText(snap.get("username", ""))
            self.profileEmail.setText(snap.get("email", ""))
            self.profilePhone.setText(snap.get("phone", ""))
            if hasattr(self, "accountRole"):
                self.accountRole.setText(snap.get("role_text", ""))
            if hasattr(self, "MemberSince"):
                self.MemberSince.setText(snap.get("member_since", ""))

            self.apply_profile_view_style()
            return True
        except Exception:
            return False
    def setup_profile_validation(self):
        """Setup validation for profile form fields"""
        phone_validator = QRegularExpressionValidator(
            QRegularExpression(r'^(?:0\d{0,10}|9\d{0,9}|63\d{0,10}|\+63\d{0,10})$')
        )
        self.profilePhone.setMaxLength(13)
        self.profilePhone.setValidator(phone_validator)

        # Connect phone formatting
        self.profilePhone.textChanged.connect(self.on_profile_phone_changed)

        # Email validation will be handled in the save method
    def on_profile_phone_changed(self, text):
        """Real-time phone number formatting for profile phone"""
        if not text:
            return

        cursor_pos = self.profilePhone.cursorPosition()

        if text.startswith('+63'):
            digits_after = ''.join(ch for ch in text[3:] if ch.isdigit())
            if len(digits_after) > 10:
                digits_after = digits_after[:10]
            normalized = '+63' + digits_after
            if normalized != text:
                self.profilePhone.blockSignals(True)
                self.profilePhone.setText(normalized)
                self.profilePhone.blockSignals(False)
                self.profilePhone.setCursorPosition(len(normalized))
            return

        if text.startswith('63'):
            rest = ''.join(ch for ch in text[2:] if ch.isdigit())
            if len(rest) > 10:
                rest = rest[:10]
            normalized = '+63' + rest
            if normalized != text:
                self.profilePhone.blockSignals(True)
                self.profilePhone.setText(normalized)
                self.profilePhone.blockSignals(False)
                self.profilePhone.setCursorPosition(len(normalized))
            return

        if text.startswith('09'):
            if len(text) == 11:
                normalized = '+63' + text[1:]
                if normalized != text:
                    self.profilePhone.blockSignals(True)
                    self.profilePhone.setText(normalized)
                    self.profilePhone.blockSignals(False)
                    self.profilePhone.setCursorPosition(len(normalized))
            elif len(text) > 11:
                self.profilePhone.blockSignals(True)
                self.profilePhone.setText(text[:11])
                self.profilePhone.blockSignals(False)
                self.profilePhone.setCursorPosition(cursor_pos)
            return

        if text.startswith('9'):
            digits_only = ''.join(ch for ch in text if ch.isdigit())
            if len(digits_only) == 10:
                normalized = '+63' + digits_only
                self.profilePhone.blockSignals(True)
                self.profilePhone.setText(normalized)
                self.profilePhone.blockSignals(False)
                self.profilePhone.setCursorPosition(len(normalized))
            elif len(digits_only) > 10:
                self.profilePhone.blockSignals(True)
                self.profilePhone.setText(digits_only[:10])
                self.profilePhone.blockSignals(False)
                self.profilePhone.setCursorPosition(min(cursor_pos, 10))
            return
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
            self.passForConfirm.setStyleSheet(error_style_passForConfirm)
            return
        else:
            self.passForConfirm.setStyleSheet(default_style_passForConfirm)
            self.passForConfirm.clear()

        # Prepare data for API
        profile_data = {
            "full_name": self.profileFullName.text().strip(),
            "email": self.profileEmail.text().strip(),
            "phone": self.profilePhone.text().strip()
        }

        # Async verify password then async PATCH update profile
        self._set_settings_busy(True, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)

        def _invalid_password():
            self._set_settings_busy(False, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)
            toast = Toast(self, "Incorrect password! Please try again.", icon_path="Icons/warning.png")
            toast.show_toast()
            self.passForConfirm.setStyleSheet(error_style_passForConfirm)
            self.passForConfirm.clear()
            self.passForConfirm.setFocus()

        def _verify_error(err: str):
            self._set_settings_busy(False, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)
            toast = Toast(self, f"Failed to verify password ({err})", icon_path="Icons/warning.png")
            toast.show_toast()

        def _do_update_profile():
            user_id = (self.current_user or {}).get('id')
            if not user_id:
                self._set_settings_busy(False, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)
                toast = Toast(self, "No user session found", icon_path="Icons/warning.png")
                toast.show_toast()
                return

            self.api.patch(
                url=f"/api/desktop-users/{user_id}/",
                data=profile_data,
                on_success=lambda updated_user: self._on_profile_updated(updated_user),
                on_error=lambda e: self._on_profile_update_failed(e),
                timeout=15,
                show_loading=True,
                loading_title="Updating profile...",
                loading_subtitle="Saving changes"
            )

        self._verify_password_async(
            password,
            on_valid=_do_update_profile,
            on_invalid=_invalid_password,
            on_error=_verify_error
        )

    def _on_profile_updated(self, updated_user):
        try:
            if isinstance(updated_user, dict) and self.current_user is not None:
                self.current_user.update(updated_user)
        except Exception:
            pass
        toast = Toast(self, "Profile updated successfully!", icon_path="Icons/check.png")
        toast.show_toast()
        self._set_settings_busy(False, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)
        self.profileEdit_cancel()  # Return to view mode

    def _on_profile_update_failed(self, err: str):
        self._set_settings_busy(False, self.settingsProfileSaveBtn, self.settingsProfileCancelBtn)
        toast = Toast(self, "Failed to update profile!", icon_path="Icons/warning.png")
        toast.show_toast()
        print(f"Profile update failed: {err}")
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
        if not self._restore_profile_snapshot():
            # Fallback (older sessions / no snapshot)
            self.load_user_profile(self.current_user)

        self.passForConfirm.clear()
        # Disconnect signals to prevent multiple connections
        try:
            self.settingsProfileSaveBtn.clicked.disconnect()
            self.settingsProfileCancelBtn.clicked.disconnect()
        except:
            pass
    def load_user_profile(self, current_user):
        self.passwordFrame.hide()
        self.spacer.show()
        user_id = (current_user or {}).get('id')
        if not user_id:
            return

        try:
            response = requests.get(f"{API_BASE_URL}/api/desktop-users/{user_id}")
            userData = response.json() if response.ok else {}
        except Exception:
            userData = {}

        full_name = userData.get("full_name") or userData.get("fullName")
        if not full_name:
            first = userData.get("firstName") or userData.get("first_name") or ""
            middle = userData.get("middleName") or userData.get("middle_name") or ""
            last = userData.get("lastName") or userData.get("last_name") or ""
            full_name = " ".join([p for p in [first, middle, last] if p]).strip()

        self.profileFullName.setText(full_name or "")
        self.profileUserName.setText(userData.get("username", ""))
        self.profileEmail.setText(userData.get("email", ""))
        self.profilePhone.setText(userData.get("phone", ""))
        role = userData.get('role', '')
        self.accountRole.setText(f"Role: {role}" if role else "")
        created_at = userData.get("created_at")
        if created_at:
            date = self.format_date(created_at)
            self.MemberSince.setText(f"Member Since: {date}")
        else:
            self.MemberSince.setText("")

        # Apply view style when loading
        self.apply_profile_view_style()

        # Keep snapshot in sync with the latest loaded server values
        self._capture_profile_snapshot()
    def apply_profile_view_style(self):
        """Apply the view style to profile fields"""
        for field in [self.profileFullName, self.profileEmail,self.profilePhone]:
            field.setStyleSheet(profile_view_style)
    def apply_profile_edit_style(self):
        """Apply the edit style to profile fields"""
        for field in [self.profileFullName, self.profileEmail, self.profilePhone]:
            field.setStyleSheet(profile_edit_style)
        self.passForConfirm.setStyleSheet(profile_edit_style_passForConfirm)
    #    SECURITY TAB
    def setup_security_tab(self):
        """Initialize security tab connections"""
        self.changeUsernameBtn.clicked.connect(self.change_username)
        self.changePasswordBtn.clicked.connect(self.change_password)

        # Password visibility toggles
        toggle_pairs = [
            ("passForConfirm", "showProfileIInfoPassBtn"),
            ("changeUsernamePass", "changeUsernamePassShow"),
            ("currentPassEdit", "showCurrentPass"),
            ("newPassEdit", "showNewPass"),
            ("confirmPassEdit", "showConfirmPass"),
        ]
        for line_edit_name, button_name in toggle_pairs:
            line_edit = getattr(self, line_edit_name, None)
            button = getattr(self, button_name, None)
            if line_edit is not None and button is not None:
                setup_password_toggle(line_edit, button)

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

        self._set_settings_busy(True, self.changeUsernameBtn)

        def _invalid_password():
            self._set_settings_busy(False, self.changeUsernameBtn)
            self.show_security_error("Incorrect password!")
            self.changeUsernamePass.setStyleSheet(error_style_passForConfirm)
            self.changeUsernamePass.clear()
            self.changeUsernamePass.setFocus()

        def _verify_error(err: str):
            self._set_settings_busy(False, self.changeUsernameBtn)
            self.show_security_error(f"Failed to verify password ({err})")

        def _do_update_username():
            user_id = (self.current_user or {}).get('id')
            if not user_id:
                self._set_settings_busy(False, self.changeUsernameBtn)
                self.show_security_error("No user session found")
                return

            self.api.patch(
                url=f"/api/desktop-users/{user_id}/",
                data={"username": new_username},
                on_success=lambda updated_user: self._on_username_updated(updated_user),
                on_error=lambda e: self._on_username_update_failed(e),
                timeout=15,
                show_loading=True,
                loading_title="Updating username...",
                loading_subtitle="Saving changes"
            )

        self._verify_password_async(
            password,
            on_valid=_do_update_username,
            on_invalid=_invalid_password,
            on_error=_verify_error
        )
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

        self._set_settings_busy(True, self.changePasswordBtn)

        user_id = (self.current_user or {}).get('id')
        password_data = {
            "user_id": user_id,
            "current_password": current_password,
            "new_password": new_password
        }

        def _on_changed(data):
            self._set_settings_busy(False, self.changePasswordBtn)
            if isinstance(data, dict) and data.get('success'):
                self.show_security_success("Password updated successfully!")
                self.clear_security_fields()
                self.logout_after_update()
            else:
                self.show_security_error("Failed to update password! Current password may be incorrect.")

        def _on_change_err(err: str):
            self._set_settings_busy(False, self.changePasswordBtn)
            # 400/401 shows up here as "HTTP error: <code>"
            if "HTTP error: 400" in str(err) or "HTTP error: 401" in str(err):
                self.show_security_error("Failed to update password! Current password may be incorrect.")
            else:
                self.show_security_error(f"Failed to update password ({err})")

        self.api.post(
            url="/api/desktop-change-password/",
            data=password_data,
            on_success=_on_changed,
            on_error=_on_change_err,
            timeout=15,
            show_loading=True,
            loading_title="Updating password...",
            loading_subtitle="Saving changes"
        )

    def _on_username_updated(self, updated_user):
        try:
            if isinstance(updated_user, dict) and self.current_user is not None:
                self.current_user.update(updated_user)
        except Exception:
            pass
        self._set_settings_busy(False, self.changeUsernameBtn)
        self.show_security_success("Username updated successfully!")
        self.clear_security_fields()
        self.logout_after_update()

    def _on_username_update_failed(self, err: str):
        self._set_settings_busy(False, self.changeUsernameBtn)
        self.show_security_error("Failed to update username!")
        print(f"Username update failed: {err}")

    def _set_settings_busy(self, busy: bool, *widgets):
        """Disable/enable settings action buttons during async requests."""
        for w in widgets:
            try:
                if w is not None:
                    w.setEnabled(not busy)
            except Exception:
                pass

    def _verify_password_async(self, password: str, on_valid, on_invalid, on_error=None):
        """Verify the current user's password via /api/desktop-login/ without blocking the UI."""
        username = (self.current_user or {}).get('username')
        if not username:
            if on_error:
                on_error('No username in session')
            return

        def _ok(_data):
            try:
                on_valid()
            except Exception:
                on_valid()

        def _err(err: str):
            # 400/401 means invalid credentials; other errors are connectivity/server
            if "HTTP error: 400" in str(err) or "HTTP error: 401" in str(err):
                on_invalid()
                return
            if on_error:
                on_error(err)
            else:
                on_invalid()

        self.api.post(
            url="/api/desktop-login/",
            data={"username": username, "password": password},
            on_success=_ok,
            on_error=_err,
            timeout=10,
            show_loading=True,
            loading_title="Verifying password...",
            loading_subtitle="Please wait"
        )
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
            self.changeUsernamePass.setStyleSheet(error_style_passForConfirm)
        else:
            self.changeUsernamePass.setStyleSheet(default_style_passForConfirm)

        return errors
    def validate_password_fields(self, current_password, new_password, confirm_password):
        """Validate password change fields"""
        errors = []

        if not current_password:
            errors.append("Current password is required")
            self.currentPassEdit.setStyleSheet(error_style_passForConfirm)
        else:
            self.currentPassEdit.setStyleSheet(default_style_passForConfirm)

        if not new_password:
            errors.append("New password is required")
            self.newPassEdit.setStyleSheet(error_style_passForConfirm)
        else:
            self.newPassEdit.setStyleSheet(default_style_passForConfirm)

        if not confirm_password:
            errors.append("Please confirm your new password")
            self.confirmPassEdit.setStyleSheet(error_style_passForConfirm)
        else:
            self.confirmPassEdit.setStyleSheet(default_style_passForConfirm)

        if new_password and confirm_password and new_password != confirm_password:
            errors.append("New passwords do not match")
            self.newPassEdit.setStyleSheet(error_style_passForConfirm)
            self.confirmPassEdit.setStyleSheet(error_style_passForConfirm)

        if new_password and len(new_password) < 6:  # Minimum password length
            errors.append("New password must be at least 6 characters long")
            self.newPassEdit.setStyleSheet(error_style_passForConfirm)

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
            field.setStyleSheet(default_style_passForConfirm)
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
        if not self.current_user or self.current_user.get('role') != 'admin':
            toast = Toast(self, "Only administrators can create staff accounts", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        self._set_settings_busy(True, self.addAccountBtn)

        def _on_created(data):
            self._set_settings_busy(False, self.addAccountBtn)
            try:
                staff_account = (data or {}).get('staff_account')
                if not isinstance(staff_account, dict):
                    raise ValueError('Invalid staff_account payload')
                if staff_account.get('temp_password'):
                    self.temp_passwords[staff_account['id']] = staff_account['temp_password']
                toast = Toast(
                    self,
                    f"Staff account created!\nUsername: {staff_account.get('username','')}\nPassword: {staff_account.get('temp_password','')}",
                    icon_path="Icons/check.png"
                )
                toast.show_toast()
            except Exception as e:
                print(f"Error reading staff account response: {e}")
                toast = Toast(self, "Staff account created, but response was unexpected", icon_path="Icons/check.png")
                toast.show_toast()
            self.load_staff_accounts()

        def _on_create_err(err: str):
            self._set_settings_busy(False, self.addAccountBtn)
            print(f"Error generating staff account: {err}")
            toast = Toast(self, "Failed to create staff account!", icon_path="Icons/warning.png")
            toast.show_toast()

        self.api.post(
            url="/api/desktop-create-staff/",
            data={
                'admin_id': self.current_user['id'],
                'full_name': "Staff User"
            },
            on_success=_on_created,
            on_error=_on_create_err,
            timeout=15,
            show_loading=True,
            loading_title="Creating staff account...",
            loading_subtitle="Please wait"
        )
    def load_staff_accounts(self):
        """Load all staff accounts asynchronously with loading indicator"""
        try:
            # Clear existing content
            scroll_layout = self.accountUserLayout
            if scroll_layout:
                while scroll_layout.count():
                    child = scroll_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # Show loading label while fetching
            loading_label = QLabel("Loading staff accounts...")
            loading_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addWidget(loading_label)

            # Fetch staff accounts from API asynchronously
            self.api.get(
                "/api/desktop-users/",
                on_success=self._on_staff_accounts_loaded,
                on_error=self._on_staff_accounts_error
            )

        except Exception as e:
            print(f"Error loading staff accounts: {e}")
            toast = Toast(self, "Error loading staff accounts", icon_path="Icons/warning.png")
            toast.show_toast()

    def _on_staff_accounts_loaded(self, data):
        """Callback when staff accounts data is received"""
        try:
            # Clear loading label
            scroll_layout = self.accountUserLayout
            while scroll_layout.count():
                child = scroll_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Extract staff accounts
            staff_accounts = [user for user in data.get('users', []) if user['role'] == 'staff']

            # Create all staff cards
            if staff_accounts:
                self.create_staff_cards(staff_accounts)
            else:
                empty_label = QLabel("No staff accounts")
                empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                scroll_layout.addWidget(empty_label)

        except Exception as e:
            print(f"Error processing staff accounts: {e}")
            toast = Toast(self, "Error processing staff accounts", icon_path="Icons/warning.png")
            toast.show_toast()

    def _on_staff_accounts_error(self, error_msg):
        """Callback when staff accounts loading fails"""
        print(f"Error loading staff accounts: {error_msg}")
        scroll_layout = self.accountUserLayout
        while scroll_layout.count():
            child = scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        error_label = QLabel("Failed to load staff accounts")
        error_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(255, 100, 100);")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(error_label)
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
        if not self.current_user or self.current_user.get('role') != 'admin':
            toast = Toast(self, "Only administrators can reset passwords", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # Use custom ConfirmCard instead of default QMessageBox
        username = account.get('username', 'this account')
        self.confirmCard.confirmationMessage.setText(
            f"Reset password for {username}?\n\nThis will generate new temporary credentials."
        )
        self.confirmCard.yesButton.setText("RESET")
        self.confirmCard.noButton.setText("CANCEL")
        self.confirmCard.yesButton.setStyleSheet(reset_yes_style)
        self.confirmCard.noButton.setStyleSheet(reset_no_style)

        try:
            self.confirmCard.yesButton.clicked.disconnect()
            self.confirmCard.noButton.clicked.disconnect()
        except Exception:
            pass

        def clicked_no():
            self.confirmCard.close()
            self.restore_confirm_card_default()

        def clicked_yes():
            # Hide confirm card immediately, then proceed with async call
            self.confirmCard.close()
            self.restore_confirm_card_default()

            def _on_reset(data):
                new_pw = (data or {}).get('new_password', '')
                toast = Toast(self, f"Password reset!\nNew password: {new_pw}", icon_path="Icons/check.png")
                toast.show_toast()
                self.load_staff_accounts()

            def _on_reset_err(err: str):
                print(f"Error resetting password: {err}")
                toast = Toast(self, "Failed to reset password", icon_path="Icons/warning.png")
                toast.show_toast()

            self.api.post(
                url="/api/desktop-reset-password/",
                data={
                    'admin_id': self.current_user['id'],
                    'staff_id': account['id']
                },
                on_success=_on_reset,
                on_error=_on_reset_err,
                timeout=15,
                show_loading=True,
                loading_title="Resetting password...",
                loading_subtitle="Please wait"
            )

        self.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.confirmCard.noButton.clicked.connect(clicked_no)
        self.confirmCard.show_card()
    def delete_staff_account(self, account):
        """Delete staff account"""
        if not self.current_user or self.current_user.get('role') != 'admin':
            toast = Toast(self, "Only administrators can delete accounts", icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # Use custom ConfirmCard instead of default QMessageBox
        username = account.get('username', 'this account')
        self.confirmCard.confirmationMessage.setText(
            f"Delete {username}?\n\nThis action cannot be undone."
        )
        # Keep default delete styling/text (YES/NO), but ensure correct styles
        self.confirmCard.yesButton.setText("DELETE")
        self.confirmCard.noButton.setText("CANCEL")
        self.confirmCard.yesButton.setStyleSheet(original_yes_style)
        self.confirmCard.noButton.setStyleSheet(original_no_style)

        try:
            self.confirmCard.yesButton.clicked.disconnect()
            self.confirmCard.noButton.clicked.disconnect()
        except Exception:
            pass

        def clicked_no():
            self.confirmCard.close()
            self.restore_confirm_card_default()

        def clicked_yes():
            self.confirmCard.close()
            self.restore_confirm_card_default()

            def _on_deleted(_data):
                toast = Toast(self, "Account deleted successfully", icon_path="Icons/check.png")
                toast.show_toast()
                self.load_staff_accounts()

            def _on_delete_err(err: str):
                print(f"Error deleting account: {err}")
                toast = Toast(self, "Failed to delete account", icon_path="Icons/warning.png")
                toast.show_toast()

            self.api.delete(
                url=f"/api/desktop-users/{account['id']}/",
                on_success=_on_deleted,
                on_error=_on_delete_err,
                timeout=15,
                show_loading=True,
                loading_title="Deleting account...",
                loading_subtitle="Please wait"
            )

        self.confirmCard.yesButton.clicked.connect(clicked_yes)
        self.confirmCard.noButton.clicked.connect(clicked_no)
        self.confirmCard.show_card()

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
            self.scale_widget_font(line_edit, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
        #for comboBox
        for comboBox in self.findChildren(QComboBox):
            self.scale_widget_font(comboBox, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
        # for date
        for dateEdit in self.findChildren(QDateEdit):
            self.scale_widget_font(dateEdit, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
        #owner details title label
        for title_label in self.ownerDetailsFrame.findChildren(QLabel):
            self.scale_widget_font(title_label, base_size=16, min_size=12, max_size=35, family="Rubik Mono One")
        #owner details header
        self.scale_widget_font(self.pageHeader1, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader2, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader3, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader4, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader5, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader6, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        self.scale_widget_font(self.pageHeader8, base_size=25, min_size=12, max_size=35, family="Rubik Mono One")
        # pet details title
        self.scale_widget_font(self.label_27, base_size=16, min_size=14, max_size=35, family="Rubik Mono One")
        for submitBtns in self.findChildren(QPushButton):
            self.scale_widget_font(submitBtns, base_size=14, min_size=8, max_size=25, family="Rubik Mono One")
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
                self.scale_widget_font(userNameLabel, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")

            for passwordLabel in card.findChildren(QLabel, "passwordLabel"):
                self.scale_widget_font(passwordLabel, base_size=14, min_size=8, max_size=35, family="Montserrat Medium")

            for status in card.findChildren(QLabel, "status"):
                self.scale_widget_font(status, base_size=14, min_size=8, max_size=35, family="Montserrat Medium")

            if card.profileIcon:
                self.scale_label_pixmap(card.profileIcon, min_size=50, max_size=120)

        # AppointmentsTodayCard scaling
        container = self.findChild(QWidget, "appointmentsTodayScroll")
        if container:
            appointment_cards = []
            layout = container.layout()
            if layout:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    card = item.widget()
                    if card and hasattr(card, "appointmentOwner"):
                        appointment_cards.append(card)
            self.scale_cards(appointment_cards, base_h=90)
            for card in appointment_cards:
                # Use correct font weights from .ui file
                for ownerLabel in card.findChildren(QLabel, "appointmentOwner"):
                    self.scale_widget_font(ownerLabel, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")
                for breedLabel in card.findChildren(QLabel, "appointmentBreed"):
                    self.scale_widget_font(breedLabel, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
                for petLabel in card.findChildren(QLabel, "appointmentPet"):
                    self.scale_widget_font(petLabel, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
                for serviceLabel in card.findChildren(QLabel, "appointmentService"):
                    self.scale_widget_font(serviceLabel, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
                for timeLabel in card.findChildren(QLabel, "appointmentTime"):
                    self.scale_widget_font(timeLabel, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")

    def refresh_analytics(self):

        # Force fresh data: analytics endpoints were cached for performance.
        try:
            self.api.invalidate_cache('/api/speciesCounts/')
            self.api.invalidate_cache('/api/serviceCounts/')
            self.api.invalidate_cache('/api/todaysAppointments/')
        except Exception:
            pass

        self.clear_layout(self.SpeciesPieGraph.layout())
        self.clear_layout(self.ServiceBarGraph.layout())

        self.setup_bar_graph()
        self.setup_pie_graph()
        self.appointments_today()


    def _ensure_container_layout(self, container: QWidget) -> QVBoxLayout:
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        return layout


    def _show_graph_skeleton(self, container: QWidget, kind: str = "generic"):
        """Show a lightweight skeleton placeholder inside a graph container."""
        layout = self._ensure_container_layout(container)
        self.clear_layout(layout)

        skeleton = QWidget(container)
        skeleton_layout = QVBoxLayout(skeleton)
        skeleton_layout.setContentsMargins(18, 18, 18, 18)
        skeleton_layout.setSpacing(12)

        title = QFrame()
        title.setFixedHeight(26)
        title.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

        legend = QFrame()
        legend.setFixedHeight(18)
        legend.setStyleSheet("background-color: #f0f0f0; border-radius: 6px;")

        skeleton_layout.addWidget(title)
        skeleton_layout.addWidget(legend)

        if kind == "pie":
            pie_holder = QWidget()
            pie_layout = QHBoxLayout(pie_holder)
            pie_layout.setContentsMargins(0, 0, 0, 0)
            pie_layout.setSpacing(0)

            circle = QFrame()
            # Responsive: keep reference and resize with the container.
            container._pie_skeleton_circle = circle
            container.installEventFilter(self)
            self._resize_pie_skeleton_circle(container)
            pie_layout.addStretch()
            pie_layout.addWidget(circle)
            pie_layout.addStretch()
            skeleton_layout.addWidget(pie_holder, 1)
        elif kind == "bar":
            bars_holder = QWidget()
            bars_layout = QHBoxLayout(bars_holder)
            bars_layout.setContentsMargins(0, 0, 0, 0)
            bars_layout.setSpacing(10)

            # Simple bar placeholders
            for h in (140, 200, 110, 170, 90):
                bar = QFrame()
                bar.setFixedWidth(28)
                bar.setFixedHeight(h)
                bar.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")
                bars_layout.addWidget(bar, 0, Qt.AlignmentFlag.AlignBottom)

            skeleton_layout.addStretch()
            skeleton_layout.addWidget(bars_holder, 0, Qt.AlignmentFlag.AlignHCenter)
            skeleton_layout.addStretch()
        else:
            body = QFrame()
            body.setMinimumHeight(220)
            body.setStyleSheet("background-color: #e0e0e0; border-radius: 10px;")
            skeleton_layout.addWidget(body, 1)

        layout.addWidget(skeleton)


    def _resize_pie_skeleton_circle(self, container: QWidget):
        """Resize the pie skeleton circle to track available chart area."""
        circle = getattr(container, "_pie_skeleton_circle", None)
        if circle is None:
            return

        try:
            # Approximate available chart area after margins + title/legend.
            # This keeps the skeleton from being larger than the real pie.
            horizontal_padding = 18 * 2 + 40  # skeleton margins + extra breathing room
            vertical_overhead = 18 * 2 + 26 + 12 + 18 + 40  # margins + title + spacing + legend + extra

            available_w = max(0, container.width() - horizontal_padding)
            available_h = max(0, container.height() - vertical_overhead)
            base = min(available_w, available_h)

            circle_d = int(base * 0.90)
            circle_d = max(140, min(220, circle_d))

            circle.setFixedSize(circle_d, circle_d)
            circle.setStyleSheet(f"background-color: #e0e0e0; border-radius: {circle_d // 2}px;")
        except RuntimeError:
            # The widget may have been deleted when the real chart replaced it.
            container._pie_skeleton_circle = None


    def eventFilter(self, obj, event):
        # Keep graph skeletons responsive (maximize/restore).
        if event.type() == QEvent.Type.Resize and hasattr(obj, "_pie_skeleton_circle"):
            self._resize_pie_skeleton_circle(obj)
        # ✅ Force repaint of pie chart during resize to prevent animation trails
        if event.type() == QEvent.Type.Resize and obj == self.SpeciesPieGraph:
            if hasattr(self, '_pie_chart_view') and self._pie_chart_view:
                try:
                    # Check if the widget is still valid before updating
                    if not self._pie_chart_view.isVisible():
                        return super().eventFilter(obj, event)
                    QTimer.singleShot(0, self._pie_chart_view.update)
                except RuntimeError:
                    # Chart view has been deleted, clear the reference
                    self._pie_chart_view = None
        return super().eventFilter(obj, event)


    def _show_graph_error(self, container: QWidget, message: str):
        layout = self._ensure_container_layout(container)
        self.clear_layout(layout)

        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            font: 81 14pt 'Montserrat ExtraBold';
            color: rgb(168,168,168);
            padding: 40px;
            background: transparent;
        """)
        layout.addWidget(label)


    def clear_layout(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


    def setup_bar_graph(self):
        """Load bar graph data asynchronously"""
        self._show_graph_skeleton(self.ServiceBarGraph, kind="bar")
        self.api.get(
            '/api/serviceCounts/',
            on_success=self._populate_bar_graph,
            on_error=lambda e: self._show_graph_error(self.ServiceBarGraph, "Failed to load service chart"),
            use_cache=True,
            cache_ttl=300
        )
    
    def _populate_bar_graph(self, data):
        """Populate bar graph with loaded data"""
        if data is None:
            print("BAR GRAPH ERROR — No data")
            return

        from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis

        set0 = QBarSet("Services")
        values = list(data.values())
        categories = list(data.keys())
        for v in values:
            set0.append(v)

        series = QBarSeries()
        series.append(set0)
        series.setBarWidth(0.9)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Total Every Service")
        chart.setTitleFont(QFont("Montserrat ExtraBold" ,20))

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)
        chart.legend().setFont(QFont("Montserrat", 12))


        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setAnimationDuration(1000)
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)


        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setGridLineVisible(False)
        axis_x.setMinorGridLineVisible(False)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        chart_view = QChartView(chart)

        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.ServiceBarGraph.setGraphicsEffect(shadow)
        

        layout = self.ServiceBarGraph.layout()
        if layout is None:
            layout = QVBoxLayout(self.ServiceBarGraph)

        # Remove previous charts
        while layout.count():
            old = layout.takeAt(0)
            if old.widget():
                old.widget().deleteLater()

        layout.addWidget(chart_view)
# ✅ Install event filter on container to handle resize properly
        self.SpeciesPieGraph.installEventFilter(self)
        
    def setup_pie_graph(self):
        """Load pie graph data asynchronously"""
        self._show_graph_skeleton(self.SpeciesPieGraph, kind="pie")
        self.api.get(
            '/api/speciesCounts/',
            on_success=self._populate_pie_graph,
            on_error=lambda e: self._populate_pie_graph({"dogs": 0, "cats": 0, "others": 0}),
            use_cache=True,
            cache_ttl=300
        )
    
    def _populate_pie_graph(self, data):
        """Populate pie graph with loaded data"""
        # Chart is about to replace the skeleton; clear any skeleton references.
        try:
            self.SpeciesPieGraph._pie_skeleton_circle = None
        except Exception:
            pass
        
        # Clear old chart view reference
        self._pie_chart_view = None

        if not data:
            print("PIE GRAPH — No data found, using zero fallback")
            data = {"dogs": 0, "cats": 0, "others": 0}

        from PyQt6.QtCharts import QChart, QChartView, QPieSeries

        dogs = data.get("dogs", 0)
        cats = data.get("cats", 0)
        others = data.get("others", 0)

        series = QPieSeries()
        total = dogs + cats + others

        if total == 0:
            series.append("No Data", 1)
        else:
            series.append(f"Dogs: {dogs}", dogs)
            series.append(f"Cats: {cats}", cats)
            series.append(f"Others: {others}", others)


        series.setHoleSize(0.30)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Species Distribution")
        chart.setTitleFont(QFont("Montserrat ExtraBold", 20))


        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignTop)
        chart.legend().setFont(QFont("Montserrat", 12))

        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        chart.setAnimationDuration(1000)
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)
        for s in series.slices():
            s.setExplodeDistanceFactor(0.4)
            s.setLabelVisible(False)


        series.hovered.connect(lambda slice, state: slice.setExploded(state))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.SpeciesPieGraph.setGraphicsEffect(shadow)

        layout = self.SpeciesPieGraph.layout()
        if layout is None:
            layout = QVBoxLayout(self.SpeciesPieGraph)

        # ✅ Remove previous charts
        while layout.count():
            old = layout.takeAt(0)
            if old.widget():
                old.widget().deleteLater()

        layout.addWidget(chart_view)
        
        # ✅ Update reference after adding to layout
        self._pie_chart_view = chart_view

    def appointments_today(self):
        """Load today's appointments asynchronously"""
        self.api.get(
            '/api/todaysAppointments/',
            on_success=self._on_appointments_loaded,
            on_error=lambda e: print("❌ API ERROR:", e),
            timeout=5,
            use_cache=True,
            cache_ttl=60
        )
    
    def _on_appointments_loaded(self, data):
        """Callback when appointments data is received"""

        print("DEBUG: API Response data:", data)  # 🔍 Debug: see actual response

        container = self.findChild(QWidget, "appointmentsTodayScroll")
        if not container:
            print("❌ appointmentsTodayScroll NOT FOUND")
            return

        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            container.setLayout(layout)

        label = container.findChild(QLabel, "noAppointmentToday")
        if not label:
            print("noAppointmentToday not found")
            return

        # Treat missing/None data as empty
        if not data:
            label.setVisible(True)

            # Clear everything except the empty-state label
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                widget = item.widget() if item else None
                if widget is not None and widget.objectName() == "noAppointmentToday":
                    continue
                item = layout.takeAt(i)
                if item and item.widget():
                    item.widget().deleteLater()

            return

        label.setVisible(False)

        # Clear old widgets
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget() if item else None
            if widget is not None and widget.objectName() == "noAppointmentToday":
                continue
            item = layout.takeAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        # Responsive scaling: collect cards
        appointment_cards = []

        # Populate cards
        for appt in data:
            print(f"DEBUG: Processing appointment: {appt}")  # 🔍 Debug each appointment
            card = uic.loadUi("ui-files/AppointmentsTodayCard.ui")

            card.appointmentOwner.setText(str(appt["owner"]).title())
            card.appointmentBreed.setText(str(appt["breed"]).title())
            card.appointmentPet.setText(str(appt["pet_name"]).title())
            card.appointmentService.setText(str(appt["service"]).title())

            time_obj = datetime.strptime(appt["prefTime"], "%H:%M:%S")
            card.appointmentTime.setText(time_obj.strftime("%I:%M %p"))

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(3)
            shadow.setColor(QColor(0, 0, 0, 60))
            card.setGraphicsEffect(shadow)

            # Responsive font scaling for card labels
            self.scale_widget_font(card.appointmentOwner, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")
            self.scale_widget_font(card.appointmentBreed, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
            self.scale_widget_font(card.appointmentPet, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
            self.scale_widget_font(card.appointmentService, base_size=12, min_size=8, max_size=25, family="Montserrat Medium")
            self.scale_widget_font(card.appointmentTime, base_size=14, min_size=8, max_size=35, family="Montserrat ExtraBold")

            appointment_cards.append(card)
            layout.addWidget(card)

        # Responsive card scaling
        self.scale_cards(appointment_cards, base_h=90)
        layout.addStretch()

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
    def load_office_hours(self, show_loading: bool = False):
        """Load office hours from API (non-blocking)."""

        def _on_loaded(data):
            # API returns a list; tolerate other shapes just in case
            office_hours = data
            if isinstance(data, dict) and isinstance(data.get('results'), list):
                office_hours = data.get('results')
            if not isinstance(office_hours, list):
                office_hours = []
            self.populate_office_hours(office_hours)

        def _on_err(err: str):
            Toast(self, f"Failed to load office hours", icon_path="Icons/error.png").show_toast()
            print(f"Failed to load office hours: {err}")

        self.api.get(
            url="/api/office-hours/",
            on_success=_on_loaded,
            on_error=_on_err,
            timeout=15,
            show_loading=bool(show_loading),
            loading_title="Loading office hours...",
            loading_subtitle="Please wait"
        )
    def setup_office_hours(self):
        """Initialize office hours tab"""
        # Connect buttons
        self.saveHrsBtn.clicked.connect(self.save_office_hours)
        self.resetHrsBtn.clicked.connect(self.show_reset_confirmation)  # Changed to show confirmation

        # Setup radio button groups for each day
        self.setup_day_radio_groups()

        # Setup QTimeEdit display format for all days
        self.setup_time_edit_formats()

        # Load current office hours (async; avoid blocking UI)
        self.load_office_hours(show_loading=False)
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

        # Populate UI with default values immediately
        self.populate_office_hours(default_hours)

        def _finish_confirm():
            # Always restore card and close it
            try:
                self.restore_confirm_card_default()
                self.confirmCard.close()
            except Exception:
                pass

        def _on_ok(_data):
            Toast(self, "Office hours reset to default values!", icon_path="Icons/check.png").show_toast()
            _finish_confirm()

        def _on_err(err: str):
            Toast(self, "Failed to reset office hours", icon_path="Icons/warning.png").show_toast()
            print(f"Reset office hours failed: {err}")
            _finish_confirm()

        # Save defaults to database (non-blocking + loading modal)
        self.api.post(
            url="/api/office-hours/update/",
            data=default_hours,
            on_success=_on_ok,
            on_error=_on_err,
            timeout=20,
            show_loading=True,
            loading_title="Resetting office hours...",
            loading_subtitle="Saving default values"
        )
    def save_office_hours(self):
        """Save office hours to API"""
        office_hours_data = self.collect_office_hours_data()

        def _on_ok(_data):
            Toast(self, "Office hours saved successfully!", icon_path="Icons/check.png").show_toast()
            self.load_office_hours(show_loading=False)  # Reload to confirm (async)

        def _on_err(err: str):
            Toast(self, "Failed to save office hours", icon_path="Icons/warning.png").show_toast()
            print(f"Save office hours failed: {err}")

        self.api.post(
            url="/api/office-hours/update/",
            data=office_hours_data,
            on_success=_on_ok,
            on_error=_on_err,
            timeout=20,
            show_loading=True,
            loading_title="Saving office hours...",
            loading_subtitle="Please wait"
        )
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


import os
import sys

# ETO ANG SAGGOT
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)  # Go up from frontend to Desktop_Application
project_root = os.path.dirname(project_root)  # Go up to the actual project root

# Add to path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QPushButton, QVBoxLayout, QFrame, \
    QToolButton, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate, QTimer
from PyQt6.QtGui import QPixmap
from shadowEffects import *
from input_styles import *
from toast import Toast
from config_loader import API_BASE_URL
from async_helper import AsyncHelper


class AddServicePopUp(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/addService.ui", self)

        # Use the main window's AsyncHelper if available; otherwise create our own.
        self.api = getattr(self.main_window, 'api', None)
        if self.api is None:
            self.api = AsyncHelper(self.main_window if self.main_window else self, base_url=API_BASE_URL)

        # Initialize service type state
        self.service_cards = []
        self.service_pagination_widget = None
        self.selected_service_type_id = None  # For edit mode
        self.is_edit_mode = False  # Track if we're adding or editing

        # Pagination state
        self.service_currentPage = 1
        self.total_service_pages = 1
        self.total_service_count = 0

        # Search state
        self.service_search_term = ""
        self._service_search_timer = QTimer()
        self._service_search_timer.setSingleShot(True)
        self._service_search_timer.timeout.connect(self.perform_service_search)

        # Setup graphics effects
        self.setGraphicsEffect(create_card_shadow())
        self.serviceDescription.setGraphicsEffect(create_card_shadow())
        self.serviceNameLineEdit.setGraphicsEffect(create_card_shadow())
        self.addServiceBtn.setGraphicsEffect(create_card_shadow())
        self.cancelAddServiceBtn.setGraphicsEffect(create_card_shadow())

        # Connect buttons
        self.addServiceBtn.clicked.connect(self.handle_add_edit_service)
        self.cancelAddServiceBtn.clicked.connect(self.cancel_operation)
        self.closePopUpBtn.clicked.connect(self.cancel_operation)

        # Initialize the layout
        self.setup_layout_structure()

        # Setup search functionality
        self.setup_service_search()

        # Load service types when the popup is initialized
        self.load_service_types(1)

    def setup_layout_structure(self):
        """Setup a proper layout structure with fixed pagination at bottom"""
        # Get the scroll area widget
        scroll_widget = self.main_window.availableServicesContents

        # Clear any existing layout
        QWidget().setLayout(scroll_widget.layout()) if scroll_widget.layout() else None

        # Create a main vertical layout
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a container for the cards (this will expand)
        self.cards_container = QWidget()
        self.serviceLayout = QVBoxLayout(self.cards_container)
        self.serviceLayout.setSpacing(10)
        self.serviceLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.serviceLayout.setContentsMargins(0, 0, 0, 0)

        # Add the cards container to main layout (with stretch factor to take available space)
        main_layout.addWidget(self.cards_container, 1)  # The '1' makes it expand

        # Create a fixed container for pagination at the bottom
        self.pagination_container = QWidget()
        pagination_container_layout = QVBoxLayout(self.pagination_container)
        pagination_container_layout.setContentsMargins(0, 20, 0, 20)  # Add top and bottom margin
        pagination_container_layout.setSpacing(0)

        # Add pagination container to main layout (no stretch factor)
        main_layout.addWidget(self.pagination_container, 0, Qt.AlignmentFlag.AlignHCenter)

        # Set the cards container to expand vertically
        self.cards_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set the pagination container to fixed height
        self.pagination_container.setFixedHeight(120)  # Fixed height for pagination area

    def setup_service_search(self):
        """Setup search functionality for service types"""
        # Connect search input
        if hasattr(self, 'searchServiceInput'):
            self.searchServiceInput.textEdited.connect(self.handle_service_search_input)

    def handle_service_search_input(self, text):
        """Handle service search input with debouncing"""
        self.service_search_term = text.strip()
        self._service_search_timer.start(500)

    def perform_service_search(self):
        """Perform the actual search"""
        if self.service_search_term:
            self.load_service_types(page=1, search_term=self.service_search_term)
        else:
            self.load_service_types(page=1)

    def load_service_types(self, page=1, search_term=None, show_loading: bool = False):
        """Load service types from API and display them in cards (non-blocking)."""
        # Clear existing cards + pagination immediately so the UI doesn't accumulate widgets.
        self.clear_service_cards()
        self.clear_pagination_widget()

        params = {
            "is_active": "true",
        }
        if page > 1:
            params["page"] = page
        if search_term:
            params["search"] = search_term.strip()

        def _on_success(data):
            try:
                self.service_currentPage = max(1, data.get('current_page', 1))
                self.total_service_pages = data.get('total_pages', 1)
                self.total_service_count = data.get('count', 0)

                service_types = data.get('results', [])
                if not service_types and page > 1:
                    # If this page became empty (e.g., deletion), step back one page.
                    self.load_service_types(page - 1, search_term, show_loading=False)
                    return

                if not service_types:
                    self.show_empty_state(search_term is not None)
                    if self.total_service_pages > 1:
                        self.create_pagination_controls(search_term)
                    return

                self.create_service_cards(service_types)

                if self.total_service_pages > 1:
                    self.create_pagination_controls(search_term)

            except Exception as e:
                print(f"Error processing service types: {e}")
                self.show_error_state()

        def _on_error(error_msg: str):
            print(f"Error loading service types: {error_msg}")
            self.show_error_state()

        # Use absolute endpoint path since AsyncHelper already has base_url.
        self.api.get(
            "/api/service-types/",
            params=params,
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=show_loading,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Loading services...",
            loading_subtitle="Please wait"
        )

    def clear_service_cards(self):
        """Clear all service cards from the layout"""
        # Clear all cards from the cards layout
        while self.serviceLayout.count():
            child = self.serviceLayout.takeAt(0)
            if child and child.widget():
                child.widget().deleteLater()

        # Clear the cards list
        self.service_cards = []

    def clear_pagination_widget(self):
        """Clear the pagination widget"""
        if self.service_pagination_widget:
            try:
                # Clear the pagination container layout
                layout = self.pagination_container.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child and child.widget():
                        child.widget().deleteLater()

                self.service_pagination_widget = None
            except RuntimeError:
                pass

    def create_service_cards(self, service_types):
        """Create multiple service cards from service type data"""
        self.service_cards = []

        for service_type in service_types:
            try:
                # Skip inactive service types (should already be filtered by API)
                if not service_type.get('is_active', True):
                    continue

                # Load the card UI
                card_ui = uic.loadUi("ui-files/ServiceTypeCard.ui")

                if not card_ui:
                    print("Failed to load service type card UI")
                    continue

                # Scale the card
                self.scale_cards([card_ui], base_h=83)

                # Set service type data
                card_ui.ServiceNameLabel.setText(service_type.get('name', 'Unknown Service'))

                # Set description (handle None or empty description)
                description = service_type.get('description', 'No description available')
                card_ui.descriptionLabel.setText(description or 'No description available')

                # Scale fonts
                self.scale_widget_font(
                    card_ui.ServiceNameLabel,
                    base_size=14,
                    min_size=8,
                    max_size=35,
                    family="Montserrat ExtraBold"
                )
                self.scale_widget_font(
                    card_ui.descriptionLabel,
                    base_size=14,
                    min_size=8,
                    max_size=25,
                    family="Montserrat Medium"
                )

                # Set up action buttons
                edit_btn = card_ui.findChild(QToolButton, "editBtn")
                delete_btn = card_ui.findChild(QToolButton, "deleteButton")

                if edit_btn:
                    # Connect edit button
                    edit_btn.clicked.connect(
                        lambda checked, s_id=service_type.get('id'):
                            self.main_window.updateFunction.update_service_type_info(s_id)
                    )

                if delete_btn:
                    # Connect delete button to Delete class
                    delete_btn.clicked.connect(
                        lambda checked, s_id=service_type.get('id'):
                        self.main_window.deleteFunction.start_service_type_delete(s_id)
                    )

                # Add shadow effect to card
                card_ui.serviceTypeCard.setGraphicsEffect(create_card_shadow())

                # Add to layout
                self.serviceLayout.addWidget(card_ui)
                self.service_cards.append(card_ui)

            except Exception as e:
                print(f"Error creating service card: {e}")
                continue

    def delete_service_type_with_confirmation(self, service_type_id):
        """Handle service type deletion using the Delete class pattern"""
        def _on_success(service_type):
            service_name = service_type.get('name', 'this service type')

            if hasattr(self.main_window, 'deleteFunction'):
                from PyQt6.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self.main_window,
                    "Delete Service Type",
                    f"Are you sure you want to delete '{service_name}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    self.main_window.deleteFunction.delete_service_type(service_type_id, service_name)

        def _on_error(msg: str):
            print(f"Error in delete confirmation: {msg}")
            if self.main_window:
                Toast(self.main_window, "Failed to load service type",
                      icon_path="Icons/warning.png").show_toast()

        self.api.get(
            f"/api/service-types/{service_type_id}/",
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Loading service...",
            loading_subtitle="Please wait"
        )

    def create_pagination_controls(self, search_term=None):
        """Create pagination controls in the fixed bottom container"""
        try:
            # Create pagination widget
            self.service_pagination_widget = uic.loadUi("ui-files/paginationUi.ui")

            # Connect prev/next buttons with search term
            self.service_pagination_widget.PrevPage.clicked.connect(
                lambda: self.load_service_types(self.service_currentPage - 1, search_term)
            )
            self.service_pagination_widget.NextPage.clicked.connect(
                lambda: self.load_service_types(self.service_currentPage + 1, search_term)
            )

            # Set button states
            self.service_pagination_widget.PrevPage.setEnabled(self.service_currentPage > 1)
            self.service_pagination_widget.NextPage.setEnabled(self.service_currentPage < self.total_service_pages)

            # Create page buttons with search support
            self.create_service_page_buttons(search_term)

            self.service_pagination_widget.frame_59.setGraphicsEffect(create_card_shadow())

            # Add to pagination container layout
            pagination_layout = self.pagination_container.layout()
            pagination_layout.addWidget(self.service_pagination_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        except Exception as e:
            print(f"Error creating service pagination: {e}")

    def create_service_page_buttons(self, search_term=None):
        """Create page number buttons for service type pagination"""
        if not self.service_pagination_widget:
            return

        page_layout = self.service_pagination_widget.pageButtonsLayout

        # Clear existing buttons
        while page_layout.count():
            child = page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_page = self.service_currentPage
        total_pages = self.total_service_pages
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
                page_btn.clicked.connect(lambda checked, p=page: self.load_service_types(p, search_term))

            page_layout.addWidget(page_btn)

    def show_empty_state(self, is_search):
        """Show empty state message when no service types are found"""
        empty_label = QLabel()

        if is_search:
            empty_label.setText("No service types found")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color: rgb(168, 168, 168);")
        else:
            empty_label.setText("NO SERVICE TYPES")
            empty_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")

        # Add to cards container with stretch to center it
        self.serviceLayout.addStretch()
        self.serviceLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.serviceLayout.addStretch()

    def show_error_state(self):
        """Show error state when loading fails"""
        error_label = QLabel("ERROR LOADING SERVICE TYPES")
        error_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(255,100,100);")

        # Add to cards container with stretch to center it
        self.serviceLayout.addStretch()
        self.serviceLayout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.serviceLayout.addStretch()

    def edit_service_type(self, service_type_id):
        """Handle service type edit - populate the form with existing data"""
        def _on_success(service_type):
            self.serviceNameLineEdit.setText(service_type.get('name', ''))
            self.serviceDescription.setPlainText(service_type.get('description', ''))

            self.selected_service_type_id = service_type_id
            self.is_edit_mode = True

            self.addServiceBtn.setText("UPDATE SERVICE")
            self.newServiceHeader.setText("EDIT SERVICE TYPE")
            self.serviceNameLineEdit.setFocus()

            if self.main_window:
                Toast(self.main_window, f"Editing '{service_type.get('name')}'",
                      icon_path="Icons/info.png").show_toast()

        def _on_error(msg: str):
            print(f"Error loading service type: {msg}")
            if self.main_window:
                Toast(self.main_window, "Failed to load service type details",
                      icon_path="Icons/warning.png").show_toast()

        self.api.get(
            f"/api/service-types/{service_type_id}/",
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Loading service...",
            loading_subtitle="Please wait"
        )

    def handle_add_edit_service(self):
        name = self.serviceNameLineEdit.text().strip()
        desc = self.serviceDescription.toPlainText().strip()

        if not name:
            Toast(self.main_window, "Service name is required", icon_path="Icons/warning.png").show_toast()
            return

        # --------------------------
        # EDIT MODE
        # --------------------------
        if self.is_edit_mode and self.selected_service_type_id:
            payload = {"name": name, "description": desc}

            def _on_success(_data):
                Toast(self.main_window, "Service updated!", icon_path="Icons/check.png").show_toast()
                self.reset_add_form()
                self.load_service_types(1, show_loading=False)
                if hasattr(self.main_window, 'addAppointmentCard'):
                    self.main_window.addAppointmentCard.load_service_types_to_combobox()

            def _on_error(msg: str):
                Toast(self.main_window, f"Failed to update service: {msg}", icon_path="Icons/warning.png").show_toast()

            self.api.put(
                f"/api/service-types/{self.selected_service_type_id}/",
                data=payload,
                on_success=_on_success,
                on_error=_on_error,
                timeout=15,
                show_loading=True,
                loading_widget=self.main_window if self.main_window else self,
                loading_title="Updating service...",
                loading_subtitle="Please wait"
            )
            return

        # --------------------------
        # ADD MODE
        # --------------------------
        payload = {"name": name, "description": desc}

        def _on_success(_data):
            Toast(self.main_window, "Service added!", icon_path="Icons/check.png").show_toast()
            self.reset_add_form()
            self.load_service_types(1, show_loading=False)
            if hasattr(self.main_window, 'addAppointmentCard'):
                self.main_window.addAppointmentCard.load_service_types_to_combobox()

        def _on_error(msg: str):
            Toast(self.main_window, f"Failed to add service: {msg}", icon_path="Icons/warning.png").show_toast()

        self.api.post(
            "/api/service-types/",
            data=payload,
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Adding service...",
            loading_subtitle="Please wait"
        )

    def reset_add_form(self):
        self.is_edit_mode = False
        self.selected_service_type_id = None
        self.addServiceBtn.setText("ADD SERVICE")
        self.serviceNameLineEdit.clear()
        self.serviceDescription.clear()
        self.hide()

    def create_service_type(self, service_data):
        """Create a new service type"""
        def _on_success(_data):
            self.clear_form()
            self.load_service_types(self.service_currentPage, show_loading=False)
            Toast(self.main_window, "Service type created successfully!", icon_path="Icons/check.png").show_toast()

        def _on_error(msg: str):
            Toast(self.main_window, f"Failed to create service type: {msg}", icon_path="Icons/warning.png").show_toast()

        self.api.post(
            "/api/service-types/",
            data=service_data,
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Saving...",
            loading_subtitle="Please wait"
        )

    def update_service_type(self, service_data):
        """Update an existing service type"""
        def _on_success(_data):
            self.reset_form()
            self.load_service_types(self.service_currentPage, show_loading=False)
            Toast(self.main_window, "Service type updated successfully!", icon_path="Icons/check.png").show_toast()

        def _on_error(msg: str):
            Toast(self.main_window, f"Failed to update service type: {msg}", icon_path="Icons/warning.png").show_toast()

        self.api.put(
            f"/api/service-types/{self.selected_service_type_id}/",
            data=service_data,
            on_success=_on_success,
            on_error=_on_error,
            timeout=15,
            show_loading=True,
            loading_widget=self.main_window if self.main_window else self,
            loading_title="Saving...",
            loading_subtitle="Please wait"
        )

    def cancel_operation(self):
        """Cancel the current operation (add or edit)"""
        self.reset_form()
        self.hide()

    def clear_form(self):
        """Clear the form fields"""
        self.serviceNameLineEdit.clear()
        self.serviceDescription.clear()

    def reset_form(self):
        """Reset the form to add mode"""
        self.clear_form()
        self.selected_service_type_id = None
        self.is_edit_mode = False
        self.addServiceBtn.setText("ADD SERVICE")
        self.newServiceHeader.setText("ADD NEW SERVICE")

    def scale_cards(self, cards, base_h=83, design_height=720):
        """Scale the height of a list of cards based on window size"""
        if not cards:
            return

        h_scale = self.main_window.height() / design_height
        new_h = int(base_h * h_scale)

        for card in cards:
            if card:
                card.setFixedHeight(new_h)

    def scale_widget_font(self, widget, base_size, min_size=8, max_size=20, family=None):
        """Scale widget font based on window size"""
        if not widget:
            return

        w_scale = self.main_window.width() / 1280
        h_scale = self.main_window.height() / 720
        scale = min(w_scale, h_scale)

        scaled_size = int(base_size * scale)
        final_size = max(min_size, min(scaled_size, max_size))

        f = widget.font()
        if family:
            f.setFamily(family)
        f.setPointSize(final_size)
        widget.setFont(f)

    def show_card(self):
        """Show the popup card with animation"""
        # Reset form to add mode each time we show the popup
        self.reset_form()

        if self.parent():
            parent_widget = self.parent()
            # Center in parent
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
        self.anim = anim  # Keep reference to prevent garbage collection

        # Reload service types after showing to avoid blocking the UI.
        self.load_service_types(1, show_loading=True)

    def eventFilter(self, obj, event):
        """Handle resize events to keep the popup centered"""
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # Re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)
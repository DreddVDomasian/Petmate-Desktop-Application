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
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QPushButton, QVBoxLayout, QToolButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate, QTimer
from PyQt6.QtGui import QPixmap
from shadowEffects import *
from input_styles import *
from toast import Toast
from config_loader import API_BASE_URL
import requests


class AddServicePopUp(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi("ui-files/addService.ui", self)
        self.setGraphicsEffect(create_card_shadow())
        self.serviceDescription.setGraphicsEffect(create_card_shadow())
        self.serviceNameLineEdit.setGraphicsEffect(create_card_shadow())
        self.addServiceBtn.setGraphicsEffect(create_card_shadow())
        self.cancelAddServiceBtn.setGraphicsEffect(create_card_shadow())

        # Initialize service type state
        self.service_cards = []
        self.service_pagination_widget = None

        # Pagination state
        self.service_currentPage = 1
        self.total_service_pages = 1
        self.total_service_count = 0

        # Search state
        self.service_search_term = ""
        self._service_search_timer = QTimer()
        self._service_search_timer.setSingleShot(True)
        self._service_search_timer.timeout.connect(self.perform_service_search)

        # Initialize the layout
        self.setup_stackLayout()

        # Setup search functionality
        self.setup_service_search()

        # Load service types when the popup is initialized
        self.load_service_types(1)

    def setup_stackLayout(self):
        """Setup the layout for service type cards"""
        self.serviceLayout = self.main_window.availableServicesContents.layout()
        self.serviceLayout.setSpacing(10)
        self.serviceLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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

    def load_service_types(self, page=1, search_term=None):
        """Load service types from API and display them in cards"""
        try:
            # Clear existing content
            while self.serviceLayout.count():
                child = self.serviceLayout.takeAt(0)
                if child and child.widget():
                    child.widget().deleteLater()

            # Clear existing pagination widget
            if self.service_pagination_widget:
                try:
                    self.service_pagination_widget.deleteLater()
                except RuntimeError:
                    pass
                self.service_pagination_widget = None

            # Build API URL with pagination and search
            url = f"{API_BASE_URL}/api/service-types/"
            params = []

            if page > 1:
                params.append(f"page={page}")

            if search_term:
                import urllib.parse
                encoded_term = urllib.parse.quote(search_term.strip())
                params.append(f"search={encoded_term}")

            # Only show active service types by default
            params.append("is_active=true")

            if params:
                url += "?" + "&".join(params)

            # Fetch service types from API
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extract pagination info
                self.service_currentPage = max(1, data.get('current_page', 1))
                self.total_service_pages = data.get('total_pages', 1)
                self.total_service_count = data.get('count', 0)

                # Get service types
                service_types = data.get('results', [])

                # Handle empty response
                if not service_types:
                    self.show_empty_state(search_term is not None)
                    return

                # Create service type cards
                self.create_service_cards(service_types)

                # Add pagination controls
                self.add_service_pagination_controls(search_term)

            else:
                self.show_error_state()

        except Exception as e:
            print(f"Error loading service types: {e}")
            self.show_error_state()

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
                        lambda checked, s_id=service_type.get('id'): self.edit_service_type(s_id)
                    )

                if delete_btn:
                    # Connect delete button
                    delete_btn.clicked.connect(
                        lambda checked, s_id=service_type.get('id'): self.delete_service_type(s_id)
                    )

                # Add shadow effect to card
                card_ui.serviceTypeCard.setGraphicsEffect(create_card_shadow())

                # Add to layout
                self.serviceLayout.addWidget(card_ui)
                self.service_cards.append(card_ui)

            except Exception as e:
                print(f"Error creating service card: {e}")
                continue

    def add_service_pagination_controls(self, search_term=None):
        """Add pagination controls for service types"""
        if self.total_service_pages <= 1:
            return

        try:
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
            self.serviceLayout.addWidget(self.service_pagination_widget)

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

        self.serviceLayout.addStretch()
        self.serviceLayout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.serviceLayout.addStretch()

    def show_error_state(self):
        """Show error state when loading fails"""
        error_label = QLabel("ERROR LOADING SERVICE TYPES")
        error_label.setStyleSheet("font: 81 16pt 'Montserrat ExtraBold'; color:rgb(255,100,100);")
        self.serviceLayout.addStretch()
        self.serviceLayout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.serviceLayout.addStretch()

    def edit_service_type(self, service_type_id):
        """Handle service type edit"""
        print(f"Editing service type {service_type_id}")
        # TODO: Implement edit functionality
        toast = Toast(self, f"Edit service type {service_type_id}", icon_path="Icons/info.png")
        toast.show_toast()

    def delete_service_type(self, service_type_id):
        """Handle service type deletion"""
        print(f"Deleting service type {service_type_id}")
        # TODO: Implement delete functionality with confirmation
        toast = Toast(self, f"Delete service type {service_type_id}", icon_path="Icons/warning.png")
        toast.show_toast()

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
        # Reload service types each time the popup is shown
        self.load_service_types(1)

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

    def eventFilter(self, obj, event):
        """Handle resize events to keep the popup centered"""
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # Re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)
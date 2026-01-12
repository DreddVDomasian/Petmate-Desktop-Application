from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class SkeletonLoader:
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.skeleton_overlays = {}

    def show_skeleton_for_scroll_area(self, scroll_area_widget, skeleton_type="list", item_count=5, card_height=90):
        """Show skeleton loading for scroll area content widget"""
        # Store original visibility
        scroll_area_widget.original_children = []
        for i in range(scroll_area_widget.layout().count()):
            item = scroll_area_widget.layout().itemAt(i)
            if item and item.widget():
                scroll_area_widget.original_children.append(item.widget())
                item.widget().hide()

        # Create skeleton overlay
        skeleton_id = id(scroll_area_widget)
        if skeleton_id in self.skeleton_overlays:
            self.skeleton_overlays[skeleton_id].deleteLater()

        skeleton_overlay = self._create_scroll_area_skeleton(scroll_area_widget, skeleton_type, item_count, card_height)
        self.skeleton_overlays[skeleton_id] = skeleton_overlay
        skeleton_overlay.show()

        return skeleton_overlay

    def hide_skeleton_for_scroll_area(self, scroll_area_widget):
        """Hide skeleton loading and show original content"""
        skeleton_id = id(scroll_area_widget)
        if skeleton_id in self.skeleton_overlays:
            self.skeleton_overlays[skeleton_id].deleteLater()
            del self.skeleton_overlays[skeleton_id]

        # Restore original children visibility
        if hasattr(scroll_area_widget, 'original_children'):
            for widget in scroll_area_widget.original_children:
                widget.show()
            delattr(scroll_area_widget, 'original_children')

    def _create_scroll_area_skeleton(self, scroll_area_widget, skeleton_type, item_count, card_height):
        """Create skeleton that matches the scroll area's layout"""
        skeleton_overlay = QWidget(scroll_area_widget)
        skeleton_overlay.setGeometry(scroll_area_widget.rect())
        skeleton_overlay.setStyleSheet("background-color: transparent;")

        # Copy the original layout structure
        original_layout = scroll_area_widget.layout()
        if isinstance(original_layout, QVBoxLayout):
            skeleton_layout = QVBoxLayout(skeleton_overlay)
        elif isinstance(original_layout, QGridLayout):
            skeleton_layout = QGridLayout(skeleton_overlay)
        else:
            skeleton_layout = QVBoxLayout(skeleton_overlay)

        skeleton_layout.setContentsMargins(original_layout.contentsMargins())
        skeleton_layout.setSpacing(original_layout.spacing())
        skeleton_layout.setAlignment(original_layout.alignment())

        if skeleton_type == "patient_list":
            self._create_patient_list_skeleton(skeleton_layout, item_count, card_height)
        elif skeleton_type == "pet_grid":
            self._create_pet_grid_skeleton(skeleton_layout, item_count)
        elif skeleton_type == "service_list":
            self._create_service_list_skeleton(skeleton_layout, item_count)
        elif skeleton_type == "appointment_list":
            self._create_appointment_list_skeleton(skeleton_layout, item_count)
        else:
            self._create_generic_list_skeleton(skeleton_layout, item_count, card_height)

        return skeleton_overlay

    def _create_patient_list_skeleton(self, layout, item_count, card_height):
        """Skeleton for patient cards (like in PatientCard.ui)"""
        for i in range(item_count):
            card = QWidget()
            card.setFixedHeight(card_height)
            card.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                border: 1px solid #f0f0f0;
            """)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(15, 10, 15, 10)
            card_layout.setSpacing(15)

            # Profile icon placeholder
            icon_frame = QFrame()
            icon_frame.setFixedSize(50, 50)
            icon_frame.setStyleSheet("background-color: #e0e0e0; border-radius: 25px;")

            # Text content
            text_widget = QWidget()
            text_layout = QVBoxLayout(text_widget)
            text_layout.setSpacing(8)
            text_layout.setContentsMargins(0, 0, 0, 0)

            # Name placeholder (wider)
            name_label = QLabel()
            name_label.setFixedHeight(20)
            name_label.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            # Email placeholder (medium width)
            email_label = QLabel()
            email_label.setFixedHeight(16)
            email_label.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            email_label.setFixedWidth(200)

            text_layout.addWidget(name_label)
            text_layout.addWidget(email_label)
            text_layout.addStretch()

            # Buttons area (right side)
            buttons_widget = QWidget()
            buttons_layout = QHBoxLayout(buttons_widget)
            buttons_layout.setSpacing(5)
            buttons_layout.setContentsMargins(0, 0, 0, 0)

            # Edit button placeholder
            edit_btn = QLabel()
            edit_btn.setFixedSize(30, 30)
            edit_btn.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            # Delete button placeholder
            delete_btn = QLabel()
            delete_btn.setFixedSize(30, 30)
            delete_btn.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            buttons_layout.addWidget(edit_btn)
            buttons_layout.addWidget(delete_btn)
            buttons_layout.addStretch()

            card_layout.addWidget(icon_frame)
            card_layout.addWidget(text_widget, 1)
            card_layout.addWidget(buttons_widget)

            self._add_shimmer_effect(card)
            layout.addWidget(card)

    def _create_pet_grid_skeleton(self, layout, item_count):
        """Skeleton for pet grid cards (like in petRecordCard.ui)"""
        container = QWidget()
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Calculate grid dimensions (similar to your actual grid)
        cols = 2
        rows = (item_count + cols - 1) // cols

        for i in range(item_count):
            row = i // cols
            col = i % cols

            card = QWidget()
            card.setFixedSize(180, 120)
            card.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                border: 1px solid #f0f0f0;
            """)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(10)

            # Pet icon
            pet_icon = QLabel()
            pet_icon.setFixedSize(40, 40)
            pet_icon.setStyleSheet("background-color: #e0e0e0; border-radius: 8px;")

            # Pet name
            pet_name = QLabel()
            pet_name.setFixedHeight(18)
            pet_name.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            # Species/Breed
            details = QLabel()
            details.setFixedHeight(14)
            details.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")

            card_layout.addWidget(pet_icon, 0, Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(pet_name)
            card_layout.addWidget(details)
            card_layout.addStretch()

            self._add_shimmer_effect(card)
            grid_layout.addWidget(card, row, col)

        layout.addWidget(container)

    def _create_service_list_skeleton(self, layout, item_count):
        """Skeleton for service history cards (like in serviceCard.ui)"""
        for i in range(item_count):
            card = QWidget()
            card.setFixedHeight(100)
            card.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                border: 1px solid #f0f0f0;
            """)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            # Upper section (service type and date)
            upper_section = QWidget()
            upper_layout = QHBoxLayout(upper_section)
            upper_layout.setContentsMargins(0, 0, 0, 0)

            # Service type
            service_type = QLabel()
            service_type.setFixedHeight(18)
            service_type.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")
            service_type.setFixedWidth(150)

            # Date
            service_date = QLabel()
            service_date.setFixedHeight(16)
            service_date.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            service_date.setFixedWidth(100)

            upper_layout.addWidget(service_type)
            upper_layout.addStretch()
            upper_layout.addWidget(service_date)

            # Lower section (notes and return date)
            lower_section = QWidget()
            lower_layout = QHBoxLayout(lower_section)
            lower_layout.setContentsMargins(0, 0, 0, 0)

            # Notes
            notes = QLabel()
            notes.setFixedHeight(14)
            notes.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")

            # Return date
            return_date = QLabel()
            return_date.setFixedHeight(14)
            return_date.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            return_date.setFixedWidth(80)

            lower_layout.addWidget(notes, 1)
            lower_layout.addWidget(return_date)

            card_layout.addWidget(upper_section)
            card_layout.addWidget(lower_section)

            self._add_shimmer_effect(card)
            layout.addWidget(card)

    def _create_appointment_list_skeleton(self, layout, item_count):
        """Skeleton for appointment cards (like in appointmentCard.ui)"""
        for i in range(item_count):
            card = QWidget()
            card.setFixedHeight(80)
            card.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                border: 1px solid #f0f0f0;
            """)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(15, 10, 15, 10)
            card_layout.setSpacing(15)

            # Left content
            left_widget = QWidget()
            left_layout = QVBoxLayout(left_widget)
            left_layout.setSpacing(5)
            left_layout.setContentsMargins(0, 0, 0, 0)

            # Owner name
            owner_name = QLabel()
            owner_name.setFixedHeight(18)
            owner_name.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            # Pet and service
            pet_service = QLabel()
            pet_service.setFixedHeight(14)
            pet_service.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")

            left_layout.addWidget(owner_name)
            left_layout.addWidget(pet_service)
            left_layout.addStretch()

            # Right content (date/time)
            right_widget = QWidget()
            right_layout = QVBoxLayout(right_widget)
            right_layout.setSpacing(5)
            right_layout.setContentsMargins(0, 0, 0, 0)

            # Date
            app_date = QLabel()
            app_date.setFixedHeight(14)
            app_date.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            app_date.setFixedWidth(80)

            # Time
            app_time = QLabel()
            app_time.setFixedHeight(14)
            app_time.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
            app_time.setFixedWidth(60)

            right_layout.addWidget(app_date)
            right_layout.addWidget(app_time)
            right_layout.addStretch()

            card_layout.addWidget(left_widget, 1)
            card_layout.addWidget(right_widget)

            self._add_shimmer_effect(card)
            layout.addWidget(card)

    def _create_generic_list_skeleton(self, layout, item_count, card_height):
        """Generic list skeleton as fallback"""
        for i in range(item_count):
            item = QWidget()
            item.setFixedHeight(card_height)
            item.setStyleSheet("background-color: white; border-radius: 8px;")

            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(15, 10, 15, 10)

            # Simple placeholder
            placeholder = QLabel()
            placeholder.setFixedHeight(20)
            placeholder.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")

            item_layout.addWidget(placeholder)

            self._add_shimmer_effect(item)
            layout.addWidget(item)

    def _add_shimmer_effect(self, widget):
        """Add shimmer animation to skeleton element"""
        effect = ShimmerEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.start_animation()


class ShimmerEffect(QGraphicsEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(0.4)
        self.animation.setEndValue(0.8)
        self.animation.setLoopCount(-1)

    def start_animation(self):
        self.animation.start()

    def stop_animation(self):
        self.animation.stop()
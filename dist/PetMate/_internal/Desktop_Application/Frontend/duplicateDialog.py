import os
import sys
from Desktop_Application.Frontend.app import resource_path
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLabel,QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from Desktop_Application.Frontend.shadowEffects import *


class DuplicateDialog(QWidget):
    def __init__(self, duplicates, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        uic.loadUi(resource_path("ui-files/duplicateDialog.ui"), self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # Layout inside scrollAreaWidgetContents where cards will be added
        self.duplicateListLayout = self.scrollAreaWidgetContents.layout()
        self.duplicateListLayout.setSpacing(10)
        self.duplicateListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Populate immediately if duplicates are passed
        self.populate_cards(duplicates)
        self.duplicationDialogFrame.setGraphicsEffect(create_card_shadow())

        #CancelBTN
        self.CancelBtn.clicked.connect(self.reject_dialog)
        #add anyway
        self.AddAnywayBtn.clicked.connect(self.add_anyway)
        if parent:
            parent.installEventFilter(self)
    def reject_dialog(self):
        self.close()
    def show_modal(self):
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
        self.anim = anim   # keep reference

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == event.Type.Resize:
            if self.isVisible():
                # re-center
                x = (obj.width() - self.width()) // 2
                y = (obj.height() - self.height()) // 2
                self.move(x, y)
        return super().eventFilter(obj, event)

    def populate_cards(self, duplicates):
        # Clear old cards
        while self.duplicateListLayout.count():
            child = self.duplicateListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new cards
        for entry in duplicates:
            card = uic.loadUi(resource_path("ui-files/duplicateCard.ui"))
            card.setGraphicsEffect(create_card_shadow())
            patient = entry["patient"]
            pets = entry["pets"]

            # ---- Fill in patient labels ----
            name_parts = [patient.get("lastName"), patient.get("firstName"), patient.get("middleName")]
            full_name = " ".join([p for p in name_parts if p])

            address_parts = [patient.get("barangay", ""), patient.get("city", ""), patient.get("province", "")]
            full_address = ", ".join([a for a in address_parts if a])

            contacts = [patient.get("phoneNumber"), patient.get("emergencyNumber")]
            contactNumbers = " / ".join([c for c in contacts if c])

            card.fullnameLabel.setText(full_name.title())
            card.emailLabel.setText(patient.get("email", "N/A").title())
            card.address.setText(full_address.title())
            card.contactNo.setText(contactNumbers)

            card.duplicateUpdateBtn.clicked.connect(lambda _, updateId = patient['id']: self.update_duplicate(updateId))

            # ---- Handle pets scroll area ----
            # Get the container widget from your duplicateCard.ui
            pets_container = card.petsScrollAreaWidgetContents

            # Ensure it has a layout
            if not pets_container.layout():
                pets_layout = QVBoxLayout(pets_container)
                pets_container.setLayout(pets_layout)
            else:
                pets_layout = pets_container.layout()

            # Populate pets inside this card
            self.populate_pets(pets_layout, pets)

            # Add this card into the dialog's list layout
            self.duplicateListLayout.addWidget(card)

        # Add stretch at the bottom (optional for spacing)
        self.duplicateListLayout.addStretch()

    def update_duplicate(self, updateId):
        self.close()
        self.main_window.updateFunction.update_patient_info(updateId)

    def add_anyway(self):
        if self.main_window:
            self.main_window.ignore_duplicates = True
            self.close()
            # re-run submit_data with the same form
            self.main_window.submit_data()


    def populate_pets(self, layout, pets):
        # Clear old labels
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Add a QLabel for each pet
        if pets:
            for pet in pets:
                pet_name = pet.get("petName", "Unnamed Pet").upper()
                label = QLabel(pet_name)
                label.setStyleSheet("font: 81 11pt 'Montserrat ExtraBold'; color:rgb(39,39,39);")
                layout.addWidget(label)
        else:
            no_pets_label = QLabel("No pets recorded")
            no_pets_label.setStyleSheet("font: 81 11pt 'Montserrat ExtraBold'; color:rgb(168,168,168);")
            layout.addWidget(no_pets_label)

        layout.addStretch()

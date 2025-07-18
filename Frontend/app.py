from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
from PyQt6 import uic
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import resources_rc
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QIcon, QAction
from uiLogic import UIHandler
from Backend.sendData import save_data_to_db
from toast import Toast
import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'Backend')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.myproject.settings")
django.setup()



class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("Home.ui", self)

        self.ui_handler = UIHandler(self.provinceComboBox, self.cityComboBox, self.barangayComboBox)
        self.ui_handler.load_provinces()

        #Changing main Page
        self.stackedWidget.setCurrentIndex(0)
        self.homeBtn.clicked.connect(lambda: self.navigate_to_page(0))
        self.addPatientBtn.clicked.connect(lambda: self.navigate_to_page(1))
        self.petRecordsBtn.clicked.connect(lambda: self.navigate_to_page(2))
        self.appointmentBtn.clicked.connect(lambda: self.navigate_to_page(3))
        self.schedVaxBtn.clicked.connect(lambda: self.navigate_to_page(4))

        self.confirmButton.clicked.connect(self.submit_data)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        self.dropShadow.setGraphicsEffect(shadow)

    def submit_data(self):
        required_fields = {
            "First Name": self.firstNameEdit,
            "Last Name": self.lastNameEdit,
            "Phone Number": self.phoneNumberEdit,
            "Province": self.provinceComboBox,
            "City": self.cityComboBox,
            "Barangay": self.barangayComboBox,
            "Detailed Address": self.detailedAddressEdit,
            "Email": self.emailEdit,
            "Emergency Number": self.emergencyNoEdit
        }

        missing = []

        default_style = """
            QLineEdit {
                border-right: 2px solid #cccccc;
                border-bottom: 2px solid #cccccc;
                border-radius: 5px;
	
	            font: 57 12pt 'Montserrat Medium';
	            color:rgb(39, 39, 39);
	            padding-left: 10px;
            }"""

        error_style = """
            QLineEdit {
                border: 1px solid #ff4f61;
                border-radius: 5px;

                font: 57 12pt 'Montserrat Medium';
                color:rgb(39, 39, 39);
                padding-left: 10px;
            }"""

        for name, widget in required_fields.items():
            text = widget.currentText() if "ComboBox" in widget.__class__.__name__ else widget.text()
            if not text.strip():
                widget.setStyleSheet(error_style)  # 🔴 highlight invalid
                missing.append(name)
            else:
                widget.setStyleSheet(default_style)  # ✅ reset style

        if missing:
            message = "The following fields are required:\n• " + "\n• ".join(missing)
            toast = Toast(self, message, icon_path="Icons/warning.png")
            toast.show_toast()
            return

        # ✅ If all good, save and show success
        save_data_to_db(
            self.firstNameEdit.text(),
            self.lastNameEdit.text(),
            self.phoneNumberEdit.text(),
            self.provinceComboBox.currentText(),
            self.cityComboBox.currentText(),
            self.barangayComboBox.currentText(),
            self.detailedAddressEdit.text(),
            self.emailEdit.text(),
            self.emergencyNoEdit.text()
        )

        self.navigate_to_page(2)
        toast = Toast(self, "Successfully Added!", icon_path="Icons/check.png")
        toast.show_toast()

    def navigate_to_page(self, index):
        self.stackedWidget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)


    font_path = os.path.join(os.path.dirname(__file__), "font/Montserrat/Montserrat-VariableFont_wght.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    ui = MainUI()
    ui.show()
    app.exec()



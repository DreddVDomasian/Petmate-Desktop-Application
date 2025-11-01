# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addAppointmentCard.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(743, 451)
        Form.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addPopUPFrame = QFrame(Form)
        self.addPopUPFrame.setObjectName(u"addPopUPFrame")
        self.addPopUPFrame.setStyleSheet(u"#addPopUPFrame{\n"
"	background-color: qlineargradient(\n"
"		 y1: 0, x1: 0, y2: 1, x2: 0,\n"
"		 stop: 0 #78B3CE, \n"
"    	 stop: 1 #D0F0FF\n"
"	);\n"
"	border-radius:15px;\n"
"}\n"
"\n"
"QDateEdit {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"QDateEdit::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 40px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    image: url(:/Icons/Icons/calendar.png);\n"
"    width: 30px;\n"
"    height: 30px;\n"
"}\n"
"\n"
"QComboBox {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"\n"
"}\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"    border: none; "
                        "\n"
"}\n"
"QComboBox:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"QComboBox::drop-down {\n"
"    background-color: transparent;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons/Icons/downArrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"/* Dropdown list */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(232, 232, 232);\n"
"    selection-background-color: rgb(217, 217, 217); \n"
"    selection-color: black;\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    outline: none;\n"
"	border:1px solid rgb(209, 209, 209);\n"
"}\n"
"\n"
"/* List items */\n"
"QComboBox QAbstractItemView::item {\n"
"    background-color:  rgb(232, 232, 232);\n"
"	color:rgb(39, 39, 39);\n"
"    height: 25px;\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: rgb(193, 193, 193);\n"
"    color"
                        ": black;\n"
"}\n"
"\n"
"/* Scrollbar inside dropdown */\n"
"QComboBox QAbstractItemView QScrollBar:vertical {\n"
"    background-color: transparent; /* or set a solid color */\n"
"    width: 10px;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView QScrollBar::add-line:vertical,\n"
"QComboBox QAbstractItemView QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"QComboBox QAbstractItemView QScrollBar,\n"
"QComboBox QAbstractItemView QScrollBar::handle,\n"
"QComboBox QAbstractItemView QScrollBar::groo"
                        "ve {\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    color: rgb(39, 39, 39);\n"
"    border: none; /* optional para di mag mukhang double border */\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTimeEdit {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 10px;\n"
"\n"
"}\n"
"\n"
"QTimeEdit::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    image: url(:/Icons/Icons/upArrow.png); /* custom icon */\n"
"    background: transparent;\n"
"    border: none;\n"
"    padding-right: 10px;\n"
"	padding-top: 5px;\n"
"}\n"
"\n"
"QTimeEdit::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    image:url(:/Icons/Icons/downArrow.png); /* custom "
                        "icon */\n"
"    background: transparent;\n"
"    border: none;\n"
"    padding-right: 10px;\n"
"	padding-bottom: 5px;\n"
"}")
        self.addPopUPFrame.setFrameShape(QFrame.StyledPanel)
        self.addPopUPFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.addPopUPFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_9 = QFrame(self.addPopUPFrame)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(20, 0, 0, 0)
        self.addAppointmentHeader = QLabel(self.frame_9)
        self.addAppointmentHeader.setObjectName(u"addAppointmentHeader")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addAppointmentHeader.sizePolicy().hasHeightForWidth())
        self.addAppointmentHeader.setSizePolicy(sizePolicy1)
        self.addAppointmentHeader.setStyleSheet(u"QLabel{\n"
"	\n"
"	font: 18pt \"Rubik Mono One\";\n"
"	color:rgb(39, 39, 39);\n"
"\n"
"}")
        self.addAppointmentHeader.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.addAppointmentHeader)

        self.frame = QFrame(self.frame_9)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.closePopUpBtn = QPushButton(self.frame)
        self.closePopUpBtn.setObjectName(u"closePopUpBtn")
        self.closePopUpBtn.setStyleSheet(u"#closePopUpBtn{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closePopUpBtn.setIcon(icon)
        self.closePopUpBtn.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.closePopUpBtn, 0, Qt.AlignLeft)


        self.horizontalLayout_6.addWidget(self.frame, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_2 = QFrame(self.addPopUPFrame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"#frame_2{\n"
"	background-color:none;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, -1, 6, -1)
        self.label_141 = QLabel(self.frame_7)
        self.label_141.setObjectName(u"label_141")
        self.label_141.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_4.addWidget(self.label_141)

        self.selectPatientPopUp = QComboBox(self.frame_7)
        self.selectPatientPopUp.addItem("")
        self.selectPatientPopUp.setObjectName(u"selectPatientPopUp")
        sizePolicy1.setHeightForWidth(self.selectPatientPopUp.sizePolicy().hasHeightForWidth())
        self.selectPatientPopUp.setSizePolicy(sizePolicy1)
        self.selectPatientPopUp.setMinimumSize(QSize(174, 45))
        self.selectPatientPopUp.setFocusPolicy(Qt.NoFocus)
        self.selectPatientPopUp.setStyleSheet(u"")
        self.selectPatientPopUp.setEditable(True)
        self.selectPatientPopUp.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.selectPatientPopUp.setDuplicatesEnabled(False)
        self.selectPatientPopUp.setFrame(True)

        self.verticalLayout_4.addWidget(self.selectPatientPopUp)


        self.horizontalLayout_2.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, 20, -1)
        self.label_142 = QLabel(self.frame_8)
        self.label_142.setObjectName(u"label_142")
        self.label_142.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_5.addWidget(self.label_142)

        self.selectPetPopUp = QComboBox(self.frame_8)
        self.selectPetPopUp.addItem("")
        self.selectPetPopUp.setObjectName(u"selectPetPopUp")
        sizePolicy1.setHeightForWidth(self.selectPetPopUp.sizePolicy().hasHeightForWidth())
        self.selectPetPopUp.setSizePolicy(sizePolicy1)
        self.selectPetPopUp.setMinimumSize(QSize(174, 45))
        self.selectPetPopUp.setFocusPolicy(Qt.NoFocus)
        self.selectPetPopUp.setStyleSheet(u"")
        self.selectPetPopUp.setEditable(True)
        self.selectPetPopUp.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.selectPetPopUp.setDuplicatesEnabled(False)
        self.selectPetPopUp.setFrame(True)

        self.verticalLayout_5.addWidget(self.selectPetPopUp)


        self.horizontalLayout_2.addWidget(self.frame_8)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_63 = QFrame(self.addPopUPFrame)
        self.frame_63.setObjectName(u"frame_63")
        sizePolicy1.setHeightForWidth(self.frame_63.sizePolicy().hasHeightForWidth())
        self.frame_63.setSizePolicy(sizePolicy1)
        self.frame_63.setStyleSheet(u"#frame_63{\n"
"	background-color:none;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"}")
        self.frame_63.setFrameShape(QFrame.StyledPanel)
        self.frame_63.setFrameShadow(QFrame.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.frame_63)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_54.setContentsMargins(20, -1, 20, 9)
        self.label_137 = QLabel(self.frame_63)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_54.addWidget(self.label_137)

        self.serviceTypeComboBox = QComboBox(self.frame_63)
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.setObjectName(u"serviceTypeComboBox")
        sizePolicy1.setHeightForWidth(self.serviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.serviceTypeComboBox.setSizePolicy(sizePolicy1)
        self.serviceTypeComboBox.setMinimumSize(QSize(174, 45))
        self.serviceTypeComboBox.setFocusPolicy(Qt.NoFocus)
        self.serviceTypeComboBox.setStyleSheet(u"")
        self.serviceTypeComboBox.setEditable(False)
        self.serviceTypeComboBox.setMaxVisibleItems(10)

        self.verticalLayout_54.addWidget(self.serviceTypeComboBox)


        self.verticalLayout_3.addWidget(self.frame_63)

        self.frame_3 = QFrame(self.addPopUPFrame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"#frame_3{\n"
"	background-color:none;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"#frame_5{\n"
"	background-color:none;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"}")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, -1, 6, -1)
        self.label_139 = QLabel(self.frame_5)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout.addWidget(self.label_139)

        self.popUpDateEdit = QDateEdit(self.frame_5)
        self.popUpDateEdit.setObjectName(u"popUpDateEdit")
        sizePolicy1.setHeightForWidth(self.popUpDateEdit.sizePolicy().hasHeightForWidth())
        self.popUpDateEdit.setSizePolicy(sizePolicy1)
        self.popUpDateEdit.setMinimumSize(QSize(174, 45))
        self.popUpDateEdit.setStyleSheet(u"")
        self.popUpDateEdit.setAccelerated(False)
        self.popUpDateEdit.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.popUpDateEdit)


        self.horizontalLayout_3.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"#frame_6{\n"
"	background-color:none;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"}")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_140 = QLabel(self.frame_6)
        self.label_140.setObjectName(u"label_140")
        self.label_140.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_2.addWidget(self.label_140)

        self.timeComboBox = QComboBox(self.frame_6)
        self.timeComboBox.addItem("")
        self.timeComboBox.setObjectName(u"timeComboBox")
        sizePolicy1.setHeightForWidth(self.timeComboBox.sizePolicy().hasHeightForWidth())
        self.timeComboBox.setSizePolicy(sizePolicy1)
        self.timeComboBox.setMinimumSize(QSize(174, 45))
        self.timeComboBox.setFocusPolicy(Qt.NoFocus)
        self.timeComboBox.setStyleSheet(u"")
        self.timeComboBox.setEditable(True)
        self.timeComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.timeComboBox.setDuplicatesEnabled(False)
        self.timeComboBox.setFrame(True)

        self.verticalLayout_2.addWidget(self.timeComboBox)


        self.horizontalLayout_3.addWidget(self.frame_6)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.addPopUPFrame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(20, -1, 20, -1)
        self.cancelAddAppointment = QPushButton(self.frame_4)
        self.cancelAddAppointment.setObjectName(u"cancelAddAppointment")
        sizePolicy1.setHeightForWidth(self.cancelAddAppointment.sizePolicy().hasHeightForWidth())
        self.cancelAddAppointment.setSizePolicy(sizePolicy1)
        self.cancelAddAppointment.setMinimumSize(QSize(174, 45))
        self.cancelAddAppointment.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancelAddAppointment.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:	rgb(220, 90, 90);\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"\n"
"}")

        self.horizontalLayout_4.addWidget(self.cancelAddAppointment)

        self.addAppointmentBtn = QPushButton(self.frame_4)
        self.addAppointmentBtn.setObjectName(u"addAppointmentBtn")
        sizePolicy1.setHeightForWidth(self.addAppointmentBtn.sizePolicy().hasHeightForWidth())
        self.addAppointmentBtn.setSizePolicy(sizePolicy1)
        self.addAppointmentBtn.setMinimumSize(QSize(174, 45))
        self.addAppointmentBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addAppointmentBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:#FCD597;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(230, 193, 137);\n"
"\n"
"}")

        self.horizontalLayout_4.addWidget(self.addAppointmentBtn)


        self.verticalLayout_3.addWidget(self.frame_4)


        self.horizontalLayout.addWidget(self.addPopUPFrame)


        self.retranslateUi(Form)

        self.serviceTypeComboBox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.addAppointmentHeader.setText(QCoreApplication.translate("Form", u"Set Appointment Details", None))
        self.closePopUpBtn.setText("")
        self.label_141.setText(QCoreApplication.translate("Form", u"Select Patient", None))
        self.selectPatientPopUp.setItemText(0, QCoreApplication.translate("Form", u"Select Patient", None))

        self.label_142.setText(QCoreApplication.translate("Form", u"Select Pet", None))
        self.selectPetPopUp.setItemText(0, QCoreApplication.translate("Form", u"Select Pet", None))

        self.label_137.setText(QCoreApplication.translate("Form", u"Service Type", None))
        self.serviceTypeComboBox.setItemText(0, QCoreApplication.translate("Form", u"Vaccination", None))
        self.serviceTypeComboBox.setItemText(1, QCoreApplication.translate("Form", u"Deworming", None))
        self.serviceTypeComboBox.setItemText(2, QCoreApplication.translate("Form", u"Tick & Flea Prevention", None))
        self.serviceTypeComboBox.setItemText(3, QCoreApplication.translate("Form", u"Consultation", None))
        self.serviceTypeComboBox.setItemText(4, QCoreApplication.translate("Form", u"Wellness Check", None))
        self.serviceTypeComboBox.setItemText(5, QCoreApplication.translate("Form", u"Surgery", None))
        self.serviceTypeComboBox.setItemText(6, QCoreApplication.translate("Form", u"Comprehensive Hematology", None))
        self.serviceTypeComboBox.setItemText(7, QCoreApplication.translate("Form", u"Blood Chemistry", None))
        self.serviceTypeComboBox.setItemText(8, QCoreApplication.translate("Form", u"Progesterone test", None))
        self.serviceTypeComboBox.setItemText(9, QCoreApplication.translate("Form", u"Pregnancy test", None))
        self.serviceTypeComboBox.setItemText(10, QCoreApplication.translate("Form", u"Diagnostic Microscopy", None))
        self.serviceTypeComboBox.setItemText(11, QCoreApplication.translate("Form", u"Urinalysis", None))
        self.serviceTypeComboBox.setItemText(12, QCoreApplication.translate("Form", u"Antigen/Antibody", None))

        self.serviceTypeComboBox.setCurrentText("")
        self.label_139.setText(QCoreApplication.translate("Form", u"Preffered Date", None))
        self.popUpDateEdit.setDisplayFormat(QCoreApplication.translate("Form", u"MMM d, yyyy", None))
        self.label_140.setText(QCoreApplication.translate("Form", u"Preffered Time", None))
        self.timeComboBox.setItemText(0, QCoreApplication.translate("Form", u"Select Time", None))

        self.cancelAddAppointment.setText(QCoreApplication.translate("Form", u"CANCEL", None))
        self.addAppointmentBtn.setText(QCoreApplication.translate("Form", u"ADD", None))
    # retranslateUi


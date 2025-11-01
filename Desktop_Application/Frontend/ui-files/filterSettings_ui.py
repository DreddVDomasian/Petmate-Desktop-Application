# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filterSettings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(734, 395)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"#frame{\n"
"		background-color: qlineargradient(\n"
"		 y1: 0, x1: 0, y2: 1, x2: 0,\n"
"		 stop: 0 #78B3CE, \n"
"    	 stop: 1 #D0F0FF\n"
"	);\n"
"	border-radius:10px;\n"
"}\n"
"QDateEdit {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 10px;\n"
"}\n"
"QDateEdit :disabled{\n"
"    background-color: #f0f0f0;\n"
"    color: #888;   \n"
"\n"
"}\n"
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
"    border-radius: 10px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"\n"
"QComboBox:disabled {\n"
"    border-radiu"
                        "s: 10px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"    color: #888;    \n"
"	padding-left: 10px;\n"
"    background-color: #f0f0f0;   \n"
"}\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    color: rgb(39, 39, 39);\n"
"    border: none; \n"
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
"QComboBox QAbstractItemV"
                        "iew::item {\n"
"    background-color:  rgb(232, 232, 232);\n"
"    color: black;\n"
"    height: 25px;\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: rgb(193, 193, 193);\n"
"    color: black;\n"
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
"QComboBox QAbstractI"
                        "temView QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"QComboBox QAbstractItemView QScrollBar,\n"
"QComboBox QAbstractItemView QScrollBar::handle,\n"
"QComboBox QAbstractItemView QScrollBar::groove {\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    color: rgb(39, 39, 39);\n"
"    border: none; /* optional para di mag mukhang double border */\n"
"    background: transparent;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.FilterHeader = QLabel(self.frame_2)
        self.FilterHeader.setObjectName(u"FilterHeader")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FilterHeader.sizePolicy().hasHeightForWidth())
        self.FilterHeader.setSizePolicy(sizePolicy)
        self.FilterHeader.setStyleSheet(u"QLabel{\n"
"	\n"
"	font: 18pt \"Rubik Mono One\";\n"
"	color:rgb(39, 39, 39);\n"
"\n"
"}")
        self.FilterHeader.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.FilterHeader)

        self.closePopUpBtn = QPushButton(self.frame_2)
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

        self.horizontalLayout_8.addWidget(self.closePopUpBtn)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Checker = QCheckBox(self.frame_4)
        self.Checker.setObjectName(u"Checker")
        self.Checker.setStyleSheet(u"\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: transparent;\n"
"    image: url(:/Icons/Icons/checkBox.png); \n"
"	border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    background-color: rgb(120, 179, 206);\n"
"}\n"
"")
        self.Checker.setIconSize(QSize(50, 50))
        self.Checker.setCheckable(True)
        self.Checker.setTristate(False)

        self.horizontalLayout_2.addWidget(self.Checker)

        self.serviceTypeComboBox = QComboBox(self.frame_4)
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
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.setObjectName(u"serviceTypeComboBox")
        self.serviceTypeComboBox.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.serviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.serviceTypeComboBox.setSizePolicy(sizePolicy1)
        self.serviceTypeComboBox.setMinimumSize(QSize(174, 45))
        self.serviceTypeComboBox.setMaximumSize(QSize(16777215, 65))
        self.serviceTypeComboBox.setFocusPolicy(Qt.NoFocus)
        self.serviceTypeComboBox.setStyleSheet(u"")
        self.serviceTypeComboBox.setEditable(False)
        self.serviceTypeComboBox.setMaxVisibleItems(10)

        self.horizontalLayout_2.addWidget(self.serviceTypeComboBox)


        self.horizontalLayout_9.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Checker_2 = QCheckBox(self.frame_5)
        self.Checker_2.setObjectName(u"Checker_2")
        self.Checker_2.setStyleSheet(u"\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: transparent;\n"
"    image: url(:/Icons/Icons/checkBox.png); \n"
"	border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    background-color: rgb(120, 179, 206);\n"
"}\n"
"")
        self.Checker_2.setIconSize(QSize(50, 50))
        self.Checker_2.setCheckable(True)
        self.Checker_2.setTristate(False)

        self.horizontalLayout_3.addWidget(self.Checker_2)

        self.speciesComboBox = QComboBox(self.frame_5)
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.setObjectName(u"speciesComboBox")
        self.speciesComboBox.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.speciesComboBox.sizePolicy().hasHeightForWidth())
        self.speciesComboBox.setSizePolicy(sizePolicy1)
        self.speciesComboBox.setMinimumSize(QSize(174, 45))
        self.speciesComboBox.setMaximumSize(QSize(16777215, 65))
        self.speciesComboBox.setStyleSheet(u"")
        self.speciesComboBox.setEditable(False)

        self.horizontalLayout_3.addWidget(self.speciesComboBox)


        self.horizontalLayout_9.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_9 = QFrame(self.frame)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"font: 63 14pt \"Montserrat SemiBold\";")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.frame_9)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)


        self.verticalLayout.addWidget(self.frame_9)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Checker_3 = QCheckBox(self.frame_7)
        self.Checker_3.setObjectName(u"Checker_3")
        self.Checker_3.setStyleSheet(u"\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: transparent;\n"
"    image: url(:/Icons/Icons/checkBox.png); \n"
"	border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    background-color: rgb(120, 179, 206);\n"
"}\n"
"")
        self.Checker_3.setIconSize(QSize(50, 50))
        self.Checker_3.setCheckable(True)
        self.Checker_3.setTristate(False)

        self.horizontalLayout_4.addWidget(self.Checker_3)

        self.dateEdit = QDateEdit(self.frame_7)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy1)
        self.dateEdit.setMinimumSize(QSize(174, 45))
        self.dateEdit.setMaximumSize(QSize(16777215, 65))
        self.dateEdit.setStyleSheet(u"")
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setAccelerated(False)
        self.dateEdit.setCalendarPopup(True)

        self.horizontalLayout_4.addWidget(self.dateEdit)


        self.horizontalLayout_10.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.Checker_4 = QCheckBox(self.frame_8)
        self.Checker_4.setObjectName(u"Checker_4")
        self.Checker_4.setStyleSheet(u"\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: transparent;\n"
"    image: url(:/Icons/Icons/checkBox.png); \n"
"	border: 2px solid rgb(255, 255, 255);\n"
"	border-radius:5px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    background-color: rgb(120, 179, 206);\n"
"}\n"
"")
        self.Checker_4.setIconSize(QSize(50, 50))
        self.Checker_4.setCheckable(True)
        self.Checker_4.setTristate(False)

        self.horizontalLayout_5.addWidget(self.Checker_4)

        self.dateEdit_2 = QDateEdit(self.frame_8)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.dateEdit_2.sizePolicy().hasHeightForWidth())
        self.dateEdit_2.setSizePolicy(sizePolicy1)
        self.dateEdit_2.setMinimumSize(QSize(174, 45))
        self.dateEdit_2.setMaximumSize(QSize(16777215, 65))
        self.dateEdit_2.setStyleSheet(u"")
        self.dateEdit_2.setReadOnly(True)
        self.dateEdit_2.setAccelerated(False)
        self.dateEdit_2.setCalendarPopup(True)

        self.horizontalLayout_5.addWidget(self.dateEdit_2)


        self.horizontalLayout_10.addWidget(self.frame_8)


        self.verticalLayout.addWidget(self.frame_6)

        self.frame_10 = QFrame(self.frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.addAppointmentBtn = QPushButton(self.frame_10)
        self.addAppointmentBtn.setObjectName(u"addAppointmentBtn")
        sizePolicy.setHeightForWidth(self.addAppointmentBtn.sizePolicy().hasHeightForWidth())
        self.addAppointmentBtn.setSizePolicy(sizePolicy)
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

        self.horizontalLayout_6.addWidget(self.addAppointmentBtn)


        self.verticalLayout.addWidget(self.frame_10)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)
        self.Checker.clicked["bool"].connect(self.serviceTypeComboBox.setEnabled)
        self.Checker_2.clicked["bool"].connect(self.speciesComboBox.setEnabled)
        self.Checker_3.clicked["bool"].connect(self.dateEdit.setEnabled)
        self.Checker_4.clicked["bool"].connect(self.dateEdit_2.setEnabled)

        self.serviceTypeComboBox.setCurrentIndex(0)
        self.speciesComboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.FilterHeader.setText(QCoreApplication.translate("Form", u"Filters", None))
        self.closePopUpBtn.setText("")
        self.Checker.setText("")
        self.serviceTypeComboBox.setItemText(0, QCoreApplication.translate("Form", u"Select Service", None))
        self.serviceTypeComboBox.setItemText(1, QCoreApplication.translate("Form", u"Vaccination", None))
        self.serviceTypeComboBox.setItemText(2, QCoreApplication.translate("Form", u"Deworming", None))
        self.serviceTypeComboBox.setItemText(3, QCoreApplication.translate("Form", u"Tick & Flea Prevention", None))
        self.serviceTypeComboBox.setItemText(4, QCoreApplication.translate("Form", u"Consultation", None))
        self.serviceTypeComboBox.setItemText(5, QCoreApplication.translate("Form", u"Wellness Check", None))
        self.serviceTypeComboBox.setItemText(6, QCoreApplication.translate("Form", u"Surgery", None))
        self.serviceTypeComboBox.setItemText(7, QCoreApplication.translate("Form", u"CBC", None))
        self.serviceTypeComboBox.setItemText(8, QCoreApplication.translate("Form", u"Blood Chemistry", None))
        self.serviceTypeComboBox.setItemText(9, QCoreApplication.translate("Form", u"Progesterone test", None))
        self.serviceTypeComboBox.setItemText(10, QCoreApplication.translate("Form", u"Pregnancy test", None))
        self.serviceTypeComboBox.setItemText(11, QCoreApplication.translate("Form", u"Diagnostic Microscopy", None))
        self.serviceTypeComboBox.setItemText(12, QCoreApplication.translate("Form", u"Urinalysis", None))
        self.serviceTypeComboBox.setItemText(13, QCoreApplication.translate("Form", u"Antigen/Antibody", None))

        self.serviceTypeComboBox.setCurrentText(QCoreApplication.translate("Form", u"Select Service", None))
        self.Checker_2.setText("")
        self.speciesComboBox.setItemText(0, QCoreApplication.translate("Form", u"Select Species", None))
        self.speciesComboBox.setItemText(1, QCoreApplication.translate("Form", u"Cat", None))
        self.speciesComboBox.setItemText(2, QCoreApplication.translate("Form", u"Dog", None))
        self.speciesComboBox.setItemText(3, QCoreApplication.translate("Form", u"Others", None))

        self.speciesComboBox.setCurrentText(QCoreApplication.translate("Form", u"Select Species", None))
        self.label.setText(QCoreApplication.translate("Form", u"DATE RANGE", None))
        self.Checker_3.setText("")
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("Form", u"MMM d, yyyy", None))
        self.Checker_4.setText("")
        self.dateEdit_2.setDisplayFormat(QCoreApplication.translate("Form", u"MMM d, yyyy", None))
        self.addAppointmentBtn.setText(QCoreApplication.translate("Form", u"APPLY", None))
    # retranslateUi


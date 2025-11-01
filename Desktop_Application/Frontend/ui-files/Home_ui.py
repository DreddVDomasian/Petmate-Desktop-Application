# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home.ui'
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
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1280, 720))
        icon = QIcon()
        icon.addFile(u":/images/image/desktopIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"	border:none;\n"
"}\n"
"QToolButton{\n"
"border:none\n"
"\n"
"}")
        MainWindow.setIconSize(QSize(31, 24))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#centralwidget{\n"
"	background-color: qlineargradient(\n"
"		 y1: 0, x1: 0, y2: 1, x2: 0,\n"
"		 stop: 0 #78B3CE, \n"
"    	 stop: 1 #D5EDF8\n"
"	);\n"
"}\n"
"")
        self.verticalLayout_70 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_70.setSpacing(0)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.verticalLayout_70.setContentsMargins(15, 15, 0, 15)
        self.underFrame = QFrame(self.centralwidget)
        self.underFrame.setObjectName(u"underFrame")
        self.underFrame.setStyleSheet(u"#underFrame{\n"
"	background-color:transparent;\n"
"	border-radius:15px;\n"
"}\n"
"")
        self.underFrame.setFrameShape(QFrame.StyledPanel)
        self.underFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_71 = QHBoxLayout(self.underFrame)
        self.horizontalLayout_71.setSpacing(15)
        self.horizontalLayout_71.setObjectName(u"horizontalLayout_71")
        self.horizontalLayout_71.setContentsMargins(0, 0, 15, 2)
        self.sideNav = QFrame(self.underFrame)
        self.sideNav.setObjectName(u"sideNav")
        self.sideNav.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sideNav.sizePolicy().hasHeightForWidth())
        self.sideNav.setSizePolicy(sizePolicy1)
        self.sideNav.setStyleSheet(u"#sideNav{\n"
"	background-color:rgb(255, 255, 255);\n"
"	border:none;\n"
"    border-radius: 15px;\n"
"\n"
"}")
        self.sideNav.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.sideNav)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 29)
        self.frame_50 = QFrame(self.sideNav)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.StyledPanel)
        self.frame_50.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_76 = QHBoxLayout(self.frame_50)
        self.horizontalLayout_76.setSpacing(0)
        self.horizontalLayout_76.setObjectName(u"horizontalLayout_76")
        self.horizontalLayout_76.setContentsMargins(0, 0, 0, 0)
        self.fullNavBtn = QPushButton(self.frame_50)
        self.fullNavBtn.setObjectName(u"fullNavBtn")
        self.fullNavBtn.setStyleSheet(u"border:none;")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/hideNav.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fullNavBtn.setIcon(icon1)
        self.fullNavBtn.setIconSize(QSize(25, 25))
        self.fullNavBtn.setCheckable(True)
        self.fullNavBtn.setChecked(False)
        self.fullNavBtn.setAutoRepeat(False)

        self.horizontalLayout_76.addWidget(self.fullNavBtn)


        self.verticalLayout_2.addWidget(self.frame_50, 0, Qt.AlignRight)

        self.PetmateLogo = QLabel(self.sideNav)
        self.PetmateLogo.setObjectName(u"PetmateLogo")
        sizePolicy.setHeightForWidth(self.PetmateLogo.sizePolicy().hasHeightForWidth())
        self.PetmateLogo.setSizePolicy(sizePolicy)
        self.PetmateLogo.setMaximumSize(QSize(212, 81))
        self.PetmateLogo.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.PetmateLogo.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.PetmateLogo, 0, Qt.AlignHCenter)

        self.Buttons = QFrame(self.sideNav)
        self.Buttons.setObjectName(u"Buttons")
        sizePolicy.setHeightForWidth(self.Buttons.sizePolicy().hasHeightForWidth())
        self.Buttons.setSizePolicy(sizePolicy)
        self.Buttons.setStyleSheet(u"QToolButton{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	font-family:\"Montserrat Black\";\n"
"	font-weight:87;\n"
"	color:#78B3CE;\n"
"	border-radius:15px;\n"
"	padding:10;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color: rgb(255, 241, 206);\n"
"\n"
"}\n"
"\n"
"QToolButton:checked{\n"
"    background-color:rgb(252, 213, 151);   /* Active bg color */\n"
"	border-radius:15px;\n"
"    color: #78B3CE;    \n"
"}")
        self.Buttons.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.Buttons)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.homeBtn = QToolButton(self.Buttons)
        self.homeBtn.setObjectName(u"homeBtn")
        sizePolicy.setHeightForWidth(self.homeBtn.sizePolicy().hasHeightForWidth())
        self.homeBtn.setSizePolicy(sizePolicy)
        self.homeBtn.setMaximumSize(QSize(16777215, 70))
        self.homeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.homeBtn.setAutoFillBackground(False)
        self.homeBtn.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/Icons/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.homeBtn.setIcon(icon2)
        self.homeBtn.setIconSize(QSize(40, 40))
        self.homeBtn.setPopupMode(QToolButton.DelayedPopup)
        self.homeBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.homeBtn.setAutoRaise(False)
        self.homeBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.homeBtn)

        self.addPatientBtn = QToolButton(self.Buttons)
        self.addPatientBtn.setObjectName(u"addPatientBtn")
        sizePolicy.setHeightForWidth(self.addPatientBtn.sizePolicy().hasHeightForWidth())
        self.addPatientBtn.setSizePolicy(sizePolicy)
        self.addPatientBtn.setMaximumSize(QSize(16777215, 70))
        self.addPatientBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addPatientBtn.setAutoFillBackground(False)
        self.addPatientBtn.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/Icons/Icons/addPatient.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addPatientBtn.setIcon(icon3)
        self.addPatientBtn.setIconSize(QSize(40, 40))
        self.addPatientBtn.setPopupMode(QToolButton.DelayedPopup)
        self.addPatientBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addPatientBtn.setAutoRaise(False)
        self.addPatientBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.addPatientBtn)

        self.petRecordsBtn = QToolButton(self.Buttons)
        self.petRecordsBtn.setObjectName(u"petRecordsBtn")
        sizePolicy.setHeightForWidth(self.petRecordsBtn.sizePolicy().hasHeightForWidth())
        self.petRecordsBtn.setSizePolicy(sizePolicy)
        self.petRecordsBtn.setMaximumSize(QSize(16777215, 70))
        self.petRecordsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.petRecordsBtn.setAutoFillBackground(False)
        self.petRecordsBtn.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u":/Icons/Icons/Records.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.petRecordsBtn.setIcon(icon4)
        self.petRecordsBtn.setIconSize(QSize(40, 40))
        self.petRecordsBtn.setPopupMode(QToolButton.DelayedPopup)
        self.petRecordsBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.petRecordsBtn.setAutoRaise(False)
        self.petRecordsBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.petRecordsBtn)

        self.appointmentBtn = QToolButton(self.Buttons)
        self.appointmentBtn.setObjectName(u"appointmentBtn")
        sizePolicy.setHeightForWidth(self.appointmentBtn.sizePolicy().hasHeightForWidth())
        self.appointmentBtn.setSizePolicy(sizePolicy)
        self.appointmentBtn.setMaximumSize(QSize(16777215, 70))
        self.appointmentBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.appointmentBtn.setAutoFillBackground(False)
        self.appointmentBtn.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u":/Icons/Icons/AddAppointment.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.appointmentBtn.setIcon(icon5)
        self.appointmentBtn.setIconSize(QSize(40, 40))
        self.appointmentBtn.setPopupMode(QToolButton.DelayedPopup)
        self.appointmentBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.appointmentBtn.setAutoRaise(False)
        self.appointmentBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.appointmentBtn)

        self.schedVaxBtn = QToolButton(self.Buttons)
        self.schedVaxBtn.setObjectName(u"schedVaxBtn")
        sizePolicy.setHeightForWidth(self.schedVaxBtn.sizePolicy().hasHeightForWidth())
        self.schedVaxBtn.setSizePolicy(sizePolicy)
        self.schedVaxBtn.setMaximumSize(QSize(16777215, 70))
        self.schedVaxBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.schedVaxBtn.setAutoFillBackground(False)
        self.schedVaxBtn.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u":/Icons/Icons/schedVax.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.schedVaxBtn.setIcon(icon6)
        self.schedVaxBtn.setIconSize(QSize(40, 40))
        self.schedVaxBtn.setPopupMode(QToolButton.DelayedPopup)
        self.schedVaxBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.schedVaxBtn.setAutoRaise(False)
        self.schedVaxBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.schedVaxBtn)

        self.settingsBtn = QToolButton(self.Buttons)
        self.settingsBtn.setObjectName(u"settingsBtn")
        sizePolicy.setHeightForWidth(self.settingsBtn.sizePolicy().hasHeightForWidth())
        self.settingsBtn.setSizePolicy(sizePolicy)
        self.settingsBtn.setMaximumSize(QSize(16777215, 70))
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settingsBtn.setAutoFillBackground(False)
        self.settingsBtn.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u":/Icons/Icons/settings-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsBtn.setIcon(icon7)
        self.settingsBtn.setIconSize(QSize(40, 40))
        self.settingsBtn.setPopupMode(QToolButton.DelayedPopup)
        self.settingsBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.settingsBtn.setAutoRaise(False)
        self.settingsBtn.setArrowType(Qt.NoArrow)

        self.verticalLayout.addWidget(self.settingsBtn)


        self.verticalLayout_2.addWidget(self.Buttons, 0, Qt.AlignHCenter)

        self.verticalSpacer_15 = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_15)

        self.frame_74 = QFrame(self.sideNav)
        self.frame_74.setObjectName(u"frame_74")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_74.sizePolicy().hasHeightForWidth())
        self.frame_74.setSizePolicy(sizePolicy2)
        self.frame_74.setFrameShape(QFrame.StyledPanel)
        self.frame_74.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_84 = QHBoxLayout(self.frame_74)
        self.horizontalLayout_84.setSpacing(0)
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.horizontalLayout_84.setContentsMargins(0, 0, 0, 0)
        self.logoutBtn = QToolButton(self.frame_74)
        self.logoutBtn.setObjectName(u"logoutBtn")
        sizePolicy.setHeightForWidth(self.logoutBtn.sizePolicy().hasHeightForWidth())
        self.logoutBtn.setSizePolicy(sizePolicy)
        self.logoutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.logoutBtn.setStyleSheet(u"QToolButton{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	font: 87 12pt \"Montserrat Black\";\n"
"	font-weight:bold;\n"
"	color:#78B3CE;\n"
"	border-radius:15px;\n"
"	padding:10;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color: rgb(255, 241, 206);\n"
"\n"
"}")
        self.logoutBtn.setText(u"    LOG OUT")
        icon8 = QIcon()
        icon8.addFile(u":/Icons/Icons/logOutIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logoutBtn.setIcon(icon8)
        self.logoutBtn.setIconSize(QSize(30, 30))
        self.logoutBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_84.addWidget(self.logoutBtn)


        self.verticalLayout_2.addWidget(self.frame_74, 0, Qt.AlignHCenter)


        self.horizontalLayout_71.addWidget(self.sideNav)

        self.MiniNav = QFrame(self.underFrame)
        self.MiniNav.setObjectName(u"MiniNav")
        self.MiniNav.setEnabled(True)
        sizePolicy.setHeightForWidth(self.MiniNav.sizePolicy().hasHeightForWidth())
        self.MiniNav.setSizePolicy(sizePolicy)
        self.MiniNav.setMaximumSize(QSize(100, 16777215))
        self.MiniNav.setStyleSheet(u"#MiniNav{\n"
"	background-color:rgb(255, 255, 255);\n"
"	border:none;\n"
"	border-radius: 15px;\n"
"}")
        self.MiniNav.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_48 = QVBoxLayout(self.MiniNav)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_48.setContentsMargins(5, 10, 5, 29)
        self.frame_51 = QFrame(self.MiniNav)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setFrameShape(QFrame.StyledPanel)
        self.frame_51.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_77 = QHBoxLayout(self.frame_51)
        self.horizontalLayout_77.setSpacing(0)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.horizontalLayout_77.setContentsMargins(0, 5, 0, 20)
        self.miniNavBtn = QPushButton(self.frame_51)
        self.miniNavBtn.setObjectName(u"miniNavBtn")
        self.miniNavBtn.setStyleSheet(u"border:none;")
        icon9 = QIcon()
        icon9.addFile(u":/Icons/Icons/showNav.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.miniNavBtn.setIcon(icon9)
        self.miniNavBtn.setIconSize(QSize(25, 25))
        self.miniNavBtn.setCheckable(True)
        self.miniNavBtn.setAutoRepeat(False)

        self.horizontalLayout_77.addWidget(self.miniNavBtn, 0, Qt.AlignRight)


        self.verticalLayout_48.addWidget(self.frame_51)

        self.PetmateLogo_2 = QLabel(self.MiniNav)
        self.PetmateLogo_2.setObjectName(u"PetmateLogo_2")
        sizePolicy.setHeightForWidth(self.PetmateLogo_2.sizePolicy().hasHeightForWidth())
        self.PetmateLogo_2.setSizePolicy(sizePolicy)
        self.PetmateLogo_2.setMaximumSize(QSize(30, 50))
        self.PetmateLogo_2.setPixmap(QPixmap(u":/images/image/Dog.png"))
        self.PetmateLogo_2.setScaledContents(True)

        self.verticalLayout_48.addWidget(self.PetmateLogo_2, 0, Qt.AlignHCenter)

        self.verticalSpacer_17 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_48.addItem(self.verticalSpacer_17)

        self.Buttons_2 = QFrame(self.MiniNav)
        self.Buttons_2.setObjectName(u"Buttons_2")
        sizePolicy.setHeightForWidth(self.Buttons_2.sizePolicy().hasHeightForWidth())
        self.Buttons_2.setSizePolicy(sizePolicy)
        self.Buttons_2.setStyleSheet(u"QToolButton{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	font-family:\"Montserrat Black\";\n"
"	font-weight:87;\n"
"	color:#78B3CE;\n"
"	border-radius:15px;\n"
"	padding:5;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color: rgb(255, 241, 206);\n"
"\n"
"}\n"
"\n"
"QToolButton:checked{\n"
"    background-color:rgb(252, 213, 151);   /* Active bg color */\n"
"	border-radius:15px;\n"
"    color: #78B3CE;    \n"
"}\n"
"")
        self.Buttons_2.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_68 = QVBoxLayout(self.Buttons_2)
        self.verticalLayout_68.setSpacing(5)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.verticalLayout_68.setContentsMargins(5, 5, 5, 5)
        self.homeBtn_2 = QToolButton(self.Buttons_2)
        self.homeBtn_2.setObjectName(u"homeBtn_2")
        sizePolicy.setHeightForWidth(self.homeBtn_2.sizePolicy().hasHeightForWidth())
        self.homeBtn_2.setSizePolicy(sizePolicy)
        self.homeBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.homeBtn_2.setAutoFillBackground(False)
        self.homeBtn_2.setStyleSheet(u"")
        self.homeBtn_2.setIcon(icon2)
        self.homeBtn_2.setIconSize(QSize(40, 40))
        self.homeBtn_2.setCheckable(True)
        self.homeBtn_2.setChecked(False)
        self.homeBtn_2.setAutoRepeat(True)
        self.homeBtn_2.setPopupMode(QToolButton.DelayedPopup)
        self.homeBtn_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.homeBtn_2.setAutoRaise(False)
        self.homeBtn_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.homeBtn_2)

        self.addPatientBtn_2 = QToolButton(self.Buttons_2)
        self.addPatientBtn_2.setObjectName(u"addPatientBtn_2")
        sizePolicy.setHeightForWidth(self.addPatientBtn_2.sizePolicy().hasHeightForWidth())
        self.addPatientBtn_2.setSizePolicy(sizePolicy)
        self.addPatientBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addPatientBtn_2.setAutoFillBackground(False)
        self.addPatientBtn_2.setStyleSheet(u"")
        self.addPatientBtn_2.setIcon(icon3)
        self.addPatientBtn_2.setIconSize(QSize(40, 40))
        self.addPatientBtn_2.setCheckable(True)
        self.addPatientBtn_2.setAutoRepeat(True)
        self.addPatientBtn_2.setPopupMode(QToolButton.DelayedPopup)
        self.addPatientBtn_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addPatientBtn_2.setAutoRaise(False)
        self.addPatientBtn_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.addPatientBtn_2)

        self.petRecordsBtn_2 = QToolButton(self.Buttons_2)
        self.petRecordsBtn_2.setObjectName(u"petRecordsBtn_2")
        sizePolicy.setHeightForWidth(self.petRecordsBtn_2.sizePolicy().hasHeightForWidth())
        self.petRecordsBtn_2.setSizePolicy(sizePolicy)
        self.petRecordsBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.petRecordsBtn_2.setAutoFillBackground(False)
        self.petRecordsBtn_2.setStyleSheet(u"")
        self.petRecordsBtn_2.setIcon(icon4)
        self.petRecordsBtn_2.setIconSize(QSize(40, 40))
        self.petRecordsBtn_2.setCheckable(True)
        self.petRecordsBtn_2.setAutoRepeat(True)
        self.petRecordsBtn_2.setPopupMode(QToolButton.DelayedPopup)
        self.petRecordsBtn_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.petRecordsBtn_2.setAutoRaise(False)
        self.petRecordsBtn_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.petRecordsBtn_2)

        self.appointmentBtn_2 = QToolButton(self.Buttons_2)
        self.appointmentBtn_2.setObjectName(u"appointmentBtn_2")
        sizePolicy.setHeightForWidth(self.appointmentBtn_2.sizePolicy().hasHeightForWidth())
        self.appointmentBtn_2.setSizePolicy(sizePolicy)
        self.appointmentBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.appointmentBtn_2.setAutoFillBackground(False)
        self.appointmentBtn_2.setStyleSheet(u"")
        self.appointmentBtn_2.setIcon(icon5)
        self.appointmentBtn_2.setIconSize(QSize(40, 40))
        self.appointmentBtn_2.setCheckable(True)
        self.appointmentBtn_2.setAutoRepeat(True)
        self.appointmentBtn_2.setPopupMode(QToolButton.DelayedPopup)
        self.appointmentBtn_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.appointmentBtn_2.setAutoRaise(False)
        self.appointmentBtn_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.appointmentBtn_2)

        self.schedVaxBtn_2 = QToolButton(self.Buttons_2)
        self.schedVaxBtn_2.setObjectName(u"schedVaxBtn_2")
        sizePolicy.setHeightForWidth(self.schedVaxBtn_2.sizePolicy().hasHeightForWidth())
        self.schedVaxBtn_2.setSizePolicy(sizePolicy)
        self.schedVaxBtn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.schedVaxBtn_2.setAutoFillBackground(False)
        self.schedVaxBtn_2.setStyleSheet(u"")
        self.schedVaxBtn_2.setIcon(icon6)
        self.schedVaxBtn_2.setIconSize(QSize(40, 40))
        self.schedVaxBtn_2.setCheckable(True)
        self.schedVaxBtn_2.setAutoRepeat(True)
        self.schedVaxBtn_2.setPopupMode(QToolButton.DelayedPopup)
        self.schedVaxBtn_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.schedVaxBtn_2.setAutoRaise(False)
        self.schedVaxBtn_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.schedVaxBtn_2)

        self.settings_2 = QToolButton(self.Buttons_2)
        self.settings_2.setObjectName(u"settings_2")
        sizePolicy.setHeightForWidth(self.settings_2.sizePolicy().hasHeightForWidth())
        self.settings_2.setSizePolicy(sizePolicy)
        self.settings_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_2.setAutoFillBackground(False)
        self.settings_2.setStyleSheet(u"")
        self.settings_2.setIcon(icon7)
        self.settings_2.setIconSize(QSize(40, 40))
        self.settings_2.setCheckable(True)
        self.settings_2.setAutoRepeat(True)
        self.settings_2.setPopupMode(QToolButton.DelayedPopup)
        self.settings_2.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.settings_2.setAutoRaise(False)
        self.settings_2.setArrowType(Qt.NoArrow)

        self.verticalLayout_68.addWidget(self.settings_2)


        self.verticalLayout_48.addWidget(self.Buttons_2)

        self.verticalSpacer_16 = QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_48.addItem(self.verticalSpacer_16)

        self.toolButton_4 = QToolButton(self.MiniNav)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toolButton_4.setStyleSheet(u"QToolButton{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	font: 87 12pt \"Montserrat Black\";\n"
"	font-weight:bold;\n"
"	color:#78B3CE;\n"
"	border-radius:15px;\n"
"	padding:10;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color: rgb(255, 241, 206);\n"
"\n"
"}")
        self.toolButton_4.setText(u"")
        self.toolButton_4.setIcon(icon8)
        self.toolButton_4.setIconSize(QSize(30, 30))
        self.toolButton_4.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_48.addWidget(self.toolButton_4, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_71.addWidget(self.MiniNav)

        self.MainContent = QFrame(self.underFrame)
        self.MainContent.setObjectName(u"MainContent")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.MainContent.sizePolicy().hasHeightForWidth())
        self.MainContent.setSizePolicy(sizePolicy3)
        self.MainContent.setStyleSheet(u"#MainContent{\n"
"	background-color:white;\n"
"    border-radius: 15px;\n"
"\n"
"}")
        self.MainContent.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_3 = QVBoxLayout(self.MainContent)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.MainContent)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setLayoutDirection(Qt.LeftToRight)
        self.stackedWidget.setStyleSheet(u"QStackedWidget{\n"
"	background:transparent;\n"
"\n"
"}")
        self.stackedWidget.setFrameShape(QFrame.NoFrame)
        self.homepage = QWidget()
        self.homepage.setObjectName(u"homepage")
        self.homepage.setStyleSheet(u"QWidget{\n"
"	background:transparent;\n"
"\n"
"}")
        self.verticalLayout_7 = QVBoxLayout(self.homepage)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.home = QFrame(self.homepage)
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"QFrame{\n"
"	background:transparent;\n"
"\n"
"}")
        self.home.setFrameShape(QFrame.StyledPanel)
        self.home.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.home)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(10, 0, 0, 0)
        self.homeBackBtn = QPushButton(self.home)
        self.homeBackBtn.setObjectName(u"homeBackBtn")
        self.homeBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        icon10 = QIcon()
        icon10.addFile(u":/Icons/Icons/left-arrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.homeBackBtn.setIcon(icon10)

        self.verticalLayout_8.addWidget(self.homeBackBtn, 0, Qt.AlignLeft)

        self.frame = QFrame(self.home)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(816, 250))
        self.frame.setMaximumSize(QSize(16777215, 300))
        self.frame.setStyleSheet(u"QFrame{\n"
"	background:transparent;\n"
"\n"
"}")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_7 = QHBoxLayout(self.frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(15, -1, 15, -1)
        self.frame_22 = QFrame(self.frame)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_22)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.horizontalLayout_7.addWidget(self.frame_22)

        self.frame_48 = QFrame(self.frame)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setMinimumSize(QSize(0, 0))
        self.frame_48.setFrameShape(QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_79 = QHBoxLayout(self.frame_48)
        self.horizontalLayout_79.setObjectName(u"horizontalLayout_79")
        self.horizontalLayout_79.setContentsMargins(15, -1, -1, 15)

        self.horizontalLayout_7.addWidget(self.frame_48)


        self.verticalLayout_8.addWidget(self.frame)

        self.Appointment = QFrame(self.home)
        self.Appointment.setObjectName(u"Appointment")
        sizePolicy3.setHeightForWidth(self.Appointment.sizePolicy().hasHeightForWidth())
        self.Appointment.setSizePolicy(sizePolicy3)
        self.Appointment.setMinimumSize(QSize(0, 0))
        self.Appointment.setStyleSheet(u"QFrame{\n"
"	background:transparent;\n"
"\n"
"}")
        self.Appointment.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_78 = QHBoxLayout(self.Appointment)
        self.horizontalLayout_78.setSpacing(7)
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.horizontalLayout_78.setContentsMargins(15, -1, 15, -1)
        self.frame_53 = QFrame(self.Appointment)
        self.frame_53.setObjectName(u"frame_53")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_53.sizePolicy().hasHeightForWidth())
        self.frame_53.setSizePolicy(sizePolicy4)
        self.frame_53.setFrameShape(QFrame.StyledPanel)
        self.frame_53.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_78.addWidget(self.frame_53)

        self.frame_54 = QFrame(self.Appointment)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setFrameShape(QFrame.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_54)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.horizontalLayout_78.addWidget(self.frame_54)


        self.verticalLayout_8.addWidget(self.Appointment)


        self.verticalLayout_7.addWidget(self.home)

        self.stackedWidget.addWidget(self.homepage)
        self.AddpatientPage = QWidget()
        self.AddpatientPage.setObjectName(u"AddpatientPage")
        self.AddpatientPage.setStyleSheet(u"QWidget{\n"
"	background:transparent;\n"
"\n"
"}")
        self.verticalLayout_12 = QVBoxLayout(self.AddpatientPage)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.addPatientBackBtn = QPushButton(self.AddpatientPage)
        self.addPatientBackBtn.setObjectName(u"addPatientBackBtn")
        self.addPatientBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.addPatientBackBtn.setIcon(icon10)

        self.verticalLayout_12.addWidget(self.addPatientBackBtn, 0, Qt.AlignLeft)

        self.frame_2 = QFrame(self.AddpatientPage)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pageHeader1 = QLabel(self.frame_2)
        self.pageHeader1.setObjectName(u"pageHeader1")
        sizePolicy3.setHeightForWidth(self.pageHeader1.sizePolicy().hasHeightForWidth())
        self.pageHeader1.setSizePolicy(sizePolicy3)
        self.pageHeader1.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pageHeader1)

        self.clinicIconP1 = QLabel(self.frame_2)
        self.clinicIconP1.setObjectName(u"clinicIconP1")
        sizePolicy.setHeightForWidth(self.clinicIconP1.sizePolicy().hasHeightForWidth())
        self.clinicIconP1.setSizePolicy(sizePolicy)
        self.clinicIconP1.setMaximumSize(QSize(145, 60))
        self.clinicIconP1.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP1.setScaledContents(True)
        self.clinicIconP1.setAlignment(Qt.AlignCenter)
        self.clinicIconP1.setWordWrap(False)

        self.horizontalLayout.addWidget(self.clinicIconP1)


        self.verticalLayout_12.addWidget(self.frame_2, 0, Qt.AlignTop)

        self.verticalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_12.addItem(self.verticalSpacer_11)

        self.ownerDetailsFrame = QFrame(self.AddpatientPage)
        self.ownerDetailsFrame.setObjectName(u"ownerDetailsFrame")
        sizePolicy.setHeightForWidth(self.ownerDetailsFrame.sizePolicy().hasHeightForWidth())
        self.ownerDetailsFrame.setSizePolicy(sizePolicy)
        self.ownerDetailsFrame.setMinimumSize(QSize(0, 0))
        self.ownerDetailsFrame.setStyleSheet(u"QLabel{\n"
"	font-family: \"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QComboBox QLineEdit {\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
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
"QComboBox::down-arrow {"
                        "\n"
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
"QComboBox QAbstractItemView"
                        " QScrollBar::handle:vertical {\n"
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
"QComboBox QAbstractItemView QScrollBar::groove {\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    color: rgb(39, 39, 39);\n"
"    border: none; /* optional para di mag mukhang double border */\n"
"    background: tran"
                        "sparent;\n"
"}")
        self.ownerDetailsFrame.setFrameShape(QFrame.StyledPanel)
        self.ownerDetailsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.ownerDetailsFrame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(50, -1, 50, 0)
        self.verticalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_9)

        self.label_4 = QLabel(self.ownerDetailsFrame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setStyleSheet(u"")

        self.verticalLayout_9.addWidget(self.label_4)

        self.frame_36 = QFrame(self.ownerDetailsFrame)
        self.frame_36.setObjectName(u"frame_36")
        sizePolicy.setHeightForWidth(self.frame_36.sizePolicy().hasHeightForWidth())
        self.frame_36.setSizePolicy(sizePolicy)
        self.frame_36.setMinimumSize(QSize(0, 50))
        self.frame_36.setMaximumSize(QSize(16777215, 80))
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_52 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(0, 0, 9, 5)
        self.firstNameEdit = QLineEdit(self.frame_36)
        self.firstNameEdit.setObjectName(u"firstNameEdit")
        sizePolicy.setHeightForWidth(self.firstNameEdit.sizePolicy().hasHeightForWidth())
        self.firstNameEdit.setSizePolicy(sizePolicy)
        self.firstNameEdit.setStyleSheet(u"")

        self.horizontalLayout_52.addWidget(self.firstNameEdit)

        self.lastNameEdit = QLineEdit(self.frame_36)
        self.lastNameEdit.setObjectName(u"lastNameEdit")
        sizePolicy.setHeightForWidth(self.lastNameEdit.sizePolicy().hasHeightForWidth())
        self.lastNameEdit.setSizePolicy(sizePolicy)
        self.lastNameEdit.setStyleSheet(u"")

        self.horizontalLayout_52.addWidget(self.lastNameEdit)

        self.middleNameEdit = QLineEdit(self.frame_36)
        self.middleNameEdit.setObjectName(u"middleNameEdit")
        sizePolicy.setHeightForWidth(self.middleNameEdit.sizePolicy().hasHeightForWidth())
        self.middleNameEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_52.addWidget(self.middleNameEdit)


        self.verticalLayout_9.addWidget(self.frame_36)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_10)

        self.ownerDetails = QFrame(self.ownerDetailsFrame)
        self.ownerDetails.setObjectName(u"ownerDetails")
        sizePolicy.setHeightForWidth(self.ownerDetails.sizePolicy().hasHeightForWidth())
        self.ownerDetails.setSizePolicy(sizePolicy)
        self.ownerDetails.setMinimumSize(QSize(0, 50))
        self.ownerDetails.setMaximumSize(QSize(16777215, 80))
        self.ownerDetails.setStyleSheet(u"")
        self.ownerDetails.setFrameShape(QFrame.StyledPanel)
        self.ownerDetails.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.ownerDetails)
        self.horizontalLayout_51.setSpacing(15)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(0, 0, -1, 5)
        self.emailEdit = QLineEdit(self.ownerDetails)
        self.emailEdit.setObjectName(u"emailEdit")
        sizePolicy.setHeightForWidth(self.emailEdit.sizePolicy().hasHeightForWidth())
        self.emailEdit.setSizePolicy(sizePolicy)
        self.emailEdit.setStyleSheet(u"")

        self.horizontalLayout_51.addWidget(self.emailEdit)

        self.phoneNumberEdit = QLineEdit(self.ownerDetails)
        self.phoneNumberEdit.setObjectName(u"phoneNumberEdit")
        sizePolicy.setHeightForWidth(self.phoneNumberEdit.sizePolicy().hasHeightForWidth())
        self.phoneNumberEdit.setSizePolicy(sizePolicy)
        self.phoneNumberEdit.setStyleSheet(u"")

        self.horizontalLayout_51.addWidget(self.phoneNumberEdit)

        self.secondaryPhoneEdit = QLineEdit(self.ownerDetails)
        self.secondaryPhoneEdit.setObjectName(u"secondaryPhoneEdit")
        sizePolicy.setHeightForWidth(self.secondaryPhoneEdit.sizePolicy().hasHeightForWidth())
        self.secondaryPhoneEdit.setSizePolicy(sizePolicy)
        self.secondaryPhoneEdit.setStyleSheet(u"")

        self.horizontalLayout_51.addWidget(self.secondaryPhoneEdit)


        self.verticalLayout_9.addWidget(self.ownerDetails)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_5)

        self.label_15 = QLabel(self.ownerDetailsFrame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy5.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy5)
        self.label_15.setStyleSheet(u"	color:rgb(52, 52, 52);")

        self.verticalLayout_9.addWidget(self.label_15)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_9.addItem(self.verticalSpacer_6)

        self.ownerDetails_2 = QFrame(self.ownerDetailsFrame)
        self.ownerDetails_2.setObjectName(u"ownerDetails_2")
        sizePolicy.setHeightForWidth(self.ownerDetails_2.sizePolicy().hasHeightForWidth())
        self.ownerDetails_2.setSizePolicy(sizePolicy)
        self.ownerDetails_2.setMinimumSize(QSize(0, 50))
        self.ownerDetails_2.setMaximumSize(QSize(16777215, 80))
        self.ownerDetails_2.setStyleSheet(u"")
        self.ownerDetails_2.setFrameShape(QFrame.StyledPanel)
        self.ownerDetails_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.ownerDetails_2)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, -1, 5)
        self.provinceComboBox = QComboBox(self.ownerDetails_2)
        self.provinceComboBox.setObjectName(u"provinceComboBox")
        sizePolicy.setHeightForWidth(self.provinceComboBox.sizePolicy().hasHeightForWidth())
        self.provinceComboBox.setSizePolicy(sizePolicy)
        self.provinceComboBox.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.provinceComboBox.setFocusPolicy(Qt.NoFocus)
        self.provinceComboBox.setStyleSheet(u"")
        self.provinceComboBox.setEditable(True)
        self.provinceComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.provinceComboBox.setDuplicatesEnabled(False)
        self.provinceComboBox.setFrame(True)

        self.horizontalLayout_30.addWidget(self.provinceComboBox)

        self.cityComboBox = QComboBox(self.ownerDetails_2)
        self.cityComboBox.setObjectName(u"cityComboBox")
        sizePolicy.setHeightForWidth(self.cityComboBox.sizePolicy().hasHeightForWidth())
        self.cityComboBox.setSizePolicy(sizePolicy)
        self.cityComboBox.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.cityComboBox.setFocusPolicy(Qt.NoFocus)
        self.cityComboBox.setStyleSheet(u"")
        self.cityComboBox.setEditable(True)
        self.cityComboBox.setMaxVisibleItems(10)

        self.horizontalLayout_30.addWidget(self.cityComboBox)

        self.barangayComboBox = QComboBox(self.ownerDetails_2)
        self.barangayComboBox.setObjectName(u"barangayComboBox")
        sizePolicy.setHeightForWidth(self.barangayComboBox.sizePolicy().hasHeightForWidth())
        self.barangayComboBox.setSizePolicy(sizePolicy)
        self.barangayComboBox.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.barangayComboBox.setFocusPolicy(Qt.NoFocus)
        self.barangayComboBox.setStyleSheet(u"")
        self.barangayComboBox.setEditable(True)

        self.horizontalLayout_30.addWidget(self.barangayComboBox)


        self.verticalLayout_9.addWidget(self.ownerDetails_2)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_9.addItem(self.verticalSpacer_7)

        self.ownerDetails_3 = QFrame(self.ownerDetailsFrame)
        self.ownerDetails_3.setObjectName(u"ownerDetails_3")
        sizePolicy.setHeightForWidth(self.ownerDetails_3.sizePolicy().hasHeightForWidth())
        self.ownerDetails_3.setSizePolicy(sizePolicy)
        self.ownerDetails_3.setMinimumSize(QSize(0, 50))
        self.ownerDetails_3.setMaximumSize(QSize(16777215, 80))
        self.ownerDetails_3.setStyleSheet(u"")
        self.ownerDetails_3.setFrameShape(QFrame.StyledPanel)
        self.ownerDetails_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.ownerDetails_3)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 0, -1, -1)
        self.detailedAddressEdit = QLineEdit(self.ownerDetails_3)
        self.detailedAddressEdit.setObjectName(u"detailedAddressEdit")
        sizePolicy.setHeightForWidth(self.detailedAddressEdit.sizePolicy().hasHeightForWidth())
        self.detailedAddressEdit.setSizePolicy(sizePolicy)
        self.detailedAddressEdit.setStyleSheet(u"")

        self.horizontalLayout_31.addWidget(self.detailedAddressEdit)


        self.verticalLayout_9.addWidget(self.ownerDetails_3)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_8)

        self.frame_12 = QFrame(self.ownerDetailsFrame)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setMaximumSize(QSize(16777215, 80))
        self.frame_12.setStyleSheet(u"QPushButton{\n"
"	font-family: \"Montserrat SemiBold\";\n"
"	font-weight: 63;\n"
"	color:rgb(52, 52, 52);\n"
"}")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, -1, -1, 5)
        self.horizontalSpacer = QSpacerItem(120, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer)

        self.confirmButton = QPushButton(self.frame_12)
        self.confirmButton.setObjectName(u"confirmButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.confirmButton.sizePolicy().hasHeightForWidth())
        self.confirmButton.setSizePolicy(sizePolicy6)
        self.confirmButton.setMaximumSize(QSize(450, 60))
        self.confirmButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.confirmButton.setStyleSheet(u"QPushButton{\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.horizontalLayout_23.addWidget(self.confirmButton)

        self.cancelButton = QPushButton(self.frame_12)
        self.cancelButton.setObjectName(u"cancelButton")
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMaximumSize(QSize(450, 60))
        self.cancelButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancelButton.setStyleSheet(u"QPushButton{\n"
"	background-color:	rgb(220, 90, 90);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"\n"
"}")

        self.horizontalLayout_23.addWidget(self.cancelButton)

        self.updateBasicInfo = QPushButton(self.frame_12)
        self.updateBasicInfo.setObjectName(u"updateBasicInfo")
        sizePolicy.setHeightForWidth(self.updateBasicInfo.sizePolicy().hasHeightForWidth())
        self.updateBasicInfo.setSizePolicy(sizePolicy)
        self.updateBasicInfo.setMaximumSize(QSize(450, 60))
        self.updateBasicInfo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.updateBasicInfo.setStyleSheet(u"QPushButton{\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.horizontalLayout_23.addWidget(self.updateBasicInfo)

        self.horizontalSpacer_4 = QSpacerItem(120, 50, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_4)


        self.verticalLayout_9.addWidget(self.frame_12)


        self.verticalLayout_12.addWidget(self.ownerDetailsFrame)

        self.stackedWidget.addWidget(self.AddpatientPage)
        self.ownerDetailsFrame.raise_()
        self.frame_2.raise_()
        self.addPatientBackBtn.raise_()
        self.PetRecords = QWidget()
        self.PetRecords.setObjectName(u"PetRecords")
        self.PetRecords.setStyleSheet(u"background:transparent;")
        self.verticalLayout_10 = QVBoxLayout(self.PetRecords)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.RecordsBackBtn = QPushButton(self.PetRecords)
        self.RecordsBackBtn.setObjectName(u"RecordsBackBtn")
        self.RecordsBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.RecordsBackBtn.setIcon(icon10)

        self.verticalLayout_10.addWidget(self.RecordsBackBtn, 0, Qt.AlignLeft)

        self.PersonalRecords = QFrame(self.PetRecords)
        self.PersonalRecords.setObjectName(u"PersonalRecords")
        sizePolicy.setHeightForWidth(self.PersonalRecords.sizePolicy().hasHeightForWidth())
        self.PersonalRecords.setSizePolicy(sizePolicy)
        self.PersonalRecords.setMaximumSize(QSize(16777215, 150))
        self.PersonalRecords.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"}")
        self.PersonalRecords.setFrameShape(QFrame.StyledPanel)
        self.PersonalRecords.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.PersonalRecords)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pageHeader2 = QLabel(self.PersonalRecords)
        self.pageHeader2.setObjectName(u"pageHeader2")
        self.pageHeader2.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pageHeader2)

        self.clinicIconP2 = QLabel(self.PersonalRecords)
        self.clinicIconP2.setObjectName(u"clinicIconP2")
        self.clinicIconP2.setMaximumSize(QSize(145, 60))
        self.clinicIconP2.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP2.setScaledContents(True)
        self.clinicIconP2.setAlignment(Qt.AlignCenter)
        self.clinicIconP2.setWordWrap(False)

        self.horizontalLayout_5.addWidget(self.clinicIconP2, 0, Qt.AlignTop)


        self.verticalLayout_10.addWidget(self.PersonalRecords, 0, Qt.AlignTop)

        self.searchframe = QFrame(self.PetRecords)
        self.searchframe.setObjectName(u"searchframe")
        sizePolicy.setHeightForWidth(self.searchframe.sizePolicy().hasHeightForWidth())
        self.searchframe.setSizePolicy(sizePolicy)
        self.searchframe.setStyleSheet(u"")
        self.horizontalLayout_4 = QHBoxLayout(self.searchframe)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(-1, 20, -1, 20)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.searchBar = QLineEdit(self.searchframe)
        self.searchBar.setObjectName(u"searchBar")
        sizePolicy.setHeightForWidth(self.searchBar.sizePolicy().hasHeightForWidth())
        self.searchBar.setSizePolicy(sizePolicy)
        self.searchBar.setAutoFillBackground(False)
        self.searchBar.setStyleSheet(u"QLineEdit#searchBar {\n"
"    background-color: rgb(250, 250, 250);\n"
"    border-top-left-radius: 10px;\n"
" 	border-bottom-left-radius: 10px;\n"
"	border-top:2px solid rgb(133, 164, 177);\n"
"	border-left:2px solid rgb(133, 164, 177);\n"
"	border-bottom:2px solid rgb(133, 164, 177);\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 15px;\n"
"}\n"
"QLineEdit#searchBar:focus{\n"
"    background-color: rgb(239, 239, 239);\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.searchBar)

        self.searchButton = QFrame(self.searchframe)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setStyleSheet(u"#searchButton{\n"
"	border-top:2px solid rgb(133, 164, 177);\n"
"	border-right:2px solid rgb(133, 164, 177);\n"
"	border-bottom:2px solid rgb(133, 164, 177);\n"
"    background-color: rgb(250, 250, 250);\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"")
        self.searchButton.setFrameShape(QFrame.StyledPanel)
        self.searchButton.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.searchButton)
        self.horizontalLayout_6.setSpacing(9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.searchIcon = QLabel(self.searchButton)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setMaximumSize(QSize(24, 24))
        self.searchIcon.setStyleSheet(u"")
        self.searchIcon.setPixmap(QPixmap(u":/Icons/Icons/searchIcon.png"))
        self.searchIcon.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.searchIcon)


        self.horizontalLayout_4.addWidget(self.searchButton)


        self.verticalLayout_10.addWidget(self.searchframe, 0, Qt.AlignTop)

        self.patientScrollArea = QScrollArea(self.PetRecords)
        self.patientScrollArea.setObjectName(u"patientScrollArea")
        self.patientScrollArea.setStyleSheet(u"#patientScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"#patientScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#patientScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"#patientScrollArea QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"#patientScrollArea QScrollBar::add-line:vertical,\n"
"#patientScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#patientScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"")
        self.patientScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 150, 33))
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setSpacing(5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_30 = QLabel(self.scrollAreaWidgetContents)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setStyleSheet(u"font: 81 16pt \"Montserrat ExtraBold\";\n"
"color:rgb(141, 141, 141);")

        self.verticalLayout_11.addWidget(self.label_30, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.patientScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.patientScrollArea)

        self.stackedWidget.addWidget(self.PetRecords)
        self.AppointmentPage = QWidget()
        self.AppointmentPage.setObjectName(u"AppointmentPage")
        self.AppointmentPage.setStyleSheet(u"QWidget{\n"
"	background:transparent;\n"
"\n"
"}\n"
"")
        self.verticalLayout_13 = QVBoxLayout(self.AppointmentPage)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.appointmentBackBtn = QPushButton(self.AppointmentPage)
        self.appointmentBackBtn.setObjectName(u"appointmentBackBtn")
        self.appointmentBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.appointmentBackBtn.setIcon(icon10)

        self.verticalLayout_13.addWidget(self.appointmentBackBtn, 0, Qt.AlignLeft)

        self.frame_4 = QFrame(self.AppointmentPage)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMaximumSize(QSize(16777215, 150))
        self.frame_4.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"\n"
"}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pageHeader3 = QLabel(self.frame_4)
        self.pageHeader3.setObjectName(u"pageHeader3")
        sizePolicy3.setHeightForWidth(self.pageHeader3.sizePolicy().hasHeightForWidth())
        self.pageHeader3.setSizePolicy(sizePolicy3)
        self.pageHeader3.setStyleSheet(u"")

        self.horizontalLayout_8.addWidget(self.pageHeader3)

        self.clinicIconP3 = QLabel(self.frame_4)
        self.clinicIconP3.setObjectName(u"clinicIconP3")
        self.clinicIconP3.setMaximumSize(QSize(145, 60))
        self.clinicIconP3.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP3.setScaledContents(True)
        self.clinicIconP3.setAlignment(Qt.AlignCenter)
        self.clinicIconP3.setWordWrap(False)

        self.horizontalLayout_8.addWidget(self.clinicIconP3)


        self.verticalLayout_13.addWidget(self.frame_4, 0, Qt.AlignTop)

        self.frame_5 = QFrame(self.AppointmentPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy4.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy4)
        self.frame_5.setMaximumSize(QSize(16777215, 100))
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_5)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy4.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy4)
        self.frame_6.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: rgb(166, 166, 166);\n"
"	font-family:\"Montserrat SemiBold\";\n"
"    font-weight: 63;\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(252, 213, 151);   /* Active bg color */\n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);                         \n"
"}")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 15, 0, 15)
        self.websiteBtn = QPushButton(self.frame_6)
        self.websiteBtn.setObjectName(u"websiteBtn")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.websiteBtn.sizePolicy().hasHeightForWidth())
        self.websiteBtn.setSizePolicy(sizePolicy7)
        self.websiteBtn.setMinimumSize(QSize(0, 45))
        self.websiteBtn.setMaximumSize(QSize(16777215, 60))
        self.websiteBtn.setStyleSheet(u"")

        self.horizontalLayout_12.addWidget(self.websiteBtn)

        self.walkInBtn = QPushButton(self.frame_6)
        self.walkInBtn.setObjectName(u"walkInBtn")
        sizePolicy7.setHeightForWidth(self.walkInBtn.sizePolicy().hasHeightForWidth())
        self.walkInBtn.setSizePolicy(sizePolicy7)
        self.walkInBtn.setMinimumSize(QSize(0, 45))
        self.walkInBtn.setMaximumSize(QSize(16777215, 60))
        self.walkInBtn.setStyleSheet(u"")

        self.horizontalLayout_12.addWidget(self.walkInBtn)


        self.horizontalLayout_11.addWidget(self.frame_6)

        self.searchframe_2 = QFrame(self.frame_5)
        self.searchframe_2.setObjectName(u"searchframe_2")
        sizePolicy1.setHeightForWidth(self.searchframe_2.sizePolicy().hasHeightForWidth())
        self.searchframe_2.setSizePolicy(sizePolicy1)
        self.searchframe_2.setStyleSheet(u"")
        self.horizontalLayout_9 = QHBoxLayout(self.searchframe_2)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_9.setContentsMargins(0, 7, 0, 7)
        self.searchBar_2 = QLineEdit(self.searchframe_2)
        self.searchBar_2.setObjectName(u"searchBar_2")
        sizePolicy1.setHeightForWidth(self.searchBar_2.sizePolicy().hasHeightForWidth())
        self.searchBar_2.setSizePolicy(sizePolicy1)
        self.searchBar_2.setMinimumSize(QSize(234, 44))
        self.searchBar_2.setMaximumSize(QSize(16777215, 50))
        self.searchBar_2.setAutoFillBackground(False)
        self.searchBar_2.setStyleSheet(u"QLineEdit#searchBar_2 {\n"
"    background-color: rgb(250, 250, 250);\n"
"    border-top-left-radius: 10px;\n"
" 	border-bottom-left-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 15px;\n"
"	border-top:2px solid rgb(133, 164, 177);\n"
"	border-left:2px solid rgb(133, 164, 177);\n"
"	border-bottom:2px solid rgb(133, 164, 177);\n"
"}\n"
"\n"
"QLineEdit#searchBar_2 :focus{\n"
"    background-color: rgb(239, 239, 239);\n"
"}\n"
"")

        self.horizontalLayout_9.addWidget(self.searchBar_2)

        self.searchButton_2 = QFrame(self.searchframe_2)
        self.searchButton_2.setObjectName(u"searchButton_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.searchButton_2.sizePolicy().hasHeightForWidth())
        self.searchButton_2.setSizePolicy(sizePolicy8)
        self.searchButton_2.setMaximumSize(QSize(16777215, 50))
        self.searchButton_2.setStyleSheet(u"QFrame#searchButton_2{\n"
"	border-top:2px solid rgb(133, 164, 177);\n"
"	border-right:2px solid rgb(133, 164, 177);\n"
"	border-bottom:2px solid rgb(133, 164, 177);\n"
"    background-color: rgb(250, 250, 250);\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"")
        self.searchButton_2.setFrameShape(QFrame.StyledPanel)
        self.searchButton_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.searchButton_2)
        self.horizontalLayout_10.setSpacing(9)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 9, 9, 9)
        self.searchIcon_2 = QLabel(self.searchButton_2)
        self.searchIcon_2.setObjectName(u"searchIcon_2")
        self.searchIcon_2.setMaximumSize(QSize(24, 24))
        self.searchIcon_2.setStyleSheet(u"")
        self.searchIcon_2.setPixmap(QPixmap(u":/Icons/Icons/searchIcon.png"))
        self.searchIcon_2.setScaledContents(True)

        self.horizontalLayout_10.addWidget(self.searchIcon_2)


        self.horizontalLayout_9.addWidget(self.searchButton_2)


        self.horizontalLayout_11.addWidget(self.searchframe_2)


        self.verticalLayout_13.addWidget(self.frame_5)

        self.walkInOrWeb = QStackedWidget(self.AppointmentPage)
        self.walkInOrWeb.setObjectName(u"walkInOrWeb")
        self.walkInOrWeb.setMinimumSize(QSize(0, 492))
        self.walkInOrWeb.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: rgb(166, 166, 166);\n"
"	font-family:\"Montserrat SemiBold\";\n"
"    font-weight: 63;\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(124, 181, 208); \n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);                         \n"
"}")
        self.website = QWidget()
        self.website.setObjectName(u"website")
        self.verticalLayout_16 = QVBoxLayout(self.website)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.AcceptedDeclineBtns = QFrame(self.website)
        self.AcceptedDeclineBtns.setObjectName(u"AcceptedDeclineBtns")
        sizePolicy4.setHeightForWidth(self.AcceptedDeclineBtns.sizePolicy().hasHeightForWidth())
        self.AcceptedDeclineBtns.setSizePolicy(sizePolicy4)
        self.AcceptedDeclineBtns.setMaximumSize(QSize(16777215, 90))
        self.AcceptedDeclineBtns.setStyleSheet(u"")
        self.AcceptedDeclineBtns.setFrameShape(QFrame.StyledPanel)
        self.AcceptedDeclineBtns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.AcceptedDeclineBtns)
        self.horizontalLayout_32.setSpacing(5)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 5, 0, 5)
        self.pendingWebBtn = QPushButton(self.AcceptedDeclineBtns)
        self.pendingWebBtn.setObjectName(u"pendingWebBtn")
        sizePolicy.setHeightForWidth(self.pendingWebBtn.sizePolicy().hasHeightForWidth())
        self.pendingWebBtn.setSizePolicy(sizePolicy)
        self.pendingWebBtn.setMaximumSize(QSize(16777215, 60))
        self.pendingWebBtn.setStyleSheet(u"")

        self.horizontalLayout_32.addWidget(self.pendingWebBtn)

        self.AcceptedBtn = QPushButton(self.AcceptedDeclineBtns)
        self.AcceptedBtn.setObjectName(u"AcceptedBtn")
        sizePolicy.setHeightForWidth(self.AcceptedBtn.sizePolicy().hasHeightForWidth())
        self.AcceptedBtn.setSizePolicy(sizePolicy)
        self.AcceptedBtn.setMaximumSize(QSize(16777215, 60))
        self.AcceptedBtn.setStyleSheet(u"")

        self.horizontalLayout_32.addWidget(self.AcceptedBtn)

        self.DeclinedBtn = QPushButton(self.AcceptedDeclineBtns)
        self.DeclinedBtn.setObjectName(u"DeclinedBtn")
        sizePolicy.setHeightForWidth(self.DeclinedBtn.sizePolicy().hasHeightForWidth())
        self.DeclinedBtn.setSizePolicy(sizePolicy)
        self.DeclinedBtn.setMaximumSize(QSize(16777215, 60))
        self.DeclinedBtn.setStyleSheet(u"")

        self.horizontalLayout_32.addWidget(self.DeclinedBtn)


        self.verticalLayout_16.addWidget(self.AcceptedDeclineBtns)

        self.webAppointmentStackWidget = QStackedWidget(self.website)
        self.webAppointmentStackWidget.setObjectName(u"webAppointmentStackWidget")
        sizePolicy4.setHeightForWidth(self.webAppointmentStackWidget.sizePolicy().hasHeightForWidth())
        self.webAppointmentStackWidget.setSizePolicy(sizePolicy4)
        self.webAppointmentStackWidget.setMinimumSize(QSize(0, 440))
        self.webAppointmentStackWidget.setStyleSheet(u"QScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"QScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"QScrollAreaa QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:vertical,\n"
"QScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QScrollArea QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 10px; /* horizontal thickness */\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:horizontal {\n"
"    background-color: rgb(129, 191, "
                        "218);\n"
"    border-radius: 5px;\n"
"    height: 10px; /* same as scrollbar height */\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:horizontal,\n"
"QScrollArea QScrollBar::sub-line:horizontal {\n"
"    width: 0px; /* hide buttons */\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:horizontal {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.webAppPending = QWidget()
        self.webAppPending.setObjectName(u"webAppPending")
        self.verticalLayout_28 = QVBoxLayout(self.webAppPending)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_7 = QScrollArea(self.webAppPending)
        self.scrollArea_7.setObjectName(u"scrollArea_7")
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWebAppPending = QWidget()
        self.scrollAreaWebAppPending.setObjectName(u"scrollAreaWebAppPending")
        self.scrollAreaWebAppPending.setGeometry(QRect(0, 0, 98, 28))
        sizePolicy.setHeightForWidth(self.scrollAreaWebAppPending.sizePolicy().hasHeightForWidth())
        self.scrollAreaWebAppPending.setSizePolicy(sizePolicy)
        self.verticalLayout_42 = QVBoxLayout(self.scrollAreaWebAppPending)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_7.setWidget(self.scrollAreaWebAppPending)

        self.verticalLayout_28.addWidget(self.scrollArea_7)

        self.webAppointmentStackWidget.addWidget(self.webAppPending)
        self.webAppAccepted = QWidget()
        self.webAppAccepted.setObjectName(u"webAppAccepted")
        self.verticalLayout_40 = QVBoxLayout(self.webAppAccepted)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_8 = QScrollArea(self.webAppAccepted)
        self.scrollArea_8.setObjectName(u"scrollArea_8")
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollArea_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWebAppAccepted = QWidget()
        self.scrollAreaWebAppAccepted.setObjectName(u"scrollAreaWebAppAccepted")
        self.scrollAreaWebAppAccepted.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_43 = QVBoxLayout(self.scrollAreaWebAppAccepted)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_8.setWidget(self.scrollAreaWebAppAccepted)

        self.verticalLayout_40.addWidget(self.scrollArea_8)

        self.webAppointmentStackWidget.addWidget(self.webAppAccepted)
        self.webAppDeclined = QWidget()
        self.webAppDeclined.setObjectName(u"webAppDeclined")
        self.verticalLayout_41 = QVBoxLayout(self.webAppDeclined)
        self.verticalLayout_41.setSpacing(0)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_9 = QScrollArea(self.webAppDeclined)
        self.scrollArea_9.setObjectName(u"scrollArea_9")
        self.scrollArea_9.setStyleSheet(u"")
        self.scrollArea_9.setWidgetResizable(True)
        self.scrollArea_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWebAppDeclined = QWidget()
        self.scrollAreaWebAppDeclined.setObjectName(u"scrollAreaWebAppDeclined")
        self.scrollAreaWebAppDeclined.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_44 = QVBoxLayout(self.scrollAreaWebAppDeclined)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_9.setWidget(self.scrollAreaWebAppDeclined)

        self.verticalLayout_41.addWidget(self.scrollArea_9)

        self.webAppointmentStackWidget.addWidget(self.webAppDeclined)

        self.verticalLayout_16.addWidget(self.webAppointmentStackWidget)

        self.walkInOrWeb.addWidget(self.website)
        self.walkIn = QWidget()
        self.walkIn.setObjectName(u"walkIn")
        sizePolicy.setHeightForWidth(self.walkIn.sizePolicy().hasHeightForWidth())
        self.walkIn.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.walkIn)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.addWalkinButton = QFrame(self.walkIn)
        self.addWalkinButton.setObjectName(u"addWalkinButton")
        sizePolicy.setHeightForWidth(self.addWalkinButton.sizePolicy().hasHeightForWidth())
        self.addWalkinButton.setSizePolicy(sizePolicy)
        self.addWalkinButton.setMinimumSize(QSize(0, 70))
        self.addWalkinButton.setMaximumSize(QSize(16777215, 120))
        self.addWalkinButton.setStyleSheet(u"#addWalkinButton{\n"
"	border: 2px dashed #4F4F4F;\n"
"    border-radius: 10px;\n"
"}\n"
"#addWalkinButton:hover{\n"
"	background-color:rgb(230, 230, 230);\n"
"}")
        self.addWalkinButton.setFrameShape(QFrame.StyledPanel)
        self.addWalkinButton.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.addWalkinButton)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(30, 8, 0, 8)
        self.toolButton_3 = QToolButton(self.addWalkinButton)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        icon11 = QIcon()
        icon11.addFile(u":/Icons/Icons/AddIconAppointment.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_3.setIcon(icon11)
        self.toolButton_3.setIconSize(QSize(50, 50))

        self.horizontalLayout_13.addWidget(self.toolButton_3)

        self.toolButton_2 = QToolButton(self.addWalkinButton)
        self.toolButton_2.setObjectName(u"toolButton_2")
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        self.toolButton_2.setStyleSheet(u"QToolButton{\n"
"background-color:transparent;\n"
"border:none;\n"
"	font-family:\"Montserrat ExtraBold\";\n"
"	font-weight:81;\n"
"	color: #4F4F4F;\n"
"}")
        self.toolButton_2.setIconSize(QSize(34, 34))
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_13.addWidget(self.toolButton_2)


        self.verticalLayout_6.addWidget(self.addWalkinButton, 0, Qt.AlignTop)

        self.pendingCompletedBtn = QFrame(self.walkIn)
        self.pendingCompletedBtn.setObjectName(u"pendingCompletedBtn")
        sizePolicy4.setHeightForWidth(self.pendingCompletedBtn.sizePolicy().hasHeightForWidth())
        self.pendingCompletedBtn.setSizePolicy(sizePolicy4)
        self.pendingCompletedBtn.setStyleSheet(u"")
        self.pendingCompletedBtn.setFrameShape(QFrame.StyledPanel)
        self.pendingCompletedBtn.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.pendingCompletedBtn)
        self.horizontalLayout_26.setSpacing(5)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 5, 0, 5)
        self.pendingBtn = QPushButton(self.pendingCompletedBtn)
        self.pendingBtn.setObjectName(u"pendingBtn")
        sizePolicy.setHeightForWidth(self.pendingBtn.sizePolicy().hasHeightForWidth())
        self.pendingBtn.setSizePolicy(sizePolicy)
        self.pendingBtn.setMaximumSize(QSize(16777215, 60))
        self.pendingBtn.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.pendingBtn)

        self.completedBtn = QPushButton(self.pendingCompletedBtn)
        self.completedBtn.setObjectName(u"completedBtn")
        sizePolicy.setHeightForWidth(self.completedBtn.sizePolicy().hasHeightForWidth())
        self.completedBtn.setSizePolicy(sizePolicy)
        self.completedBtn.setMaximumSize(QSize(16777215, 60))
        self.completedBtn.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.completedBtn)

        self.overdueBtn = QPushButton(self.pendingCompletedBtn)
        self.overdueBtn.setObjectName(u"overdueBtn")
        sizePolicy.setHeightForWidth(self.overdueBtn.sizePolicy().hasHeightForWidth())
        self.overdueBtn.setSizePolicy(sizePolicy)
        self.overdueBtn.setMaximumSize(QSize(16777215, 60))
        self.overdueBtn.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.overdueBtn)

        self.cancelledBtn = QPushButton(self.pendingCompletedBtn)
        self.cancelledBtn.setObjectName(u"cancelledBtn")
        sizePolicy.setHeightForWidth(self.cancelledBtn.sizePolicy().hasHeightForWidth())
        self.cancelledBtn.setSizePolicy(sizePolicy)
        self.cancelledBtn.setMinimumSize(QSize(0, 45))
        self.cancelledBtn.setMaximumSize(QSize(16777215, 60))
        self.cancelledBtn.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.cancelledBtn)


        self.verticalLayout_6.addWidget(self.pendingCompletedBtn, 0, Qt.AlignTop)

        self.statusStackedWidget = QStackedWidget(self.walkIn)
        self.statusStackedWidget.setObjectName(u"statusStackedWidget")
        sizePolicy4.setHeightForWidth(self.statusStackedWidget.sizePolicy().hasHeightForWidth())
        self.statusStackedWidget.setSizePolicy(sizePolicy4)
        self.statusStackedWidget.setStyleSheet(u"QScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"QScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"QScrollAreaa QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:vertical,\n"
"QScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QScrollArea QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 10px; /* horizontal thickness */\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:horizontal {\n"
"    background-color: rgb(129, 191, "
                        "218);\n"
"    border-radius: 5px;\n"
"    height: 10px; /* same as scrollbar height */\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:horizontal,\n"
"QScrollArea QScrollBar::sub-line:horizontal {\n"
"    width: 0px; /* hide buttons */\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:horizontal {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.pendingPage = QWidget()
        self.pendingPage.setObjectName(u"pendingPage")
        sizePolicy4.setHeightForWidth(self.pendingPage.sizePolicy().hasHeightForWidth())
        self.pendingPage.setSizePolicy(sizePolicy4)
        self.pendingPage.setStyleSheet(u"")
        self.verticalLayout_66 = QVBoxLayout(self.pendingPage)
        self.verticalLayout_66.setSpacing(0)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.verticalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.walkInScrollArea = QScrollArea(self.pendingPage)
        self.walkInScrollArea.setObjectName(u"walkInScrollArea")
        self.walkInScrollArea.setStyleSheet(u"#walkInScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"#walkInScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::add-line:vertical,\n"
"#walkInScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"#walkInScrollArea QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 10px; /* horizontal thickness */\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:horizo"
                        "ntal {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    height: 10px; /* same as scrollbar height */\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::add-line:horizontal,\n"
"#walkInScrollArea QScrollBar::sub-line:horizontal {\n"
"    width: 0px; /* hide buttons */\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::groove:horizontal {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.walkInScrollArea.setWidgetResizable(True)
        self.walkInScrollAreaWidgetContents = QWidget()
        self.walkInScrollAreaWidgetContents.setObjectName(u"walkInScrollAreaWidgetContents")
        self.walkInScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.walkInScrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_17 = QVBoxLayout(self.walkInScrollAreaWidgetContents)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.walkInScrollArea.setWidget(self.walkInScrollAreaWidgetContents)

        self.verticalLayout_66.addWidget(self.walkInScrollArea)

        self.statusStackedWidget.addWidget(self.pendingPage)
        self.completedPage = QWidget()
        self.completedPage.setObjectName(u"completedPage")
        sizePolicy4.setHeightForWidth(self.completedPage.sizePolicy().hasHeightForWidth())
        self.completedPage.setSizePolicy(sizePolicy4)
        self.verticalLayout_34 = QVBoxLayout(self.completedPage)
        self.verticalLayout_34.setSpacing(0)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_4 = QScrollArea(self.completedPage)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setStyleSheet(u"")
        self.scrollArea_4.setWidgetResizable(True)
        self.completedScrollAreaWidgetContents = QWidget()
        self.completedScrollAreaWidgetContents.setObjectName(u"completedScrollAreaWidgetContents")
        self.completedScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_37 = QVBoxLayout(self.completedScrollAreaWidgetContents)
        self.verticalLayout_37.setSpacing(6)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_4.setWidget(self.completedScrollAreaWidgetContents)

        self.verticalLayout_34.addWidget(self.scrollArea_4)

        self.statusStackedWidget.addWidget(self.completedPage)
        self.overduePage = QWidget()
        self.overduePage.setObjectName(u"overduePage")
        self.verticalLayout_35 = QVBoxLayout(self.overduePage)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_5 = QScrollArea(self.overduePage)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.overdueScrollAreaWidgetContents = QWidget()
        self.overdueScrollAreaWidgetContents.setObjectName(u"overdueScrollAreaWidgetContents")
        self.overdueScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_38 = QVBoxLayout(self.overdueScrollAreaWidgetContents)
        self.verticalLayout_38.setSpacing(6)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_5.setWidget(self.overdueScrollAreaWidgetContents)

        self.verticalLayout_35.addWidget(self.scrollArea_5)

        self.statusStackedWidget.addWidget(self.overduePage)
        self.cancelledPage = QWidget()
        self.cancelledPage.setObjectName(u"cancelledPage")
        self.verticalLayout_36 = QVBoxLayout(self.cancelledPage)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_6 = QScrollArea(self.cancelledPage)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setWidgetResizable(True)
        self.cancelledScrollAreaWidgetContents = QWidget()
        self.cancelledScrollAreaWidgetContents.setObjectName(u"cancelledScrollAreaWidgetContents")
        self.cancelledScrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_39 = QVBoxLayout(self.cancelledScrollAreaWidgetContents)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_6.setWidget(self.cancelledScrollAreaWidgetContents)

        self.verticalLayout_36.addWidget(self.scrollArea_6)

        self.statusStackedWidget.addWidget(self.cancelledPage)

        self.verticalLayout_6.addWidget(self.statusStackedWidget)

        self.walkInOrWeb.addWidget(self.walkIn)

        self.verticalLayout_13.addWidget(self.walkInOrWeb)

        self.stackedWidget.addWidget(self.AppointmentPage)
        self.SchedVax = QWidget()
        self.SchedVax.setObjectName(u"SchedVax")
        self.SchedVax.setStyleSheet(u"background-color: transparent;")
        self.horizontalLayout_2 = QHBoxLayout(self.SchedVax)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.schedFrame = QFrame(self.SchedVax)
        self.schedFrame.setObjectName(u"schedFrame")
        self.schedFrame.setStyleSheet(u"\n"
"QFrame{\n"
"	background-color: transparent;\n"
"\n"
"}\n"
"\n"
"")
        self.schedFrame.setFrameShape(QFrame.StyledPanel)
        self.schedFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.schedFrame)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.ReturnBackBtn = QPushButton(self.schedFrame)
        self.ReturnBackBtn.setObjectName(u"ReturnBackBtn")
        self.ReturnBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.ReturnBackBtn.setIcon(icon10)

        self.verticalLayout_23.addWidget(self.ReturnBackBtn, 0, Qt.AlignLeft)

        self.frame_70 = QFrame(self.schedFrame)
        self.frame_70.setObjectName(u"frame_70")
        sizePolicy.setHeightForWidth(self.frame_70.sizePolicy().hasHeightForWidth())
        self.frame_70.setSizePolicy(sizePolicy)
        self.frame_70.setStyleSheet(u"\n"
"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"\n"
"}")
        self.frame_70.setFrameShape(QFrame.StyledPanel)
        self.frame_70.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_65 = QHBoxLayout(self.frame_70)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.pageHeader4 = QLabel(self.frame_70)
        self.pageHeader4.setObjectName(u"pageHeader4")
        sizePolicy.setHeightForWidth(self.pageHeader4.sizePolicy().hasHeightForWidth())
        self.pageHeader4.setSizePolicy(sizePolicy)
        self.pageHeader4.setStyleSheet(u"")

        self.horizontalLayout_65.addWidget(self.pageHeader4)

        self.clinicIconP4 = QLabel(self.frame_70)
        self.clinicIconP4.setObjectName(u"clinicIconP4")
        sizePolicy.setHeightForWidth(self.clinicIconP4.sizePolicy().hasHeightForWidth())
        self.clinicIconP4.setSizePolicy(sizePolicy)
        self.clinicIconP4.setMaximumSize(QSize(145, 60))
        self.clinicIconP4.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP4.setScaledContents(True)

        self.horizontalLayout_65.addWidget(self.clinicIconP4)


        self.verticalLayout_23.addWidget(self.frame_70, 0, Qt.AlignTop)

        self.frame_71 = QFrame(self.schedFrame)
        self.frame_71.setObjectName(u"frame_71")
        sizePolicy4.setHeightForWidth(self.frame_71.sizePolicy().hasHeightForWidth())
        self.frame_71.setSizePolicy(sizePolicy4)
        self.frame_71.setMaximumSize(QSize(16777215, 90))
        self.frame_71.setStyleSheet(u"background-color: transparent;\n"
"")
        self.frame_71.setFrameShape(QFrame.StyledPanel)
        self.frame_71.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_72 = QHBoxLayout(self.frame_71)
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.horizontalLayout_72.setContentsMargins(0, 0, 0, 0)
        self.frame_80 = QFrame(self.frame_71)
        self.frame_80.setObjectName(u"frame_80")
        sizePolicy4.setHeightForWidth(self.frame_80.sizePolicy().hasHeightForWidth())
        self.frame_80.setSizePolicy(sizePolicy4)
        self.frame_80.setMaximumSize(QSize(16777215, 80))
        self.frame_80.setFrameShape(QFrame.StyledPanel)
        self.frame_80.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_75 = QHBoxLayout(self.frame_80)
        self.horizontalLayout_75.setObjectName(u"horizontalLayout_75")
        self.horizontalLayout_75.setContentsMargins(0, -1, -1, -1)
        self.monthComboBox = QComboBox(self.frame_80)
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.addItem("")
        self.monthComboBox.setObjectName(u"monthComboBox")
        sizePolicy.setHeightForWidth(self.monthComboBox.sizePolicy().hasHeightForWidth())
        self.monthComboBox.setSizePolicy(sizePolicy)
        self.monthComboBox.setMinimumSize(QSize(174, 45))
        self.monthComboBox.setMaximumSize(QSize(16777215, 80))
        self.monthComboBox.setStyleSheet(u"QComboBox {\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QComboBox QLineEdit {\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
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
"	border:1px solid rgb("
                        "209, 209, 209);\n"
"}\n"
"\n"
"/* List items */\n"
"QComboBox QAbstractItemView::item {\n"
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
"   "
                        " background: none;\n"
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
        self.monthComboBox.setMaxVisibleItems(12)

        self.horizontalLayout_75.addWidget(self.monthComboBox)


        self.horizontalLayout_72.addWidget(self.frame_80)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_72.addItem(self.horizontalSpacer_3)

        self.frame_78 = QFrame(self.frame_71)
        self.frame_78.setObjectName(u"frame_78")
        sizePolicy4.setHeightForWidth(self.frame_78.sizePolicy().hasHeightForWidth())
        self.frame_78.setSizePolicy(sizePolicy4)
        self.frame_78.setFrameShape(QFrame.StyledPanel)
        self.frame_78.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_73 = QHBoxLayout(self.frame_78)
        self.horizontalLayout_73.setSpacing(0)
        self.horizontalLayout_73.setObjectName(u"horizontalLayout_73")
        self.horizontalLayout_73.setContentsMargins(-1, -1, 0, -1)
        self.lineEdit_9 = QLineEdit(self.frame_78)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setMaximumSize(QSize(16777215, 45))
        self.lineEdit_9.setStyleSheet(u"#lineEdit_9 {\n"
"    background-color: #F0F0F0;\n"
"    border-top-left-radius: 10px;\n"
" 	border-bottom-left-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_73.addWidget(self.lineEdit_9)

        self.frame_79 = QFrame(self.frame_78)
        self.frame_79.setObjectName(u"frame_79")
        self.frame_79.setMaximumSize(QSize(16777215, 45))
        self.frame_79.setStyleSheet(u"QFrame#frame_79{\n"
"background-color: #F0F0F0;\n"
"border-top-right-radius:10px;\n"
"border-bottom-right-radius:10px;\n"
"}\n"
"")
        self.frame_79.setFrameShape(QFrame.StyledPanel)
        self.frame_79.setFrameShadow(QFrame.Raised)
        self.verticalLayout_65 = QVBoxLayout(self.frame_79)
        self.verticalLayout_65.setSpacing(0)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.verticalLayout_65.setContentsMargins(9, -1, -1, -1)
        self.label_172 = QLabel(self.frame_79)
        self.label_172.setObjectName(u"label_172")
        self.label_172.setMaximumSize(QSize(24, 24))
        self.label_172.setPixmap(QPixmap(u":/Icons/Icons/searchIcon.png"))
        self.label_172.setScaledContents(True)

        self.verticalLayout_65.addWidget(self.label_172)


        self.horizontalLayout_73.addWidget(self.frame_79)


        self.horizontalLayout_72.addWidget(self.frame_78)


        self.verticalLayout_23.addWidget(self.frame_71)

        self.frame_72 = QFrame(self.schedFrame)
        self.frame_72.setObjectName(u"frame_72")
        sizePolicy4.setHeightForWidth(self.frame_72.sizePolicy().hasHeightForWidth())
        self.frame_72.setSizePolicy(sizePolicy4)
        self.frame_72.setMaximumSize(QSize(16777215, 90))
        self.frame_72.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: rgb(166, 166, 166);\n"
"	font-family:\"Montserrat SemiBold\";\n"
"    font-weight: 63;\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(252, 213, 151);   /* Active bg color */\n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);                         \n"
"}")
        self.frame_72.setFrameShape(QFrame.StyledPanel)
        self.frame_72.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_72)
        self.horizontalLayout_17.setSpacing(5)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 5)
        self.pendingReturnBtn = QPushButton(self.frame_72)
        self.pendingReturnBtn.setObjectName(u"pendingReturnBtn")
        self.pendingReturnBtn.setMinimumSize(QSize(0, 45))
        self.pendingReturnBtn.setMaximumSize(QSize(16777215, 60))

        self.horizontalLayout_17.addWidget(self.pendingReturnBtn)

        self.completeReurnBtn = QPushButton(self.frame_72)
        self.completeReurnBtn.setObjectName(u"completeReurnBtn")
        self.completeReurnBtn.setMinimumSize(QSize(0, 45))
        self.completeReurnBtn.setMaximumSize(QSize(16777215, 60))
        self.completeReurnBtn.setStyleSheet(u"")

        self.horizontalLayout_17.addWidget(self.completeReurnBtn)

        self.overdueReturnBtn = QPushButton(self.frame_72)
        self.overdueReturnBtn.setObjectName(u"overdueReturnBtn")
        self.overdueReturnBtn.setMinimumSize(QSize(0, 45))
        self.overdueReturnBtn.setMaximumSize(QSize(16777215, 60))

        self.horizontalLayout_17.addWidget(self.overdueReturnBtn)


        self.verticalLayout_23.addWidget(self.frame_72)

        self.returnStackedWidget = QStackedWidget(self.schedFrame)
        self.returnStackedWidget.setObjectName(u"returnStackedWidget")
        self.returnStackedWidget.setStyleSheet(u"QScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"QScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"QScrollAreaa QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:vertical,\n"
"QScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QScrollArea QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 10px; /* horizontal thickness */\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#walkInScrollArea QScrollBar::handle:horizontal {\n"
"    background-color: rgb(129, 191, "
                        "218);\n"
"    border-radius: 5px;\n"
"    height: 10px; /* same as scrollbar height */\n"
"}\n"
"\n"
"QScrollArea QScrollBar::add-line:horizontal,\n"
"QScrollArea QScrollBar::sub-line:horizontal {\n"
"    width: 0px; /* hide buttons */\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea QScrollBar::groove:horizontal {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.pendingReturn = QWidget()
        self.pendingReturn.setObjectName(u"pendingReturn")
        self.verticalLayout_24 = QVBoxLayout(self.pendingReturn)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.schedReturnScrollArea = QScrollArea(self.pendingReturn)
        self.schedReturnScrollArea.setObjectName(u"schedReturnScrollArea")
        self.schedReturnScrollArea.setStyleSheet(u"#schedReturnScrollArea{\n"
"	border:none;\n"
"\n"
"}\n"
"#schedReturnScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#schedReturnScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"#schedReturnScrollArea QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"#schedReturnScrollArea QScrollBar::add-line:vertical,\n"
"#schedReturnScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#schedReturnScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"")
        self.schedReturnScrollArea.setWidgetResizable(True)
        self.pendingScrollPage = QWidget()
        self.pendingScrollPage.setObjectName(u"pendingScrollPage")
        self.pendingScrollPage.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_67 = QVBoxLayout(self.pendingScrollPage)
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.schedReturnScrollArea.setWidget(self.pendingScrollPage)

        self.verticalLayout_24.addWidget(self.schedReturnScrollArea)

        self.returnStackedWidget.addWidget(self.pendingReturn)
        self.CompletedReturn = QWidget()
        self.CompletedReturn.setObjectName(u"CompletedReturn")
        self.verticalLayout_29 = QVBoxLayout(self.CompletedReturn)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.CompletedReturn)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 450))
        self.scrollArea.setWidgetResizable(True)
        self.completedScrollPage = QWidget()
        self.completedScrollPage.setObjectName(u"completedScrollPage")
        self.completedScrollPage.setGeometry(QRect(0, 0, 98, 448))
        self.verticalLayout_33 = QVBoxLayout(self.completedScrollPage)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.scrollArea.setWidget(self.completedScrollPage)

        self.verticalLayout_29.addWidget(self.scrollArea)

        self.returnStackedWidget.addWidget(self.CompletedReturn)
        self.OverdureReturn = QWidget()
        self.OverdureReturn.setObjectName(u"OverdureReturn")
        self.verticalLayout_31 = QVBoxLayout(self.OverdureReturn)
        self.verticalLayout_31.setSpacing(0)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.OverdureReturn)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.overdueScrollPage = QWidget()
        self.overdueScrollPage.setObjectName(u"overdueScrollPage")
        self.overdueScrollPage.setGeometry(QRect(0, 0, 98, 41))
        self.verticalLayout_32 = QVBoxLayout(self.overdueScrollPage)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.pushButton = QPushButton(self.overdueScrollPage)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_32.addWidget(self.pushButton)

        self.scrollArea_2.setWidget(self.overdueScrollPage)

        self.verticalLayout_31.addWidget(self.scrollArea_2)

        self.returnStackedWidget.addWidget(self.OverdureReturn)

        self.verticalLayout_23.addWidget(self.returnStackedWidget)


        self.horizontalLayout_2.addWidget(self.schedFrame)

        self.stackedWidget.addWidget(self.SchedVax)
        self.PatientProfile = QWidget()
        self.PatientProfile.setObjectName(u"PatientProfile")
        self.PatientProfile.setStyleSheet(u"background:transparent;")
        self.verticalLayout_14 = QVBoxLayout(self.PatientProfile)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.profileBackbutton = QToolButton(self.PatientProfile)
        self.profileBackbutton.setObjectName(u"profileBackbutton")
        self.profileBackbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.profileBackbutton.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.profileBackbutton.setIcon(icon10)

        self.verticalLayout_14.addWidget(self.profileBackbutton)

        self.frame_13 = QFrame(self.PatientProfile)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy4.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy4)
        self.frame_13.setMaximumSize(QSize(16777215, 296))
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, -1, 5, -1)
        self.ProfileCard = QFrame(self.frame_13)
        self.ProfileCard.setObjectName(u"ProfileCard")
        sizePolicy4.setHeightForWidth(self.ProfileCard.sizePolicy().hasHeightForWidth())
        self.ProfileCard.setSizePolicy(sizePolicy4)
        self.ProfileCard.setStyleSheet(u"#ProfileCard{\n"
"	border-radius:10px;\n"
"	background-color:rgb(244, 244, 244);\n"
"\n"
"\n"
"}")
        self.ProfileCard.setFrameShape(QFrame.StyledPanel)
        self.ProfileCard.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.ProfileCard)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(20, -1, -1, 40)
        self.frame_8 = QFrame(self.ProfileCard)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy4.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy4)
        self.frame_8.setStyleSheet(u"font-family: \"Montserrat Light\";\n"
"font-weight:63;\n"
"color:rgb(58, 58, 58);")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_8)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(10, 0, 0, 0)
        self.profileNameLabel = QLabel(self.frame_8)
        self.profileNameLabel.setObjectName(u"profileNameLabel")
        self.profileNameLabel.setStyleSheet(u"font-family:\"Montserrat ExtraBold\";\n"
"font-weight: 81;\n"
"color:rgb(52, 52, 52);")

        self.verticalLayout_19.addWidget(self.profileNameLabel)

        self.profileEmailLabel = QLabel(self.frame_8)
        self.profileEmailLabel.setObjectName(u"profileEmailLabel")
        self.profileEmailLabel.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.profileEmailLabel)

        self.addressLabel = QLabel(self.frame_8)
        self.addressLabel.setObjectName(u"addressLabel")
        self.addressLabel.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.addressLabel)

        self.detailedAddressLabel = QLabel(self.frame_8)
        self.detailedAddressLabel.setObjectName(u"detailedAddressLabel")
        self.detailedAddressLabel.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.detailedAddressLabel)

        self.phoneLabel = QLabel(self.frame_8)
        self.phoneLabel.setObjectName(u"phoneLabel")
        self.phoneLabel.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.phoneLabel)


        self.gridLayout_2.addWidget(self.frame_8, 1, 2, 1, 1)

        self.frame_9 = QFrame(self.ProfileCard)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMaximumSize(QSize(16777215, 38))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.profileEditBtn = QToolButton(self.frame_10)
        self.profileEditBtn.setObjectName(u"profileEditBtn")
        self.profileEditBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.profileEditBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        icon12 = QIcon()
        icon12.addFile(u":/Icons/Icons/EditProfile.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profileEditBtn.setIcon(icon12)
        self.profileEditBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout_15.addWidget(self.profileEditBtn)

        self.profileDeleteBtn = QToolButton(self.frame_10)
        self.profileDeleteBtn.setObjectName(u"profileDeleteBtn")
        self.profileDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.profileDeleteBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        icon13 = QIcon()
        icon13.addFile(u":/Icons/Icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profileDeleteBtn.setIcon(icon13)
        self.profileDeleteBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout_15.addWidget(self.profileDeleteBtn)


        self.horizontalLayout_14.addWidget(self.frame_10, 0, Qt.AlignRight)


        self.gridLayout_2.addWidget(self.frame_9, 0, 2, 1, 1, Qt.AlignTop)

        self.profileIcon = QLabel(self.ProfileCard)
        self.profileIcon.setObjectName(u"profileIcon")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.profileIcon.sizePolicy().hasHeightForWidth())
        self.profileIcon.setSizePolicy(sizePolicy9)
        self.profileIcon.setMinimumSize(QSize(120, 120))
        self.profileIcon.setMaximumSize(QSize(120, 120))
        self.profileIcon.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.profileIcon.setScaledContents(True)

        self.gridLayout_2.addWidget(self.profileIcon, 1, 0, 1, 1)


        self.horizontalLayout_24.addWidget(self.ProfileCard)


        self.verticalLayout_14.addWidget(self.frame_13)

        self.profileStackedWidget = QStackedWidget(self.PatientProfile)
        self.profileStackedWidget.setObjectName(u"profileStackedWidget")
        self.petCardsPage = QWidget()
        self.petCardsPage.setObjectName(u"petCardsPage")
        self.verticalLayout_20 = QVBoxLayout(self.petCardsPage)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_3 = QScrollArea(self.petCardsPage)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setStyleSheet(u"#scrollArea_3{\n"
"	border:none;\n"
"\n"
"}\n"
"#scrollArea_3 QScrollBar:vertical {\n"
"    background: transparent; /* or any background */\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#scrollArea_3 QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"#scrollArea_3 QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"#scrollArea_3 QScrollBar::add-line:vertical,\n"
"#scrollArea_3 QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#scrollArea_3 QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 401, 109))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_6.setSpacing(10)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, -1)
        self.addPetButton = QFrame(self.scrollAreaWidgetContents_4)
        self.addPetButton.setObjectName(u"addPetButton")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.addPetButton.sizePolicy().hasHeightForWidth())
        self.addPetButton.setSizePolicy(sizePolicy10)
        self.addPetButton.setMinimumSize(QSize(401, 100))
        self.addPetButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addPetButton.setStyleSheet(u"#addPetButton{\n"
"	border-radius:10px;\n"
"	border:2px dashed #4F4F4F;\n"
"}\n"
"#addPetButton:hover{\n"
"	background-color:rgb(230, 230, 230);\n"
"}")
        self.addPetButton.setFrameShape(QFrame.StyledPanel)
        self.addPetButton.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.addPetButton)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(30, 0, 0, 0)
        self.plusSignBtn = QToolButton(self.addPetButton)
        self.plusSignBtn.setObjectName(u"plusSignBtn")
        self.plusSignBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.plusSignBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.plusSignBtn.setIcon(icon11)
        self.plusSignBtn.setIconSize(QSize(50, 50))

        self.horizontalLayout_16.addWidget(self.plusSignBtn)

        self.addpetQtoolBtn = QToolButton(self.addPetButton)
        self.addpetQtoolBtn.setObjectName(u"addpetQtoolBtn")
        sizePolicy10.setHeightForWidth(self.addpetQtoolBtn.sizePolicy().hasHeightForWidth())
        self.addpetQtoolBtn.setSizePolicy(sizePolicy10)
        self.addpetQtoolBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addpetQtoolBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;\n"
"font: 81 30pt \"Montserrat ExtraBold\";\n"
"color:#4F4F4F;")

        self.horizontalLayout_16.addWidget(self.addpetQtoolBtn)


        self.gridLayout_6.addWidget(self.addPetButton, 0, 0, 1, 1, Qt.AlignLeft|Qt.AlignTop)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_20.addWidget(self.scrollArea_3)

        self.profileStackedWidget.addWidget(self.petCardsPage)
        self.petDetailsPage = QWidget()
        self.petDetailsPage.setObjectName(u"petDetailsPage")
        self.petDetailsPage.setStyleSheet(u"QLineEdit{\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"\n"
"\n"
"QDateEdit {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
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
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-l"
                        "eft: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QComboBox QLineEdit {\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
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
"QComboBox QAbstractItemView::item {\n"
"    background-color:  rgb(232, 232, 232);\n"
"    col"
                        "or: black;\n"
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
"QComboBox QAbstractItemView QScrollBar::groove:vertical {\n"
"    background: transparent;"
                        "\n"
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
        self.verticalLayout_30 = QVBoxLayout(self.petDetailsPage)
        self.verticalLayout_30.setSpacing(15)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.petDetailsFrame = QFrame(self.petDetailsPage)
        self.petDetailsFrame.setObjectName(u"petDetailsFrame")
        sizePolicy2.setHeightForWidth(self.petDetailsFrame.sizePolicy().hasHeightForWidth())
        self.petDetailsFrame.setSizePolicy(sizePolicy2)
        self.petDetailsFrame.setFrameShape(QFrame.StyledPanel)
        self.petDetailsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.petDetailsFrame)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.petDetailsFrame)
        self.label_27.setObjectName(u"label_27")
        sizePolicy2.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy2)
        self.label_27.setStyleSheet(u"	font-family: \"Rubik Mono One\";\n"
"	color:rgb(39, 39, 39);")

        self.horizontalLayout_18.addWidget(self.label_27)


        self.verticalLayout_30.addWidget(self.petDetailsFrame)

        self.nameAndColorFrame = QFrame(self.petDetailsPage)
        self.nameAndColorFrame.setObjectName(u"nameAndColorFrame")
        sizePolicy.setHeightForWidth(self.nameAndColorFrame.sizePolicy().hasHeightForWidth())
        self.nameAndColorFrame.setSizePolicy(sizePolicy)
        self.nameAndColorFrame.setMinimumSize(QSize(0, 50))
        self.nameAndColorFrame.setMaximumSize(QSize(16777215, 80))
        self.nameAndColorFrame.setFrameShape(QFrame.StyledPanel)
        self.nameAndColorFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.nameAndColorFrame)
        self.horizontalLayout_19.setSpacing(35)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(5, 0, 5, 5)
        self.petName = QLineEdit(self.nameAndColorFrame)
        self.petName.setObjectName(u"petName")
        sizePolicy.setHeightForWidth(self.petName.sizePolicy().hasHeightForWidth())
        self.petName.setSizePolicy(sizePolicy)
        self.petName.setMinimumSize(QSize(174, 45))
        self.petName.setStyleSheet(u"")

        self.horizontalLayout_19.addWidget(self.petName)

        self.petColor = QLineEdit(self.nameAndColorFrame)
        self.petColor.setObjectName(u"petColor")
        sizePolicy.setHeightForWidth(self.petColor.sizePolicy().hasHeightForWidth())
        self.petColor.setSizePolicy(sizePolicy)
        self.petColor.setMinimumSize(QSize(174, 45))
        self.petColor.setStyleSheet(u"")

        self.horizontalLayout_19.addWidget(self.petColor)


        self.verticalLayout_30.addWidget(self.nameAndColorFrame)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_30.addItem(self.verticalSpacer)

        self.breedAndSpeciesFrame = QFrame(self.petDetailsPage)
        self.breedAndSpeciesFrame.setObjectName(u"breedAndSpeciesFrame")
        sizePolicy.setHeightForWidth(self.breedAndSpeciesFrame.sizePolicy().hasHeightForWidth())
        self.breedAndSpeciesFrame.setSizePolicy(sizePolicy)
        self.breedAndSpeciesFrame.setMinimumSize(QSize(0, 50))
        self.breedAndSpeciesFrame.setMaximumSize(QSize(16777215, 80))
        self.breedAndSpeciesFrame.setFrameShape(QFrame.StyledPanel)
        self.breedAndSpeciesFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.breedAndSpeciesFrame)
        self.horizontalLayout_21.setSpacing(20)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_69 = QFrame(self.breedAndSpeciesFrame)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setFrameShape(QFrame.StyledPanel)
        self.frame_69.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_83 = QHBoxLayout(self.frame_69)
        self.horizontalLayout_83.setSpacing(0)
        self.horizontalLayout_83.setObjectName(u"horizontalLayout_83")
        self.horizontalLayout_83.setContentsMargins(5, 0, 5, 5)
        self.breed = QLineEdit(self.frame_69)
        self.breed.setObjectName(u"breed")
        sizePolicy.setHeightForWidth(self.breed.sizePolicy().hasHeightForWidth())
        self.breed.setSizePolicy(sizePolicy)
        self.breed.setMinimumSize(QSize(174, 45))
        self.breed.setStyleSheet(u"")

        self.horizontalLayout_83.addWidget(self.breed)


        self.horizontalLayout_21.addWidget(self.frame_69)

        self.frame_59 = QFrame(self.breedAndSpeciesFrame)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setStyleSheet(u"")
        self.frame_59.setFrameShape(QFrame.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_82 = QHBoxLayout(self.frame_59)
        self.horizontalLayout_82.setSpacing(0)
        self.horizontalLayout_82.setObjectName(u"horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(5, 0, 5, 5)
        self.speciesComboBox = QComboBox(self.frame_59)
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.addItem("")
        self.speciesComboBox.setObjectName(u"speciesComboBox")
        sizePolicy.setHeightForWidth(self.speciesComboBox.sizePolicy().hasHeightForWidth())
        self.speciesComboBox.setSizePolicy(sizePolicy)
        self.speciesComboBox.setMinimumSize(QSize(174, 45))
        self.speciesComboBox.setStyleSheet(u"")
        self.speciesComboBox.setEditable(False)

        self.horizontalLayout_82.addWidget(self.speciesComboBox)

        self.otherSpeciesLineEdit = QLineEdit(self.frame_59)
        self.otherSpeciesLineEdit.setObjectName(u"otherSpeciesLineEdit")
        sizePolicy.setHeightForWidth(self.otherSpeciesLineEdit.sizePolicy().hasHeightForWidth())
        self.otherSpeciesLineEdit.setSizePolicy(sizePolicy)
        self.otherSpeciesLineEdit.setMinimumSize(QSize(174, 45))
        self.otherSpeciesLineEdit.setStyleSheet(u"QLineEdit#otherSpeciesLineEdit{\n"
"	border-top-right-radius:none;\n"
"	border-bottom-right-radius:none;\n"
"}")

        self.horizontalLayout_82.addWidget(self.otherSpeciesLineEdit)

        self.clearSpeciesBtn = QPushButton(self.frame_59)
        self.clearSpeciesBtn.setObjectName(u"clearSpeciesBtn")
        sizePolicy7.setHeightForWidth(self.clearSpeciesBtn.sizePolicy().hasHeightForWidth())
        self.clearSpeciesBtn.setSizePolicy(sizePolicy7)
        self.clearSpeciesBtn.setMinimumSize(QSize(0, 45))
        self.clearSpeciesBtn.setStyleSheet(u"background-color:rgb(245, 245, 245);\n"
"border:none;\n"
"margin:0;\n"
"padding:0;\n"
"padding-right:5px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-right-radius:10px;")
        icon14 = QIcon()
        icon14.addFile(u":/Icons/Icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clearSpeciesBtn.setIcon(icon14)
        self.clearSpeciesBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout_82.addWidget(self.clearSpeciesBtn)


        self.horizontalLayout_21.addWidget(self.frame_59)


        self.verticalLayout_30.addWidget(self.breedAndSpeciesFrame)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_30.addItem(self.verticalSpacer_2)

        self.bdayAge = QFrame(self.petDetailsPage)
        self.bdayAge.setObjectName(u"bdayAge")
        sizePolicy.setHeightForWidth(self.bdayAge.sizePolicy().hasHeightForWidth())
        self.bdayAge.setSizePolicy(sizePolicy)
        self.bdayAge.setMinimumSize(QSize(0, 50))
        self.bdayAge.setMaximumSize(QSize(16777215, 80))
        self.bdayAge.setFrameShape(QFrame.StyledPanel)
        self.bdayAge.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.bdayAge)
        self.horizontalLayout_22.setSpacing(35)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(5, 0, 5, 5)
        self.Bday = QDateEdit(self.bdayAge)
        self.Bday.setObjectName(u"Bday")
        sizePolicy.setHeightForWidth(self.Bday.sizePolicy().hasHeightForWidth())
        self.Bday.setSizePolicy(sizePolicy)
        self.Bday.setMinimumSize(QSize(174, 45))
        self.Bday.setReadOnly(True)
        self.Bday.setCalendarPopup(True)

        self.horizontalLayout_22.addWidget(self.Bday)

        self.age = QLineEdit(self.bdayAge)
        self.age.setObjectName(u"age")
        sizePolicy.setHeightForWidth(self.age.sizePolicy().hasHeightForWidth())
        self.age.setSizePolicy(sizePolicy)
        self.age.setMinimumSize(QSize(174, 45))
        self.age.setStyleSheet(u"")

        self.horizontalLayout_22.addWidget(self.age)


        self.verticalLayout_30.addWidget(self.bdayAge)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_30.addItem(self.verticalSpacer_3)

        self.frame_7 = QFrame(self.petDetailsPage)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QSize(0, 50))
        self.frame_7.setMaximumSize(QSize(16777215, 80))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_29.setSpacing(35)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(5, 0, 5, 5)
        self.petSexComboBox = QComboBox(self.frame_7)
        self.petSexComboBox.addItem("")
        self.petSexComboBox.addItem("")
        self.petSexComboBox.addItem("")
        self.petSexComboBox.setObjectName(u"petSexComboBox")
        sizePolicy.setHeightForWidth(self.petSexComboBox.sizePolicy().hasHeightForWidth())
        self.petSexComboBox.setSizePolicy(sizePolicy)
        self.petSexComboBox.setMinimumSize(QSize(174, 45))
        self.petSexComboBox.setStyleSheet(u"")

        self.horizontalLayout_29.addWidget(self.petSexComboBox)

        self.petRemarks = QLineEdit(self.frame_7)
        self.petRemarks.setObjectName(u"petRemarks")
        sizePolicy.setHeightForWidth(self.petRemarks.sizePolicy().hasHeightForWidth())
        self.petRemarks.setSizePolicy(sizePolicy)
        self.petRemarks.setMinimumSize(QSize(174, 45))
        self.petRemarks.setStyleSheet(u"")

        self.horizontalLayout_29.addWidget(self.petRemarks)


        self.verticalLayout_30.addWidget(self.frame_7)

        self.verticalSpacer_4 = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_30.addItem(self.verticalSpacer_4)

        self.actionBtns = QFrame(self.petDetailsPage)
        self.actionBtns.setObjectName(u"actionBtns")
        self.actionBtns.setMinimumSize(QSize(0, 65))
        self.actionBtns.setFrameShape(QFrame.StyledPanel)
        self.actionBtns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.actionBtns)
        self.horizontalLayout_20.setSpacing(10)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 0, -1, 0)
        self.backBtn = QPushButton(self.actionBtns)
        self.backBtn.setObjectName(u"backBtn")
        self.backBtn.setMinimumSize(QSize(174, 45))
        self.backBtn.setMaximumSize(QSize(174, 16777215))
        self.backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.backBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:	rgb(220, 90, 90);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"\n"
"}")

        self.horizontalLayout_20.addWidget(self.backBtn)

        self.petConfirmButton = QPushButton(self.actionBtns)
        self.petConfirmButton.setObjectName(u"petConfirmButton")
        self.petConfirmButton.setMinimumSize(QSize(174, 45))
        self.petConfirmButton.setMaximumSize(QSize(174, 16777215))
        self.petConfirmButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.petConfirmButton.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.horizontalLayout_20.addWidget(self.petConfirmButton)

        self.petUpdateButton = QPushButton(self.actionBtns)
        self.petUpdateButton.setObjectName(u"petUpdateButton")
        self.petUpdateButton.setMinimumSize(QSize(174, 45))
        self.petUpdateButton.setMaximumSize(QSize(174, 16777215))
        self.petUpdateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.petUpdateButton.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.horizontalLayout_20.addWidget(self.petUpdateButton)


        self.verticalLayout_30.addWidget(self.actionBtns, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.profileStackedWidget.addWidget(self.petDetailsPage)

        self.verticalLayout_14.addWidget(self.profileStackedWidget)

        self.stackedWidget.addWidget(self.PatientProfile)
        self.petProfile = QWidget()
        self.petProfile.setObjectName(u"petProfile")
        self.verticalLayout_49 = QVBoxLayout(self.petProfile)
        self.verticalLayout_49.setSpacing(0)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.verticalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.frame_49 = QFrame(self.petProfile)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setStyleSheet(u"background:transparent;")
        self.frame_49.setFrameShape(QFrame.StyledPanel)
        self.frame_49.setFrameShadow(QFrame.Raised)
        self.verticalLayout_51 = QVBoxLayout(self.frame_49)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.petProfileBackBtn = QToolButton(self.frame_49)
        self.petProfileBackBtn.setObjectName(u"petProfileBackBtn")
        self.petProfileBackBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.petProfileBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.petProfileBackBtn.setIcon(icon10)

        self.verticalLayout_51.addWidget(self.petProfileBackBtn)

        self.frame_14 = QFrame(self.frame_49)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy4.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy4)
        self.frame_14.setMaximumSize(QSize(16777215, 296))
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.petProfileCard = QFrame(self.frame_14)
        self.petProfileCard.setObjectName(u"petProfileCard")
        self.petProfileCard.setStyleSheet(u"#petProfileCard{\n"
"	border-radius:10px;\n"
"	background-color:rgb(244, 244, 244);\n"
"}")
        self.petProfileCard.setFrameShape(QFrame.StyledPanel)
        self.petProfileCard.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.petProfileCard)
        self.horizontalLayout_42.setSpacing(40)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(30, -1, -1, -1)
        self.frame_19 = QFrame(self.petProfileCard)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_19)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 50)
        self.frame_17 = QFrame(self.frame_19)
        self.frame_17.setObjectName(u"frame_17")
        sizePolicy5.setHeightForWidth(self.frame_17.sizePolicy().hasHeightForWidth())
        self.frame_17.setSizePolicy(sizePolicy5)
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.reminderBtn = QPushButton(self.frame_17)
        self.reminderBtn.setObjectName(u"reminderBtn")
        sizePolicy.setHeightForWidth(self.reminderBtn.sizePolicy().hasHeightForWidth())
        self.reminderBtn.setSizePolicy(sizePolicy)
        self.reminderBtn.setMinimumSize(QSize(40, 40))
        self.reminderBtn.setMaximumSize(QSize(40, 40))
        self.reminderBtn.setStyleSheet(u"")
        icon15 = QIcon()
        icon15.addFile(u":/Icons/Icons/checklist.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.reminderBtn.setIcon(icon15)
        self.reminderBtn.setIconSize(QSize(30, 30))

        self.horizontalLayout_40.addWidget(self.reminderBtn, 0, Qt.AlignLeft)


        self.verticalLayout_27.addWidget(self.frame_17, 0, Qt.AlignTop)

        self.frame_18 = QFrame(self.frame_19)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_18)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.petProfileIcon = QLabel(self.frame_18)
        self.petProfileIcon.setObjectName(u"petProfileIcon")
        self.petProfileIcon.setMaximumSize(QSize(120, 120))
        self.petProfileIcon.setPixmap(QPixmap(u":/Icons/Icons/catIcon.png"))
        self.petProfileIcon.setScaledContents(True)
        self.petProfileIcon.setAlignment(Qt.AlignCenter)
        self.petProfileIcon.setMargin(0)

        self.verticalLayout_26.addWidget(self.petProfileIcon)


        self.verticalLayout_27.addWidget(self.frame_18)


        self.horizontalLayout_42.addWidget(self.frame_19, 0, Qt.AlignLeft)

        self.frame_52 = QFrame(self.petProfileCard)
        self.frame_52.setObjectName(u"frame_52")
        sizePolicy4.setHeightForWidth(self.frame_52.sizePolicy().hasHeightForWidth())
        self.frame_52.setSizePolicy(sizePolicy4)
        self.frame_52.setStyleSheet(u"background:transparent;\n"
"border:none;")
        self.frame_52.setFrameShape(QFrame.StyledPanel)
        self.frame_52.setFrameShadow(QFrame.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_52)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.frame_55 = QFrame(self.frame_52)
        self.frame_55.setObjectName(u"frame_55")
        sizePolicy2.setHeightForWidth(self.frame_55.sizePolicy().hasHeightForWidth())
        self.frame_55.setSizePolicy(sizePolicy2)
        self.frame_55.setStyleSheet(u"background:transparent;\n"
"border:none;")
        self.frame_55.setFrameShape(QFrame.StyledPanel)
        self.frame_55.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_55)
        self.horizontalLayout_57.setSpacing(0)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_25.addWidget(self.frame_55)

        self.frame_16 = QFrame(self.frame_52)
        self.frame_16.setObjectName(u"frame_16")
        sizePolicy4.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy4)
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.horizontalLayout_41.setContentsMargins(0, 15, 0, 15)
        self.frame_11 = QFrame(self.frame_16)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setStyleSheet(u"font: 63 13pt \"Montserrat SemiBold\";\n"
"color:rgb(0, 0, 0);")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_11)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_20 = QFrame(self.frame_11)
        self.frame_20.setObjectName(u"frame_20")
        sizePolicy.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy)
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_43 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_20)
        self.label_6.setObjectName(u"label_6")
        sizePolicy5.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy5)
        self.label_6.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_43.addWidget(self.label_6)

        self.petProfileNameLabel = QLabel(self.frame_20)
        self.petProfileNameLabel.setObjectName(u"petProfileNameLabel")
        sizePolicy.setHeightForWidth(self.petProfileNameLabel.sizePolicy().hasHeightForWidth())
        self.petProfileNameLabel.setSizePolicy(sizePolicy)
        self.petProfileNameLabel.setStyleSheet(u"")
        self.petProfileNameLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.petProfileNameLabel.setWordWrap(True)

        self.horizontalLayout_43.addWidget(self.petProfileNameLabel)


        self.verticalLayout_21.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_11)
        self.frame_21.setObjectName(u"frame_21")
        sizePolicy.setHeightForWidth(self.frame_21.sizePolicy().hasHeightForWidth())
        self.frame_21.setSizePolicy(sizePolicy)
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_21)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_44.addWidget(self.label_11)

        self.breedLabel = QLabel(self.frame_21)
        self.breedLabel.setObjectName(u"breedLabel")
        sizePolicy.setHeightForWidth(self.breedLabel.sizePolicy().hasHeightForWidth())
        self.breedLabel.setSizePolicy(sizePolicy)
        self.breedLabel.setStyleSheet(u"")
        self.breedLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.breedLabel.setWordWrap(True)

        self.horizontalLayout_44.addWidget(self.breedLabel)


        self.verticalLayout_21.addWidget(self.frame_21)

        self.frame_33 = QFrame(self.frame_11)
        self.frame_33.setObjectName(u"frame_33")
        sizePolicy.setHeightForWidth(self.frame_33.sizePolicy().hasHeightForWidth())
        self.frame_33.setSizePolicy(sizePolicy)
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_49 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.frame_33)
        self.label_18.setObjectName(u"label_18")
        sizePolicy5.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy5)
        self.label_18.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_49.addWidget(self.label_18)

        self.petRemarksLabel = QLabel(self.frame_33)
        self.petRemarksLabel.setObjectName(u"petRemarksLabel")
        sizePolicy.setHeightForWidth(self.petRemarksLabel.sizePolicy().hasHeightForWidth())
        self.petRemarksLabel.setSizePolicy(sizePolicy)
        self.petRemarksLabel.setWordWrap(True)

        self.horizontalLayout_49.addWidget(self.petRemarksLabel)


        self.verticalLayout_21.addWidget(self.frame_33)

        self.frame_31 = QFrame(self.frame_11)
        self.frame_31.setObjectName(u"frame_31")
        sizePolicy4.setHeightForWidth(self.frame_31.sizePolicy().hasHeightForWidth())
        self.frame_31.setSizePolicy(sizePolicy4)
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.frame_31)
        self.label_16.setObjectName(u"label_16")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy11)
        self.label_16.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_46.addWidget(self.label_16)

        self.petBirthdayOptional = QLabel(self.frame_31)
        self.petBirthdayOptional.setObjectName(u"petBirthdayOptional")
        sizePolicy4.setHeightForWidth(self.petBirthdayOptional.sizePolicy().hasHeightForWidth())
        self.petBirthdayOptional.setSizePolicy(sizePolicy4)

        self.horizontalLayout_46.addWidget(self.petBirthdayOptional)


        self.verticalLayout_21.addWidget(self.frame_31)

        self.frame_56 = QFrame(self.frame_11)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setFrameShape(QFrame.StyledPanel)
        self.frame_56.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_80 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_80.setSpacing(0)
        self.horizontalLayout_80.setObjectName(u"horizontalLayout_80")
        self.horizontalLayout_80.setContentsMargins(0, 0, 0, 0)
        self.petProfileEditBtn = QToolButton(self.frame_56)
        self.petProfileEditBtn.setObjectName(u"petProfileEditBtn")
        self.petProfileEditBtn.setStyleSheet(u"\n"
"\n"
"#petProfileEditBtn{\n"
"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);\n"
"background:transparent;\n"
"}\n"
"#petProfileEditBtn:hover{\n"
"color:rgb(98, 98, 98);\n"
"\n"
"\n"
"}")
        icon16 = QIcon()
        icon16.addFile(u":/Icons/Icons/editPeDetails.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.petProfileEditBtn.setIcon(icon16)
        self.petProfileEditBtn.setIconSize(QSize(25, 25))
        self.petProfileEditBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_80.addWidget(self.petProfileEditBtn)


        self.verticalLayout_21.addWidget(self.frame_56, 0, Qt.AlignLeft)


        self.horizontalLayout_41.addWidget(self.frame_11)

        self.frame_15 = QFrame(self.frame_16)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy)
        self.frame_15.setStyleSheet(u"font: 63 13pt \"Montserrat SemiBold\";\n"
"color:rgb(0, 0, 0);")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_15)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.frame_15)
        self.frame_32.setObjectName(u"frame_32")
        sizePolicy4.setHeightForWidth(self.frame_32.sizePolicy().hasHeightForWidth())
        self.frame_32.setSizePolicy(sizePolicy4)
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_48 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.frame_32)
        self.label_17.setObjectName(u"label_17")
        sizePolicy11.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy11)
        self.label_17.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_48.addWidget(self.label_17)

        self.petColorLabel = QLabel(self.frame_32)
        self.petColorLabel.setObjectName(u"petColorLabel")
        sizePolicy4.setHeightForWidth(self.petColorLabel.sizePolicy().hasHeightForWidth())
        self.petColorLabel.setSizePolicy(sizePolicy4)
        self.petColorLabel.setStyleSheet(u"")
        self.petColorLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.petColorLabel.setWordWrap(True)

        self.horizontalLayout_48.addWidget(self.petColorLabel)


        self.verticalLayout_22.addWidget(self.frame_32)

        self.frame_30 = QFrame(self.frame_15)
        self.frame_30.setObjectName(u"frame_30")
        sizePolicy4.setHeightForWidth(self.frame_30.sizePolicy().hasHeightForWidth())
        self.frame_30.setSizePolicy(sizePolicy4)
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_30)
        self.label_14.setObjectName(u"label_14")
        sizePolicy11.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy11)
        self.label_14.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_45.addWidget(self.label_14)

        self.speciesLabel = QLabel(self.frame_30)
        self.speciesLabel.setObjectName(u"speciesLabel")
        sizePolicy4.setHeightForWidth(self.speciesLabel.sizePolicy().hasHeightForWidth())
        self.speciesLabel.setSizePolicy(sizePolicy4)
        self.speciesLabel.setStyleSheet(u"")
        self.speciesLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.speciesLabel.setWordWrap(True)

        self.horizontalLayout_45.addWidget(self.speciesLabel)


        self.verticalLayout_22.addWidget(self.frame_30)

        self.frame_34 = QFrame(self.frame_15)
        self.frame_34.setObjectName(u"frame_34")
        sizePolicy4.setHeightForWidth(self.frame_34.sizePolicy().hasHeightForWidth())
        self.frame_34.setSizePolicy(sizePolicy4)
        self.frame_34.setStyleSheet(u"")
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.horizontalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.frame_34)
        self.label_19.setObjectName(u"label_19")
        sizePolicy5.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy5)
        self.label_19.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_50.addWidget(self.label_19)

        self.petSexLabel = QLabel(self.frame_34)
        self.petSexLabel.setObjectName(u"petSexLabel")
        sizePolicy4.setHeightForWidth(self.petSexLabel.sizePolicy().hasHeightForWidth())
        self.petSexLabel.setSizePolicy(sizePolicy4)
        self.petSexLabel.setStyleSheet(u"")
        self.petSexLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.petSexLabel.setWordWrap(True)

        self.horizontalLayout_50.addWidget(self.petSexLabel)


        self.verticalLayout_22.addWidget(self.frame_34)

        self.frame_35 = QFrame(self.frame_15)
        self.frame_35.setObjectName(u"frame_35")
        sizePolicy4.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy4)
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_47 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalLayout_47.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.frame_35)
        self.label_20.setObjectName(u"label_20")
        sizePolicy11.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy11)
        self.label_20.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_47.addWidget(self.label_20)

        self.petAgeLabel = QLabel(self.frame_35)
        self.petAgeLabel.setObjectName(u"petAgeLabel")
        sizePolicy4.setHeightForWidth(self.petAgeLabel.sizePolicy().hasHeightForWidth())
        self.petAgeLabel.setSizePolicy(sizePolicy4)
        self.petAgeLabel.setStyleSheet(u"")
        self.petAgeLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.petAgeLabel.setWordWrap(True)

        self.horizontalLayout_47.addWidget(self.petAgeLabel)


        self.verticalLayout_22.addWidget(self.frame_35)

        self.frame_58 = QFrame(self.frame_15)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setFrameShape(QFrame.StyledPanel)
        self.frame_58.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_81 = QHBoxLayout(self.frame_58)
        self.horizontalLayout_81.setSpacing(0)
        self.horizontalLayout_81.setObjectName(u"horizontalLayout_81")
        self.horizontalLayout_81.setContentsMargins(0, 0, 0, 0)
        self.petProfileDeleteBtn = QToolButton(self.frame_58)
        self.petProfileDeleteBtn.setObjectName(u"petProfileDeleteBtn")
        self.petProfileDeleteBtn.setStyleSheet(u"\n"
"#petProfileDeleteBtn{\n"
"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);\n"
"background:transparent;\n"
"}\n"
"#petProfileDeleteBtn:hover{\n"
"color:rgb(98, 98, 98);\n"
"\n"
"}")
        icon17 = QIcon()
        icon17.addFile(u":/Icons/Icons/deleteBlack.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.petProfileDeleteBtn.setIcon(icon17)
        self.petProfileDeleteBtn.setIconSize(QSize(30, 30))
        self.petProfileDeleteBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_81.addWidget(self.petProfileDeleteBtn)


        self.verticalLayout_22.addWidget(self.frame_58, 0, Qt.AlignLeft)


        self.horizontalLayout_41.addWidget(self.frame_15)


        self.verticalLayout_25.addWidget(self.frame_16)

        self.frame_57 = QFrame(self.frame_52)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setStyleSheet(u"background:transparent;")
        self.frame_57.setFrameShape(QFrame.StyledPanel)
        self.frame_57.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_58.setSpacing(0)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.horizontalLayout_58.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_25.addWidget(self.frame_57)


        self.horizontalLayout_42.addWidget(self.frame_52)


        self.horizontalLayout_25.addWidget(self.petProfileCard)


        self.verticalLayout_51.addWidget(self.frame_14)

        self.frame_60 = QFrame(self.frame_49)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setMaximumSize(QSize(16777215, 70))
        self.frame_60.setFrameShape(QFrame.StyledPanel)
        self.frame_60.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_60.setSpacing(5)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.horizontalLayout_60.setContentsMargins(5, 0, 5, 10)
        self.serviceShadow = QFrame(self.frame_60)
        self.serviceShadow.setObjectName(u"serviceShadow")
        self.serviceShadow.setMaximumSize(QSize(16777215, 60))
        self.serviceShadow.setStyleSheet(u"border-radius: 5px;\n"
"border:none;")
        self.serviceShadow.setFrameShape(QFrame.StyledPanel)
        self.serviceShadow.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.serviceShadow)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.serviceHistoryBtn = QPushButton(self.serviceShadow)
        self.serviceHistoryBtn.setObjectName(u"serviceHistoryBtn")
        sizePolicy.setHeightForWidth(self.serviceHistoryBtn.sizePolicy().hasHeightForWidth())
        self.serviceHistoryBtn.setSizePolicy(sizePolicy)
        self.serviceHistoryBtn.setMaximumSize(QSize(16777215, 60))
        self.serviceHistoryBtn.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color:rgb(220, 220, 220);\n"
"    color: rgb(80, 80, 80);\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(252, 213, 151);   \n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);\n"
"	border: none;                        \n"
"}")

        self.horizontalLayout_27.addWidget(self.serviceHistoryBtn)


        self.horizontalLayout_60.addWidget(self.serviceShadow)

        self.addServiceShadow = QFrame(self.frame_60)
        self.addServiceShadow.setObjectName(u"addServiceShadow")
        self.addServiceShadow.setMaximumSize(QSize(16777215, 60))
        self.addServiceShadow.setStyleSheet(u"border-radius: 5px;\n"
"border:none;")
        self.addServiceShadow.setFrameShape(QFrame.StyledPanel)
        self.addServiceShadow.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.addServiceShadow)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.addNewServiceBtn = QPushButton(self.addServiceShadow)
        self.addNewServiceBtn.setObjectName(u"addNewServiceBtn")
        sizePolicy.setHeightForWidth(self.addNewServiceBtn.sizePolicy().hasHeightForWidth())
        self.addNewServiceBtn.setSizePolicy(sizePolicy)
        self.addNewServiceBtn.setMaximumSize(QSize(16777215, 60))
        self.addNewServiceBtn.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color:rgb(220, 220, 220);\n"
"    color: rgb(80, 80, 80);\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(252, 213, 151);   \n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);\n"
"	border: none;                        \n"
"}")

        self.horizontalLayout_28.addWidget(self.addNewServiceBtn)


        self.horizontalLayout_60.addWidget(self.addServiceShadow)


        self.verticalLayout_51.addWidget(self.frame_60)

        self.serviceHistoryStackedWidget = QStackedWidget(self.frame_49)
        self.serviceHistoryStackedWidget.setObjectName(u"serviceHistoryStackedWidget")
        self.serviceHistoryPage = QWidget()
        self.serviceHistoryPage.setObjectName(u"serviceHistoryPage")
        self.verticalLayout_50 = QVBoxLayout(self.serviceHistoryPage)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.verticalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.searchServiceFrame = QFrame(self.serviceHistoryPage)
        self.searchServiceFrame.setObjectName(u"searchServiceFrame")
        sizePolicy3.setHeightForWidth(self.searchServiceFrame.sizePolicy().hasHeightForWidth())
        self.searchServiceFrame.setSizePolicy(sizePolicy3)
        self.searchServiceFrame.setStyleSheet(u"#searchServiceFrame{\n"
"	border-radius:10px;\n"
"	border:none;\n"
"}\n"
"\n"
"")
        self.horizontalLayout_63 = QHBoxLayout(self.searchServiceFrame)
        self.horizontalLayout_63.setSpacing(0)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalLayout_63.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_63.setContentsMargins(0, 0, -1, 0)
        self.searchBar_3 = QLineEdit(self.searchServiceFrame)
        self.searchBar_3.setObjectName(u"searchBar_3")
        sizePolicy2.setHeightForWidth(self.searchBar_3.sizePolicy().hasHeightForWidth())
        self.searchBar_3.setSizePolicy(sizePolicy2)
        self.searchBar_3.setMinimumSize(QSize(234, 44))
        self.searchBar_3.setAutoFillBackground(False)
        self.searchBar_3.setStyleSheet(u"QLineEdit {\n"
"    background-color: #F0F0F0;\n"
"    border-top-left-radius: 10px;\n"
" 	border-bottom-left-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    padding-left: 15px;\n"
"    border: none;\n"
"}\n"
"")

        self.horizontalLayout_63.addWidget(self.searchBar_3, 0, Qt.AlignRight)

        self.searchButton_3 = QFrame(self.searchServiceFrame)
        self.searchButton_3.setObjectName(u"searchButton_3")
        sizePolicy11.setHeightForWidth(self.searchButton_3.sizePolicy().hasHeightForWidth())
        self.searchButton_3.setSizePolicy(sizePolicy11)
        self.searchButton_3.setStyleSheet(u"#searchButton_3{\n"
"background-color: #F0F0F0;\n"
"border-top-right-radius:10px;\n"
"border-bottom-right-radius:10px;\n"
"}\n"
"")
        self.searchButton_3.setFrameShape(QFrame.StyledPanel)
        self.searchButton_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_64 = QHBoxLayout(self.searchButton_3)
        self.horizontalLayout_64.setSpacing(9)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setContentsMargins(9, 9, 9, 9)
        self.searchIcon_3 = QLabel(self.searchButton_3)
        self.searchIcon_3.setObjectName(u"searchIcon_3")
        self.searchIcon_3.setMaximumSize(QSize(24, 24))
        self.searchIcon_3.setStyleSheet(u"")
        self.searchIcon_3.setPixmap(QPixmap(u":/Icons/Icons/searchIcon.png"))
        self.searchIcon_3.setScaledContents(True)

        self.horizontalLayout_64.addWidget(self.searchIcon_3)


        self.horizontalLayout_63.addWidget(self.searchButton_3)


        self.verticalLayout_50.addWidget(self.searchServiceFrame)

        self.serviceTableHeader = QFrame(self.serviceHistoryPage)
        self.serviceTableHeader.setObjectName(u"serviceTableHeader")
        self.serviceTableHeader.setStyleSheet(u"#serviceTableHeader{\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-bottom:2px solid rgb(115, 170, 194);\n"
"}\n"
"QFrame{\n"
"	color: rgb(48, 48, 48);\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"}")
        self.serviceTableHeader.setFrameShape(QFrame.StyledPanel)
        self.serviceTableHeader.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_74 = QHBoxLayout(self.serviceTableHeader)
        self.horizontalLayout_74.setObjectName(u"horizontalLayout_74")
        self.horizontalLayout_74.setContentsMargins(20, -1, 20, -1)
        self.label_157 = QLabel(self.serviceTableHeader)
        self.label_157.setObjectName(u"label_157")
        sizePolicy2.setHeightForWidth(self.label_157.sizePolicy().hasHeightForWidth())
        self.label_157.setSizePolicy(sizePolicy2)
        self.label_157.setStyleSheet(u"")

        self.horizontalLayout_74.addWidget(self.label_157)

        self.label_158 = QLabel(self.serviceTableHeader)
        self.label_158.setObjectName(u"label_158")
        sizePolicy2.setHeightForWidth(self.label_158.sizePolicy().hasHeightForWidth())
        self.label_158.setSizePolicy(sizePolicy2)
        self.label_158.setStyleSheet(u"")

        self.horizontalLayout_74.addWidget(self.label_158)

        self.label_159 = QLabel(self.serviceTableHeader)
        self.label_159.setObjectName(u"label_159")
        sizePolicy2.setHeightForWidth(self.label_159.sizePolicy().hasHeightForWidth())
        self.label_159.setSizePolicy(sizePolicy2)

        self.horizontalLayout_74.addWidget(self.label_159)

        self.label_160 = QLabel(self.serviceTableHeader)
        self.label_160.setObjectName(u"label_160")
        sizePolicy5.setHeightForWidth(self.label_160.sizePolicy().hasHeightForWidth())
        self.label_160.setSizePolicy(sizePolicy5)
        self.label_160.setStyleSheet(u"color:rgba(63, 63, 63, 0);")

        self.horizontalLayout_74.addWidget(self.label_160)

        self.printBtn = QPushButton(self.serviceTableHeader)
        self.printBtn.setObjectName(u"printBtn")
        sizePolicy5.setHeightForWidth(self.printBtn.sizePolicy().hasHeightForWidth())
        self.printBtn.setSizePolicy(sizePolicy5)
        self.printBtn.setStyleSheet(u"border:none;\n"
"background:none;")
        icon18 = QIcon()
        icon18.addFile(u":/Icons/Icons/printIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.printBtn.setIcon(icon18)
        self.printBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_74.addWidget(self.printBtn)


        self.verticalLayout_50.addWidget(self.serviceTableHeader)

        self.serviceHistoryScrollArea = QScrollArea(self.serviceHistoryPage)
        self.serviceHistoryScrollArea.setObjectName(u"serviceHistoryScrollArea")
        self.serviceHistoryScrollArea.setStyleSheet(u"#serviceHistoryScrollArea{\n"
"	border:none;\n"
"}\n"
"#serviceHistoryScrollArea QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#serviceHistoryScrollArea QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 120px;\n"
"	min-height: 200px;\n"
"}\n"
"\n"
"#serviceHistoryScrollArea QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"#serviceHistoryScrollArea QScrollBar::add-line:vertical,\n"
"#serviceHistoryScrollArea QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"#serviceHistoryScrollArea QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"    border-radius: 0px;\n"
"}\n"
"")
        self.serviceHistoryScrollArea.setWidgetResizable(True)
        self.serviceHistoryScrollPage = QWidget()
        self.serviceHistoryScrollPage.setObjectName(u"serviceHistoryScrollPage")
        self.serviceHistoryScrollPage.setGeometry(QRect(0, 0, 98, 33))
        self.verticalLayout_53 = QVBoxLayout(self.serviceHistoryScrollPage)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.verticalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.label_138 = QLabel(self.serviceHistoryScrollPage)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setStyleSheet(u"font: 81 16pt \"Montserrat ExtraBold\";\n"
"color:rgb(168, 168, 168);")

        self.verticalLayout_53.addWidget(self.label_138, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.serviceHistoryScrollArea.setWidget(self.serviceHistoryScrollPage)

        self.verticalLayout_50.addWidget(self.serviceHistoryScrollArea)

        self.serviceHistoryStackedWidget.addWidget(self.serviceHistoryPage)
        self.addNewServicePage = QWidget()
        self.addNewServicePage.setObjectName(u"addNewServicePage")
        self.verticalLayout_52 = QVBoxLayout(self.addNewServicePage)
        self.verticalLayout_52.setSpacing(0)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.verticalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.frame_61 = QFrame(self.addNewServicePage)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setStyleSheet(u"QDateEdit {\n"
"	background-color:rgb(245, 245, 245);\n"
"    border-radius: 10px;\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(52, 52, 52);\n"
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
"    border-radius: 10px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(52, 52, 52);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"    border: none; \n"
"}\n"
"QComboBox:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"QComboBox::drop-down {\n"
"    background-color: transparent;\n"
"    bor"
                        "der-radius: 10px;\n"
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
"    "
                        "border: none;\n"
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
"QComboBox QAbstractItemView QScrollBar::groove {\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QLineEdit {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"    color: rgb(39, 39, 39);\n"
"    border: none; /* optional para "
                        "di mag mukhang double border */\n"
"    background: transparent;\n"
"}")
        self.frame_61.setFrameShape(QFrame.StyledPanel)
        self.frame_61.setFrameShadow(QFrame.Raised)
        self.verticalLayout_56 = QVBoxLayout(self.frame_61)
        self.verticalLayout_56.setSpacing(0)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.verticalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.frame_62 = QFrame(self.frame_61)
        self.frame_62.setObjectName(u"frame_62")
        sizePolicy4.setHeightForWidth(self.frame_62.sizePolicy().hasHeightForWidth())
        self.frame_62.setSizePolicy(sizePolicy4)
        self.frame_62.setMaximumSize(QSize(16777215, 135))
        self.frame_62.setFrameShape(QFrame.StyledPanel)
        self.frame_62.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_62)
        self.horizontalLayout_61.setSpacing(35)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.horizontalLayout_61.setContentsMargins(-1, 0, 0, 5)
        self.frame_63 = QFrame(self.frame_62)
        self.frame_63.setObjectName(u"frame_63")
        sizePolicy.setHeightForWidth(self.frame_63.sizePolicy().hasHeightForWidth())
        self.frame_63.setSizePolicy(sizePolicy)
        self.frame_63.setStyleSheet(u"QFrame{\n"
"background-color: transparent;\n"
"}")
        self.frame_63.setFrameShape(QFrame.StyledPanel)
        self.frame_63.setFrameShadow(QFrame.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.frame_63)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_54.setContentsMargins(0, -1, -1, 9)
        self.label_137 = QLabel(self.frame_63)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);")

        self.verticalLayout_54.addWidget(self.label_137, 0, Qt.AlignTop)

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
        self.serviceTypeComboBox.addItem("")
        self.serviceTypeComboBox.setObjectName(u"serviceTypeComboBox")
        sizePolicy.setHeightForWidth(self.serviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.serviceTypeComboBox.setSizePolicy(sizePolicy)
        self.serviceTypeComboBox.setMinimumSize(QSize(174, 45))
        self.serviceTypeComboBox.setMaximumSize(QSize(16777215, 65))
        self.serviceTypeComboBox.setFocusPolicy(Qt.NoFocus)
        self.serviceTypeComboBox.setStyleSheet(u"")
        self.serviceTypeComboBox.setEditable(False)
        self.serviceTypeComboBox.setMaxVisibleItems(10)

        self.verticalLayout_54.addWidget(self.serviceTypeComboBox)


        self.horizontalLayout_61.addWidget(self.frame_63)

        self.frame_64 = QFrame(self.frame_62)
        self.frame_64.setObjectName(u"frame_64")
        sizePolicy.setHeightForWidth(self.frame_64.sizePolicy().hasHeightForWidth())
        self.frame_64.setSizePolicy(sizePolicy)
        self.frame_64.setStyleSheet(u"QFrame{\n"
"background-color: transparent;\n"
"}")
        self.frame_64.setFrameShape(QFrame.StyledPanel)
        self.frame_64.setFrameShadow(QFrame.Raised)
        self.verticalLayout_55 = QVBoxLayout(self.frame_64)
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.verticalLayout_55.setContentsMargins(0, -1, 5, 9)
        self.label_139 = QLabel(self.frame_64)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);")

        self.verticalLayout_55.addWidget(self.label_139, 0, Qt.AlignTop)

        self.dateEdit = QDateEdit(self.frame_64)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setMinimumSize(QSize(174, 45))
        self.dateEdit.setMaximumSize(QSize(16777215, 65))
        self.dateEdit.setStyleSheet(u"")
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setAccelerated(False)
        self.dateEdit.setCalendarPopup(True)

        self.verticalLayout_55.addWidget(self.dateEdit)


        self.horizontalLayout_61.addWidget(self.frame_64)


        self.verticalLayout_56.addWidget(self.frame_62)

        self.frame_65 = QFrame(self.frame_61)
        self.frame_65.setObjectName(u"frame_65")
        sizePolicy4.setHeightForWidth(self.frame_65.sizePolicy().hasHeightForWidth())
        self.frame_65.setSizePolicy(sizePolicy4)
        self.frame_65.setFrameShape(QFrame.StyledPanel)
        self.frame_65.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_65)
        self.horizontalLayout_62.setSpacing(35)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(0, 0, 0, -1)
        self.addNoteFrame = QFrame(self.frame_65)
        self.addNoteFrame.setObjectName(u"addNoteFrame")
        self.addNoteFrame.setFrameShape(QFrame.StyledPanel)
        self.addNoteFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_57 = QVBoxLayout(self.addNoteFrame)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.addNoteLabel = QLabel(self.addNoteFrame)
        self.addNoteLabel.setObjectName(u"addNoteLabel")
        self.addNoteLabel.setStyleSheet(u"font: 63 12pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_57.addWidget(self.addNoteLabel)

        self.addNoteLineEdit = QTextEdit(self.addNoteFrame)
        self.addNoteLineEdit.setObjectName(u"addNoteLineEdit")
        self.addNoteLineEdit.setStyleSheet(u"QTextEdit{\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	font-size:12pt;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QTextEdit:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"")
        self.addNoteLineEdit.setLineWrapMode(QTextEdit.WidgetWidth)

        self.verticalLayout_57.addWidget(self.addNoteLineEdit)


        self.horizontalLayout_62.addWidget(self.addNoteFrame)

        self.frame_67 = QFrame(self.frame_65)
        self.frame_67.setObjectName(u"frame_67")
        sizePolicy.setHeightForWidth(self.frame_67.sizePolicy().hasHeightForWidth())
        self.frame_67.setSizePolicy(sizePolicy)
        self.frame_67.setStyleSheet(u"border:none;")
        self.frame_67.setFrameShape(QFrame.StyledPanel)
        self.frame_67.setFrameShadow(QFrame.Raised)
        self.verticalLayout_58 = QVBoxLayout(self.frame_67)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.verticalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.frame_68 = QFrame(self.frame_67)
        self.frame_68.setObjectName(u"frame_68")
        sizePolicy4.setHeightForWidth(self.frame_68.sizePolicy().hasHeightForWidth())
        self.frame_68.setSizePolicy(sizePolicy4)
        self.frame_68.setFrameShape(QFrame.StyledPanel)
        self.frame_68.setFrameShadow(QFrame.Raised)
        self.verticalLayout_59 = QVBoxLayout(self.frame_68)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_59.setContentsMargins(5, 0, 5, 5)
        self.returnCheckBox = QCheckBox(self.frame_68)
        self.returnCheckBox.setObjectName(u"returnCheckBox")
        self.returnCheckBox.setStyleSheet(u"QCheckBox {\n"
"    font: 63 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    border: 1px solid rgb(120, 179, 206);\n"
"	border-radius:3px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"	background-color:rgb(120, 179, 206);\n"
"    image: url(:/Icons/Icons/checkBox.png); \n"
"    border: 1px solid rgb(104, 104, 104);\n"
"	border-radius:3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    background-color: rgb(120, 179, 206);\n"
"}\n"
"")
        self.returnCheckBox.setCheckable(True)
        self.returnCheckBox.setTristate(False)

        self.verticalLayout_59.addWidget(self.returnCheckBox)

        self.verticalSpacer_13 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_59.addItem(self.verticalSpacer_13)

        self.returnDateEdit = QDateEdit(self.frame_68)
        self.returnDateEdit.setObjectName(u"returnDateEdit")
        self.returnDateEdit.setEnabled(True)
        sizePolicy.setHeightForWidth(self.returnDateEdit.sizePolicy().hasHeightForWidth())
        self.returnDateEdit.setSizePolicy(sizePolicy)
        self.returnDateEdit.setMinimumSize(QSize(174, 45))
        self.returnDateEdit.setMaximumSize(QSize(16777215, 65))
        self.returnDateEdit.setStyleSheet(u"")
        self.returnDateEdit.setReadOnly(True)
        self.returnDateEdit.setCalendarPopup(True)

        self.verticalLayout_59.addWidget(self.returnDateEdit)

        self.returnDatePlaceholder = QLineEdit(self.frame_68)
        self.returnDatePlaceholder.setObjectName(u"returnDatePlaceholder")
        sizePolicy.setHeightForWidth(self.returnDatePlaceholder.sizePolicy().hasHeightForWidth())
        self.returnDatePlaceholder.setSizePolicy(sizePolicy)
        self.returnDatePlaceholder.setMinimumSize(QSize(174, 45))
        self.returnDatePlaceholder.setMaximumSize(QSize(16777215, 65))
        self.returnDatePlaceholder.setStyleSheet(u"QLineEdit{\n"
"    border-radius: 10px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(229, 229, 229);\n"
"}")

        self.verticalLayout_59.addWidget(self.returnDatePlaceholder)

        self.verticalSpacer_14 = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_59.addItem(self.verticalSpacer_14)


        self.verticalLayout_58.addWidget(self.frame_68)

        self.frame_66 = QFrame(self.frame_67)
        self.frame_66.setObjectName(u"frame_66")
        self.frame_66.setFrameShape(QFrame.StyledPanel)
        self.frame_66.setFrameShadow(QFrame.Raised)
        self.verticalLayout_60 = QVBoxLayout(self.frame_66)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.updateServiceBtn = QPushButton(self.frame_66)
        self.updateServiceBtn.setObjectName(u"updateServiceBtn")
        sizePolicy10.setHeightForWidth(self.updateServiceBtn.sizePolicy().hasHeightForWidth())
        self.updateServiceBtn.setSizePolicy(sizePolicy10)
        self.updateServiceBtn.setMinimumSize(QSize(174, 45))
        self.updateServiceBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.updateServiceBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.verticalLayout_60.addWidget(self.updateServiceBtn)

        self.addServiceBtn = QPushButton(self.frame_66)
        self.addServiceBtn.setObjectName(u"addServiceBtn")
        sizePolicy10.setHeightForWidth(self.addServiceBtn.sizePolicy().hasHeightForWidth())
        self.addServiceBtn.setSizePolicy(sizePolicy10)
        self.addServiceBtn.setMinimumSize(QSize(174, 45))
        self.addServiceBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addServiceBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color:rgb(129, 191, 218);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}")

        self.verticalLayout_60.addWidget(self.addServiceBtn)

        self.cancelAddServiceBtn = QPushButton(self.frame_66)
        self.cancelAddServiceBtn.setObjectName(u"cancelAddServiceBtn")
        self.cancelAddServiceBtn.setMinimumSize(QSize(174, 45))
        self.cancelAddServiceBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancelAddServiceBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color:	rgb(220, 90, 90);\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"\n"
"}")

        self.verticalLayout_60.addWidget(self.cancelAddServiceBtn)


        self.verticalLayout_58.addWidget(self.frame_66, 0, Qt.AlignTop)


        self.horizontalLayout_62.addWidget(self.frame_67)


        self.verticalLayout_56.addWidget(self.frame_65)


        self.verticalLayout_52.addWidget(self.frame_61)

        self.serviceHistoryStackedWidget.addWidget(self.addNewServicePage)

        self.verticalLayout_51.addWidget(self.serviceHistoryStackedWidget)


        self.verticalLayout_49.addWidget(self.frame_49)

        self.stackedWidget.addWidget(self.petProfile)
        self.webAppReview = QWidget()
        self.webAppReview.setObjectName(u"webAppReview")
        self.verticalLayout_61 = QVBoxLayout(self.webAppReview)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.reviewWebAppointment = QFrame(self.webAppReview)
        self.reviewWebAppointment.setObjectName(u"reviewWebAppointment")
        self.reviewWebAppointment.setStyleSheet(u"background:transparent;")
        self.reviewWebAppointment.setFrameShape(QFrame.StyledPanel)
        self.reviewWebAppointment.setFrameShadow(QFrame.Raised)
        self.verticalLayout_45 = QVBoxLayout(self.reviewWebAppointment)
        self.verticalLayout_45.setSpacing(0)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.ReviewBackBtn = QPushButton(self.reviewWebAppointment)
        self.ReviewBackBtn.setObjectName(u"ReviewBackBtn")
        sizePolicy5.setHeightForWidth(self.ReviewBackBtn.sizePolicy().hasHeightForWidth())
        self.ReviewBackBtn.setSizePolicy(sizePolicy5)
        self.ReviewBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.ReviewBackBtn.setIcon(icon10)

        self.verticalLayout_45.addWidget(self.ReviewBackBtn)

        self.frame_24 = QFrame(self.reviewWebAppointment)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"}")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.pageHeader5 = QLabel(self.frame_24)
        self.pageHeader5.setObjectName(u"pageHeader5")
        sizePolicy3.setHeightForWidth(self.pageHeader5.sizePolicy().hasHeightForWidth())
        self.pageHeader5.setSizePolicy(sizePolicy3)
        self.pageHeader5.setStyleSheet(u"")

        self.horizontalLayout_35.addWidget(self.pageHeader5)

        self.clinicIconP5 = QLabel(self.frame_24)
        self.clinicIconP5.setObjectName(u"clinicIconP5")
        self.clinicIconP5.setMaximumSize(QSize(145, 60))
        self.clinicIconP5.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP5.setScaledContents(True)
        self.clinicIconP5.setAlignment(Qt.AlignCenter)
        self.clinicIconP5.setWordWrap(False)

        self.horizontalLayout_35.addWidget(self.clinicIconP5)


        self.verticalLayout_45.addWidget(self.frame_24)

        self.reviewWeb = QFrame(self.reviewWebAppointment)
        self.reviewWeb.setObjectName(u"reviewWeb")
        sizePolicy4.setHeightForWidth(self.reviewWeb.sizePolicy().hasHeightForWidth())
        self.reviewWeb.setSizePolicy(sizePolicy4)
        self.reviewWeb.setStyleSheet(u"")
        self.reviewWeb.setFrameShape(QFrame.StyledPanel)
        self.reviewWeb.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.reviewWeb)
        self.verticalLayout_18.setSpacing(20)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(20, -1, 20, -1)
        self.reviewClient = QFrame(self.reviewWeb)
        self.reviewClient.setObjectName(u"reviewClient")
        sizePolicy3.setHeightForWidth(self.reviewClient.sizePolicy().hasHeightForWidth())
        self.reviewClient.setSizePolicy(sizePolicy3)
        self.reviewClient.setStyleSheet(u"#reviewClient{\n"
"	border-radius:10px;\n"
"	background-color:rgb(244, 244, 244);\n"
"}")
        self.reviewClient.setFrameShape(QFrame.StyledPanel)
        self.reviewClient.setFrameShadow(QFrame.Raised)
        self.verticalLayout_46 = QVBoxLayout(self.reviewClient)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_46.setContentsMargins(-1, 17, -1, 17)
        self.frame_3 = QFrame(self.reviewClient)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_53 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(80, 80))
        self.label_13.setMaximumSize(QSize(80, 80))
        self.label_13.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.label_13.setScaledContents(True)

        self.horizontalLayout_53.addWidget(self.label_13)

        self.reviewFullname = QLabel(self.frame_3)
        self.reviewFullname.setObjectName(u"reviewFullname")
        self.reviewFullname.setStyleSheet(u"font: 87 14pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_53.addWidget(self.reviewFullname)

        self.frame_41 = QFrame(self.frame_3)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setStyleSheet(u"background-color:rgb(128, 190, 217);\n"
"border-radius:5px;\n"
"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(20, 5, 20, 5)
        self.label_31 = QLabel(self.frame_41)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_66.addWidget(self.label_31)

        self.BookingId = QLabel(self.frame_41)
        self.BookingId.setObjectName(u"BookingId")
        self.BookingId.setStyleSheet(u"")

        self.horizontalLayout_66.addWidget(self.BookingId, 0, Qt.AlignTop)


        self.horizontalLayout_53.addWidget(self.frame_41, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_46.addWidget(self.frame_3)

        self.frame_23 = QFrame(self.reviewClient)
        self.frame_23.setObjectName(u"frame_23")
        sizePolicy4.setHeightForWidth(self.frame_23.sizePolicy().hasHeightForWidth())
        self.frame_23.setSizePolicy(sizePolicy4)
        self.frame_23.setStyleSheet(u"font: 57 13pt \"Montserrat Medium\";\n"
"color:rgb(52, 52, 52);")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.verticalLayout_63 = QVBoxLayout(self.frame_23)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.frame_38 = QFrame(self.frame_23)
        self.frame_38.setObjectName(u"frame_38")
        sizePolicy4.setHeightForWidth(self.frame_38.sizePolicy().hasHeightForWidth())
        self.frame_38.setSizePolicy(sizePolicy4)
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_38)
        self.horizontalLayout_55.setSpacing(6)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_38)
        self.label_2.setObjectName(u"label_2")
        sizePolicy11.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy11)
        self.label_2.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_55.addWidget(self.label_2)

        self.reviewEmail = QLabel(self.frame_38)
        self.reviewEmail.setObjectName(u"reviewEmail")
        self.reviewEmail.setStyleSheet(u"")

        self.horizontalLayout_55.addWidget(self.reviewEmail)

        self.label_3 = QLabel(self.frame_38)
        self.label_3.setObjectName(u"label_3")
        sizePolicy11.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy11)
        self.label_3.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_55.addWidget(self.label_3)

        self.reviewPhoneNo = QLabel(self.frame_38)
        self.reviewPhoneNo.setObjectName(u"reviewPhoneNo")
        self.reviewPhoneNo.setStyleSheet(u"")

        self.horizontalLayout_55.addWidget(self.reviewPhoneNo)


        self.verticalLayout_63.addWidget(self.frame_38)

        self.frame_39 = QFrame(self.frame_23)
        self.frame_39.setObjectName(u"frame_39")
        sizePolicy4.setHeightForWidth(self.frame_39.sizePolicy().hasHeightForWidth())
        self.frame_39.setSizePolicy(sizePolicy4)
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_39)
        self.label_5.setObjectName(u"label_5")
        sizePolicy11.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy11)
        self.label_5.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_56.addWidget(self.label_5)

        self.reviewAddress = QLabel(self.frame_39)
        self.reviewAddress.setObjectName(u"reviewAddress")
        self.reviewAddress.setStyleSheet(u"")

        self.horizontalLayout_56.addWidget(self.reviewAddress)


        self.verticalLayout_63.addWidget(self.frame_39)

        self.frame_40 = QFrame(self.frame_23)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame_40)
        self.label_12.setObjectName(u"label_12")
        sizePolicy11.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy11)
        self.label_12.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_36.addWidget(self.label_12)

        self.reviewDetailedAddress = QLabel(self.frame_40)
        self.reviewDetailedAddress.setObjectName(u"reviewDetailedAddress")

        self.horizontalLayout_36.addWidget(self.reviewDetailedAddress)


        self.verticalLayout_63.addWidget(self.frame_40)


        self.verticalLayout_46.addWidget(self.frame_23)


        self.verticalLayout_18.addWidget(self.reviewClient)

        self.reviewPet = QFrame(self.reviewWeb)
        self.reviewPet.setObjectName(u"reviewPet")
        sizePolicy3.setHeightForWidth(self.reviewPet.sizePolicy().hasHeightForWidth())
        self.reviewPet.setSizePolicy(sizePolicy3)
        self.reviewPet.setStyleSheet(u"#reviewPet{\n"
"	border-radius:10px;\n"
"	background-color:rgb(244, 244, 244);\n"
"}")
        self.reviewPet.setFrameShape(QFrame.StyledPanel)
        self.reviewPet.setFrameShadow(QFrame.Raised)
        self.verticalLayout_47 = QVBoxLayout(self.reviewPet)
        self.verticalLayout_47.setSpacing(0)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(-1, 17, -1, 17)
        self.frame_37 = QFrame(self.reviewPet)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_54 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.ReviewPetIcon = QLabel(self.frame_37)
        self.ReviewPetIcon.setObjectName(u"ReviewPetIcon")
        self.ReviewPetIcon.setMaximumSize(QSize(80, 80))
        self.ReviewPetIcon.setPixmap(QPixmap(u":/Icons/Icons/catIcon.png"))
        self.ReviewPetIcon.setScaledContents(True)

        self.horizontalLayout_54.addWidget(self.ReviewPetIcon)

        self.reviewPetName = QLabel(self.frame_37)
        self.reviewPetName.setObjectName(u"reviewPetName")
        self.reviewPetName.setStyleSheet(u"font: 87 14pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_54.addWidget(self.reviewPetName)


        self.verticalLayout_47.addWidget(self.frame_37)

        self.frame_26 = QFrame(self.reviewPet)
        self.frame_26.setObjectName(u"frame_26")
        sizePolicy4.setHeightForWidth(self.frame_26.sizePolicy().hasHeightForWidth())
        self.frame_26.setSizePolicy(sizePolicy4)
        self.frame_26.setStyleSheet(u"font: 57 13pt \"Montserrat Medium\";\n"
"color:rgb(52, 52, 52);")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_70 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_70.setSpacing(0)
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.horizontalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.frame_42 = QFrame(self.frame_26)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.verticalLayout_62 = QVBoxLayout(self.frame_42)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.verticalLayout_62.setContentsMargins(-1, 0, 0, 0)
        self.frame_43 = QFrame(self.frame_42)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.horizontalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.frame_43)
        self.label_21.setObjectName(u"label_21")
        sizePolicy11.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy11)
        self.label_21.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_68.addWidget(self.label_21)

        self.reviewSpecies = QLabel(self.frame_43)
        self.reviewSpecies.setObjectName(u"reviewSpecies")
        self.reviewSpecies.setStyleSheet(u"")

        self.horizontalLayout_68.addWidget(self.reviewSpecies)


        self.verticalLayout_62.addWidget(self.frame_43)

        self.frame_44 = QFrame(self.frame_42)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_69 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.horizontalLayout_69.setContentsMargins(0, 0, -1, 0)
        self.label_28 = QLabel(self.frame_44)
        self.label_28.setObjectName(u"label_28")
        sizePolicy11.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy11)
        self.label_28.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_69.addWidget(self.label_28)

        self.reviewSex = QLabel(self.frame_44)
        self.reviewSex.setObjectName(u"reviewSex")

        self.horizontalLayout_69.addWidget(self.reviewSex)


        self.verticalLayout_62.addWidget(self.frame_44)

        self.frame_45 = QFrame(self.frame_42)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setFrameShape(QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.horizontalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.frame_45)
        self.label_25.setObjectName(u"label_25")
        sizePolicy11.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy11)
        self.label_25.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_67.addWidget(self.label_25)

        self.reviewService = QLabel(self.frame_45)
        self.reviewService.setObjectName(u"reviewService")
        self.reviewService.setStyleSheet(u"")

        self.horizontalLayout_67.addWidget(self.reviewService)


        self.verticalLayout_62.addWidget(self.frame_45)

        self.frame_46 = QFrame(self.frame_42)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setFrameShape(QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.horizontalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.frame_46)
        self.label_23.setObjectName(u"label_23")
        sizePolicy11.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy11)
        self.label_23.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_59.addWidget(self.label_23)

        self.reviewDoctor = QLabel(self.frame_46)
        self.reviewDoctor.setObjectName(u"reviewDoctor")
        self.reviewDoctor.setStyleSheet(u"")

        self.horizontalLayout_59.addWidget(self.reviewDoctor)


        self.verticalLayout_62.addWidget(self.frame_46)


        self.horizontalLayout_70.addWidget(self.frame_42)

        self.frame_47 = QFrame(self.frame_26)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setFrameShape(QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.frame_47)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.verticalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.frame_25 = QFrame(self.frame_47)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.label_22 = QLabel(self.frame_25)
        self.label_22.setObjectName(u"label_22")
        sizePolicy11.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy11)
        self.label_22.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_34.addWidget(self.label_22)

        self.reviewBreed = QLabel(self.frame_25)
        self.reviewBreed.setObjectName(u"reviewBreed")
        self.reviewBreed.setStyleSheet(u"")

        self.horizontalLayout_34.addWidget(self.reviewBreed)


        self.verticalLayout_64.addWidget(self.frame_25)

        self.frame_27 = QFrame(self.frame_47)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.label_24 = QLabel(self.frame_27)
        self.label_24.setObjectName(u"label_24")
        sizePolicy11.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy11)
        self.label_24.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_37.addWidget(self.label_24)

        self.reviewColor = QLabel(self.frame_27)
        self.reviewColor.setObjectName(u"reviewColor")
        self.reviewColor.setStyleSheet(u"")

        self.horizontalLayout_37.addWidget(self.reviewColor)


        self.verticalLayout_64.addWidget(self.frame_27)

        self.frame_29 = QFrame(self.frame_47)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.frame_29)
        self.label_26.setObjectName(u"label_26")
        sizePolicy11.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy11)
        self.label_26.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_39.addWidget(self.label_26)

        self.reviewDate = QLabel(self.frame_29)
        self.reviewDate.setObjectName(u"reviewDate")
        self.reviewDate.setStyleSheet(u"")

        self.horizontalLayout_39.addWidget(self.reviewDate)


        self.verticalLayout_64.addWidget(self.frame_29)

        self.frame_28 = QFrame(self.frame_47)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.label_32 = QLabel(self.frame_28)
        self.label_32.setObjectName(u"label_32")
        sizePolicy11.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy11)
        self.label_32.setStyleSheet(u"font: 87 13pt \"Montserrat Black\";\n"
"color:rgb(52, 52, 52);")

        self.horizontalLayout_38.addWidget(self.label_32)

        self.reviewTime = QLabel(self.frame_28)
        self.reviewTime.setObjectName(u"reviewTime")

        self.horizontalLayout_38.addWidget(self.reviewTime)


        self.verticalLayout_64.addWidget(self.frame_28)


        self.horizontalLayout_70.addWidget(self.frame_47)


        self.verticalLayout_47.addWidget(self.frame_26)


        self.verticalLayout_18.addWidget(self.reviewPet)


        self.verticalLayout_45.addWidget(self.reviewWeb)

        self.AcceptDeclineFrame = QFrame(self.reviewWebAppointment)
        self.AcceptDeclineFrame.setObjectName(u"AcceptDeclineFrame")
        self.AcceptDeclineFrame.setStyleSheet(u"QPushButton{\n"
"	font: 63 14pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color: #81BFDA;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(117, 173, 197);\n"
"	border-radius: 10px;\n"
"}")
        self.AcceptDeclineFrame.setFrameShape(QFrame.StyledPanel)
        self.AcceptDeclineFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.AcceptDeclineFrame)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(20, -1, 20, -1)
        self.acceptAppointmentBtn = QPushButton(self.AcceptDeclineFrame)
        self.acceptAppointmentBtn.setObjectName(u"acceptAppointmentBtn")
        self.acceptAppointmentBtn.setMinimumSize(QSize(260, 0))

        self.horizontalLayout_33.addWidget(self.acceptAppointmentBtn)

        self.declineAppointmentBtn = QPushButton(self.AcceptDeclineFrame)
        self.declineAppointmentBtn.setObjectName(u"declineAppointmentBtn")
        self.declineAppointmentBtn.setMinimumSize(QSize(260, 0))
        self.declineAppointmentBtn.setStyleSheet(u"QPushButton{\n"
"	background-color: #FCD597;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"border-radius: 10px;\n"
"}")

        self.horizontalLayout_33.addWidget(self.declineAppointmentBtn)


        self.verticalLayout_45.addWidget(self.AcceptDeclineFrame, 0, Qt.AlignHCenter)


        self.verticalLayout_61.addWidget(self.reviewWebAppointment)

        self.stackedWidget.addWidget(self.webAppReview)
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.settings.setStyleSheet(u"QWidget{\n"
"	background:transparent;\n"
"\n"
"}")
        self.verticalLayout_15 = QVBoxLayout(self.settings)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_73 = QFrame(self.settings)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setFrameShape(QFrame.StyledPanel)
        self.frame_73.setFrameShadow(QFrame.Raised)
        self.verticalLayout_69 = QVBoxLayout(self.frame_73)
        self.verticalLayout_69.setSpacing(0)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.verticalLayout_69.setContentsMargins(0, 0, 0, 0)
        self.settingsBackBtn = QPushButton(self.frame_73)
        self.settingsBackBtn.setObjectName(u"settingsBackBtn")
        sizePolicy5.setHeightForWidth(self.settingsBackBtn.sizePolicy().hasHeightForWidth())
        self.settingsBackBtn.setSizePolicy(sizePolicy5)
        self.settingsBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.settingsBackBtn.setIcon(icon10)

        self.verticalLayout_69.addWidget(self.settingsBackBtn)

        self.frame_75 = QFrame(self.frame_73)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"}")
        self.frame_75.setFrameShape(QFrame.StyledPanel)
        self.frame_75.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_75)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.horizontalLayout_85.setContentsMargins(0, 0, 0, 0)
        self.pageHeader6 = QLabel(self.frame_75)
        self.pageHeader6.setObjectName(u"pageHeader6")
        sizePolicy3.setHeightForWidth(self.pageHeader6.sizePolicy().hasHeightForWidth())
        self.pageHeader6.setSizePolicy(sizePolicy3)
        self.pageHeader6.setStyleSheet(u"")

        self.horizontalLayout_85.addWidget(self.pageHeader6)

        self.clinicIconP6 = QLabel(self.frame_75)
        self.clinicIconP6.setObjectName(u"clinicIconP6")
        self.clinicIconP6.setMaximumSize(QSize(145, 60))
        self.clinicIconP6.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP6.setScaledContents(True)
        self.clinicIconP6.setAlignment(Qt.AlignCenter)
        self.clinicIconP6.setWordWrap(False)

        self.horizontalLayout_85.addWidget(self.clinicIconP6)


        self.verticalLayout_69.addWidget(self.frame_75)

        self.settingsTab = QFrame(self.frame_73)
        self.settingsTab.setObjectName(u"settingsTab")
        sizePolicy.setHeightForWidth(self.settingsTab.sizePolicy().hasHeightForWidth())
        self.settingsTab.setSizePolicy(sizePolicy)
        self.settingsTab.setMinimumSize(QSize(0, 45))
        self.settingsTab.setMaximumSize(QSize(16777215, 80))
        self.settingsTab.setBaseSize(QSize(0, 45))
        self.settingsTab.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: rgb(166, 166, 166);\n"
"	font-family:\"Montserrat SemiBold\";\n"
"    font-weight: 63;\n"
"    padding: 10px 15px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(194, 194, 194);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color:rgb(124, 181, 208); \n"
"	border-radius:5px;\n"
"    color: rgb(40, 40, 40);                         \n"
"}")
        self.settingsTab.setFrameShape(QFrame.StyledPanel)
        self.settingsTab.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_86 = QHBoxLayout(self.settingsTab)
        self.horizontalLayout_86.setSpacing(5)
        self.horizontalLayout_86.setObjectName(u"horizontalLayout_86")
        self.horizontalLayout_86.setContentsMargins(0, 10, 0, 5)
        self.profileTabBtn = QPushButton(self.settingsTab)
        self.profileTabBtn.setObjectName(u"profileTabBtn")
        sizePolicy.setHeightForWidth(self.profileTabBtn.sizePolicy().hasHeightForWidth())
        self.profileTabBtn.setSizePolicy(sizePolicy)
        self.profileTabBtn.setStyleSheet(u"")

        self.horizontalLayout_86.addWidget(self.profileTabBtn)

        self.securityTabBtn = QPushButton(self.settingsTab)
        self.securityTabBtn.setObjectName(u"securityTabBtn")
        sizePolicy.setHeightForWidth(self.securityTabBtn.sizePolicy().hasHeightForWidth())
        self.securityTabBtn.setSizePolicy(sizePolicy)
        self.securityTabBtn.setStyleSheet(u"")

        self.horizontalLayout_86.addWidget(self.securityTabBtn)

        self.preferencesTabBtn = QPushButton(self.settingsTab)
        self.preferencesTabBtn.setObjectName(u"preferencesTabBtn")
        sizePolicy.setHeightForWidth(self.preferencesTabBtn.sizePolicy().hasHeightForWidth())
        self.preferencesTabBtn.setSizePolicy(sizePolicy)
        self.preferencesTabBtn.setStyleSheet(u"")

        self.horizontalLayout_86.addWidget(self.preferencesTabBtn)

        self.UserManagementTabBtn = QPushButton(self.settingsTab)
        self.UserManagementTabBtn.setObjectName(u"UserManagementTabBtn")
        sizePolicy.setHeightForWidth(self.UserManagementTabBtn.sizePolicy().hasHeightForWidth())
        self.UserManagementTabBtn.setSizePolicy(sizePolicy)
        self.UserManagementTabBtn.setStyleSheet(u"")

        self.horizontalLayout_86.addWidget(self.UserManagementTabBtn)


        self.verticalLayout_69.addWidget(self.settingsTab)

        self.settingsStactWidget = QStackedWidget(self.frame_73)
        self.settingsStactWidget.setObjectName(u"settingsStactWidget")
        sizePolicy.setHeightForWidth(self.settingsStactWidget.sizePolicy().hasHeightForWidth())
        self.settingsStactWidget.setSizePolicy(sizePolicy)
        self.profileTab = QWidget()
        self.profileTab.setObjectName(u"profileTab")
        self.verticalLayout_71 = QVBoxLayout(self.profileTab)
        self.verticalLayout_71.setSpacing(0)
        self.verticalLayout_71.setObjectName(u"verticalLayout_71")
        self.verticalLayout_71.setContentsMargins(0, 0, 0, 0)
        self.frame_77 = QFrame(self.profileTab)
        self.frame_77.setObjectName(u"frame_77")
        self.frame_77.setEnabled(False)
        self.frame_77.setStyleSheet(u"QLabel{\n"
"font: 57 11pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"\n"
"QLineEdit:disabled{\n"
"	background-color:rgb(225, 225, 225);\n"
"		color:rgb(97, 97, 97);\n"
"\n"
"}")
        self.frame_77.setFrameShape(QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QFrame.Raised)
        self.verticalLayout_75 = QVBoxLayout(self.frame_77)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.verticalLayout_75.setContentsMargins(25, 25, 25, 25)
        self.profileInfoFrame = QFrame(self.frame_77)
        self.profileInfoFrame.setObjectName(u"profileInfoFrame")
        self.profileInfoFrame.setStyleSheet(u"#profileInfoFrame{\n"
"	background-color:rgb(183, 218, 234);\n"
"	border-radius:35px;\n"
"}")
        self.profileInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.profileInfoFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_78 = QVBoxLayout(self.profileInfoFrame)
        self.verticalLayout_78.setObjectName(u"verticalLayout_78")
        self.verticalLayout_78.setContentsMargins(25, 25, 25, -1)
        self.label_40 = QLabel(self.profileInfoFrame)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setStyleSheet(u"font: 87 12pt \"Montserrat Black\";")

        self.verticalLayout_78.addWidget(self.label_40)

        self.fullNameUserName = QFrame(self.profileInfoFrame)
        self.fullNameUserName.setObjectName(u"fullNameUserName")
        self.fullNameUserName.setFrameShape(QFrame.StyledPanel)
        self.fullNameUserName.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_91 = QHBoxLayout(self.fullNameUserName)
        self.horizontalLayout_91.setObjectName(u"horizontalLayout_91")
        self.horizontalLayout_91.setContentsMargins(20, -1, 0, 0)
        self.fullname = QFrame(self.fullNameUserName)
        self.fullname.setObjectName(u"fullname")
        self.fullname.setFrameShape(QFrame.StyledPanel)
        self.fullname.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_93 = QHBoxLayout(self.fullname)
        self.horizontalLayout_93.setSpacing(15)
        self.horizontalLayout_93.setObjectName(u"horizontalLayout_93")
        self.horizontalLayout_93.setContentsMargins(0, 10, 0, 10)
        self.label = QLabel(self.fullname)
        self.label.setObjectName(u"label")

        self.horizontalLayout_93.addWidget(self.label)

        self.profileFullName = QLineEdit(self.fullname)
        self.profileFullName.setObjectName(u"profileFullName")
        self.profileFullName.setEnabled(False)
        sizePolicy.setHeightForWidth(self.profileFullName.sizePolicy().hasHeightForWidth())
        self.profileFullName.setSizePolicy(sizePolicy)
        self.profileFullName.setMinimumSize(QSize(0, 45))
        self.profileFullName.setMaximumSize(QSize(16777215, 80))
        self.profileFullName.setReadOnly(False)

        self.horizontalLayout_93.addWidget(self.profileFullName)


        self.horizontalLayout_91.addWidget(self.fullname)

        self.username = QFrame(self.fullNameUserName)
        self.username.setObjectName(u"username")
        self.username.setFrameShape(QFrame.StyledPanel)
        self.username.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_92 = QHBoxLayout(self.username)
        self.horizontalLayout_92.setSpacing(20)
        self.horizontalLayout_92.setObjectName(u"horizontalLayout_92")
        self.horizontalLayout_92.setContentsMargins(0, 10, 0, 10)
        self.label_34 = QLabel(self.username)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_92.addWidget(self.label_34)

        self.profileUserName = QLineEdit(self.username)
        self.profileUserName.setObjectName(u"profileUserName")
        self.profileUserName.setEnabled(False)
        sizePolicy.setHeightForWidth(self.profileUserName.sizePolicy().hasHeightForWidth())
        self.profileUserName.setSizePolicy(sizePolicy)
        self.profileUserName.setMinimumSize(QSize(0, 45))
        self.profileUserName.setMaximumSize(QSize(16777215, 80))
        self.profileUserName.setReadOnly(False)

        self.horizontalLayout_92.addWidget(self.profileUserName)


        self.horizontalLayout_91.addWidget(self.username)


        self.verticalLayout_78.addWidget(self.fullNameUserName)

        self.EmailPhone = QFrame(self.profileInfoFrame)
        self.EmailPhone.setObjectName(u"EmailPhone")
        self.EmailPhone.setFrameShape(QFrame.StyledPanel)
        self.EmailPhone.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_94 = QHBoxLayout(self.EmailPhone)
        self.horizontalLayout_94.setObjectName(u"horizontalLayout_94")
        self.horizontalLayout_94.setContentsMargins(20, -1, 0, 0)
        self.Email = QFrame(self.EmailPhone)
        self.Email.setObjectName(u"Email")
        self.Email.setFrameShape(QFrame.StyledPanel)
        self.Email.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_96 = QHBoxLayout(self.Email)
        self.horizontalLayout_96.setSpacing(50)
        self.horizontalLayout_96.setObjectName(u"horizontalLayout_96")
        self.horizontalLayout_96.setContentsMargins(0, 10, 0, 10)
        self.label_35 = QLabel(self.Email)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_96.addWidget(self.label_35)

        self.profileEmail = QLineEdit(self.Email)
        self.profileEmail.setObjectName(u"profileEmail")
        self.profileEmail.setEnabled(False)
        sizePolicy.setHeightForWidth(self.profileEmail.sizePolicy().hasHeightForWidth())
        self.profileEmail.setSizePolicy(sizePolicy)
        self.profileEmail.setMinimumSize(QSize(0, 45))
        self.profileEmail.setMaximumSize(QSize(16777215, 80))
        self.profileEmail.setReadOnly(False)

        self.horizontalLayout_96.addWidget(self.profileEmail)


        self.horizontalLayout_94.addWidget(self.Email)

        self.Phone = QFrame(self.EmailPhone)
        self.Phone.setObjectName(u"Phone")
        self.Phone.setFrameShape(QFrame.StyledPanel)
        self.Phone.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_95 = QHBoxLayout(self.Phone)
        self.horizontalLayout_95.setSpacing(55)
        self.horizontalLayout_95.setObjectName(u"horizontalLayout_95")
        self.horizontalLayout_95.setContentsMargins(0, 10, 0, 10)
        self.label_36 = QLabel(self.Phone)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_95.addWidget(self.label_36)

        self.profilePhone = QLineEdit(self.Phone)
        self.profilePhone.setObjectName(u"profilePhone")
        self.profilePhone.setEnabled(False)
        sizePolicy.setHeightForWidth(self.profilePhone.sizePolicy().hasHeightForWidth())
        self.profilePhone.setSizePolicy(sizePolicy)
        self.profilePhone.setMinimumSize(QSize(0, 45))
        self.profilePhone.setMaximumSize(QSize(16777215, 80))
        self.profilePhone.setReadOnly(False)

        self.horizontalLayout_95.addWidget(self.profilePhone)


        self.horizontalLayout_94.addWidget(self.Phone)


        self.verticalLayout_78.addWidget(self.EmailPhone)

        self.label_37 = QLabel(self.profileInfoFrame)
        self.label_37.setObjectName(u"label_37")
        sizePolicy2.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy2)
        self.label_37.setStyleSheet(u"font: 87 12pt \"Montserrat Black\";")

        self.verticalLayout_78.addWidget(self.label_37)

        self.accountInfo = QFrame(self.profileInfoFrame)
        self.accountInfo.setObjectName(u"accountInfo")
        self.accountInfo.setFrameShape(QFrame.StyledPanel)
        self.accountInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_77 = QVBoxLayout(self.accountInfo)
        self.verticalLayout_77.setObjectName(u"verticalLayout_77")
        self.verticalLayout_77.setContentsMargins(20, -1, -1, -1)
        self.accountRole = QLabel(self.accountInfo)
        self.accountRole.setObjectName(u"accountRole")
        sizePolicy2.setHeightForWidth(self.accountRole.sizePolicy().hasHeightForWidth())
        self.accountRole.setSizePolicy(sizePolicy2)
        self.accountRole.setMargin(0)

        self.verticalLayout_77.addWidget(self.accountRole)

        self.MemberSince = QLabel(self.accountInfo)
        self.MemberSince.setObjectName(u"MemberSince")
        sizePolicy2.setHeightForWidth(self.MemberSince.sizePolicy().hasHeightForWidth())
        self.MemberSince.setSizePolicy(sizePolicy2)
        self.MemberSince.setMargin(0)

        self.verticalLayout_77.addWidget(self.MemberSince)


        self.verticalLayout_78.addWidget(self.accountInfo)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_78.addItem(self.verticalSpacer_18)

        self.settingAcctionBtn = QFrame(self.profileInfoFrame)
        self.settingAcctionBtn.setObjectName(u"settingAcctionBtn")
        self.settingAcctionBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 14pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color: #FCD597;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"border-radius: 10px;\n"
"}")
        self.settingAcctionBtn.setFrameShape(QFrame.StyledPanel)
        self.settingAcctionBtn.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_97 = QHBoxLayout(self.settingAcctionBtn)
        self.horizontalLayout_97.setObjectName(u"horizontalLayout_97")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_97.addItem(self.horizontalSpacer_5)

        self.settingsProfileEditBtn = QPushButton(self.settingAcctionBtn)
        self.settingsProfileEditBtn.setObjectName(u"settingsProfileEditBtn")

        self.horizontalLayout_97.addWidget(self.settingsProfileEditBtn)

        self.settingsProfileSaveBtn = QPushButton(self.settingAcctionBtn)
        self.settingsProfileSaveBtn.setObjectName(u"settingsProfileSaveBtn")

        self.horizontalLayout_97.addWidget(self.settingsProfileSaveBtn)

        self.settingsProfileCancelBtn = QPushButton(self.settingAcctionBtn)
        self.settingsProfileCancelBtn.setObjectName(u"settingsProfileCancelBtn")
        self.settingsProfileCancelBtn.setStyleSheet(u"QPushButton{\n"
"	background-color:	rgb(220, 90, 90);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"\n"
"}")

        self.horizontalLayout_97.addWidget(self.settingsProfileCancelBtn)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_97.addItem(self.horizontalSpacer_6)


        self.verticalLayout_78.addWidget(self.settingAcctionBtn)


        self.verticalLayout_75.addWidget(self.profileInfoFrame)


        self.verticalLayout_71.addWidget(self.frame_77)

        self.settingsStactWidget.addWidget(self.profileTab)
        self.securityTab = QWidget()
        self.securityTab.setObjectName(u"securityTab")
        self.verticalLayout_72 = QVBoxLayout(self.securityTab)
        self.verticalLayout_72.setObjectName(u"verticalLayout_72")
        self.label_7 = QLabel(self.securityTab)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setStyleSheet(u"font: 14pt \"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);")

        self.verticalLayout_72.addWidget(self.label_7)

        self.frame_76 = QFrame(self.securityTab)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setFrameShape(QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_90 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_90.setObjectName(u"horizontalLayout_90")
        self.horizontalLayout_90.setContentsMargins(100, 50, 100, 50)
        self.changePassFrame = QFrame(self.frame_76)
        self.changePassFrame.setObjectName(u"changePassFrame")
        self.changePassFrame.setMaximumSize(QSize(900, 500))
        self.changePassFrame.setStyleSheet(u"\n"
"#changePassFrame{\n"
"	background-color:rgb(183, 218, 234);\n"
"	border-radius:35px;\n"
"}\n"
"QLabel{\n"
"font: 57 12pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 10px;\n"
"	font-family: \"Montserrat Medium\";\n"
"	font-weight: 57;\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"	background-color:rgb(245, 245, 245);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 1px solid rgb(235, 235, 235);\n"
"	background-color:rgb(227, 227, 227);\n"
"}\n"
"")
        self.changePassFrame.setFrameShape(QFrame.StyledPanel)
        self.changePassFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_76 = QVBoxLayout(self.changePassFrame)
        self.verticalLayout_76.setObjectName(u"verticalLayout_76")
        self.verticalLayout_76.setContentsMargins(20, 40, 20, 20)
        self.frame_81 = QFrame(self.changePassFrame)
        self.frame_81.setObjectName(u"frame_81")
        self.frame_81.setMaximumSize(QSize(16777215, 80))
        self.frame_81.setFrameShape(QFrame.StyledPanel)
        self.frame_81.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_81)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_10 = QLabel(self.frame_81)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_3.addWidget(self.label_10)

        self.currentPassEdit = QLineEdit(self.frame_81)
        self.currentPassEdit.setObjectName(u"currentPassEdit")
        sizePolicy.setHeightForWidth(self.currentPassEdit.sizePolicy().hasHeightForWidth())
        self.currentPassEdit.setSizePolicy(sizePolicy)
        self.currentPassEdit.setMinimumSize(QSize(0, 45))
        self.currentPassEdit.setMaximumSize(QSize(16777215, 80))

        self.horizontalLayout_3.addWidget(self.currentPassEdit)


        self.verticalLayout_76.addWidget(self.frame_81)

        self.frame_82 = QFrame(self.changePassFrame)
        self.frame_82.setObjectName(u"frame_82")
        self.frame_82.setMaximumSize(QSize(16777215, 80))
        self.frame_82.setFrameShape(QFrame.StyledPanel)
        self.frame_82.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frame_82)
        self.horizontalLayout_87.setSpacing(35)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.label_29 = QLabel(self.frame_82)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_87.addWidget(self.label_29)

        self.newPassEdit = QLineEdit(self.frame_82)
        self.newPassEdit.setObjectName(u"newPassEdit")
        sizePolicy.setHeightForWidth(self.newPassEdit.sizePolicy().hasHeightForWidth())
        self.newPassEdit.setSizePolicy(sizePolicy)
        self.newPassEdit.setMinimumSize(QSize(0, 45))
        self.newPassEdit.setMaximumSize(QSize(16777215, 80))

        self.horizontalLayout_87.addWidget(self.newPassEdit)


        self.verticalLayout_76.addWidget(self.frame_82)

        self.frame_83 = QFrame(self.changePassFrame)
        self.frame_83.setObjectName(u"frame_83")
        self.frame_83.setMaximumSize(QSize(16777215, 80))
        self.frame_83.setFrameShape(QFrame.StyledPanel)
        self.frame_83.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.frame_83)
        self.horizontalLayout_88.setSpacing(7)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.label_33 = QLabel(self.frame_83)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_88.addWidget(self.label_33)

        self.confirmPassEdit = QLineEdit(self.frame_83)
        self.confirmPassEdit.setObjectName(u"confirmPassEdit")
        sizePolicy.setHeightForWidth(self.confirmPassEdit.sizePolicy().hasHeightForWidth())
        self.confirmPassEdit.setSizePolicy(sizePolicy)
        self.confirmPassEdit.setMinimumSize(QSize(0, 45))
        self.confirmPassEdit.setMaximumSize(QSize(16777215, 80))

        self.horizontalLayout_88.addWidget(self.confirmPassEdit)


        self.verticalLayout_76.addWidget(self.frame_83)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_76.addItem(self.verticalSpacer_12)

        self.frame_84 = QFrame(self.changePassFrame)
        self.frame_84.setObjectName(u"frame_84")
        self.frame_84.setMaximumSize(QSize(16777215, 80))
        self.frame_84.setFrameShape(QFrame.StyledPanel)
        self.frame_84.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_89 = QHBoxLayout(self.frame_84)
        self.horizontalLayout_89.setObjectName(u"horizontalLayout_89")
        self.pushButton_2 = QPushButton(self.frame_84)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton{\n"
"	font: 63 14pt \"Montserrat SemiBold\";\n"
"	color:rgb(52, 52, 52);\n"
"	background-color: #FCD597;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"border-radius: 10px;\n"
"}")

        self.horizontalLayout_89.addWidget(self.pushButton_2)


        self.verticalLayout_76.addWidget(self.frame_84)


        self.horizontalLayout_90.addWidget(self.changePassFrame)


        self.verticalLayout_72.addWidget(self.frame_76)

        self.settingsStactWidget.addWidget(self.securityTab)
        self.preferencesTab = QWidget()
        self.preferencesTab.setObjectName(u"preferencesTab")
        self.verticalLayout_73 = QVBoxLayout(self.preferencesTab)
        self.verticalLayout_73.setObjectName(u"verticalLayout_73")
        self.label_8 = QLabel(self.preferencesTab)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_73.addWidget(self.label_8)

        self.settingsStactWidget.addWidget(self.preferencesTab)
        self.userManagementTab = QWidget()
        self.userManagementTab.setObjectName(u"userManagementTab")
        self.verticalLayout_74 = QVBoxLayout(self.userManagementTab)
        self.verticalLayout_74.setObjectName(u"verticalLayout_74")
        self.label_9 = QLabel(self.userManagementTab)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_74.addWidget(self.label_9)

        self.settingsStactWidget.addWidget(self.userManagementTab)

        self.verticalLayout_69.addWidget(self.settingsStactWidget)


        self.verticalLayout_15.addWidget(self.frame_73)

        self.stackedWidget.addWidget(self.settings)
        self.notification = QWidget()
        self.notification.setObjectName(u"notification")
        self.notification.setStyleSheet(u"QWidget{\n"
"	background:transparent;\n"
"\n"
"}")
        self.verticalLayout_79 = QVBoxLayout(self.notification)
        self.verticalLayout_79.setObjectName(u"verticalLayout_79")
        self.frame_85 = QFrame(self.notification)
        self.frame_85.setObjectName(u"frame_85")
        self.frame_85.setFrameShape(QFrame.StyledPanel)
        self.frame_85.setFrameShadow(QFrame.Raised)
        self.notifBackBtn = QPushButton(self.frame_85)
        self.notifBackBtn.setObjectName(u"notifBackBtn")
        self.notifBackBtn.setGeometry(QRect(0, 10, 20, 16))
        sizePolicy5.setHeightForWidth(self.notifBackBtn.sizePolicy().hasHeightForWidth())
        self.notifBackBtn.setSizePolicy(sizePolicy5)
        self.notifBackBtn.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.notifBackBtn.setIcon(icon10)
        self.frame_86 = QFrame(self.frame_85)
        self.frame_86.setObjectName(u"frame_86")
        self.frame_86.setGeometry(QRect(0, 30, 858, 62))
        self.frame_86.setStyleSheet(u"QLabel{\n"
"	font-family:\"Rubik Mono One\";\n"
"	color:rgb(52, 52, 52);\n"
"}")
        self.frame_86.setFrameShape(QFrame.StyledPanel)
        self.frame_86.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_98 = QHBoxLayout(self.frame_86)
        self.horizontalLayout_98.setObjectName(u"horizontalLayout_98")
        self.horizontalLayout_98.setContentsMargins(0, 0, 0, 0)
        self.pageHeader7 = QLabel(self.frame_86)
        self.pageHeader7.setObjectName(u"pageHeader7")
        sizePolicy3.setHeightForWidth(self.pageHeader7.sizePolicy().hasHeightForWidth())
        self.pageHeader7.setSizePolicy(sizePolicy3)
        self.pageHeader7.setStyleSheet(u"")

        self.horizontalLayout_98.addWidget(self.pageHeader7)

        self.clinicIconP7 = QLabel(self.frame_86)
        self.clinicIconP7.setObjectName(u"clinicIconP7")
        self.clinicIconP7.setMaximumSize(QSize(145, 60))
        self.clinicIconP7.setPixmap(QPixmap(u":/images/image/petmateLogo.png"))
        self.clinicIconP7.setScaledContents(True)
        self.clinicIconP7.setAlignment(Qt.AlignCenter)
        self.clinicIconP7.setWordWrap(False)

        self.horizontalLayout_98.addWidget(self.clinicIconP7)


        self.verticalLayout_79.addWidget(self.frame_85)

        self.stackedWidget.addWidget(self.notification)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout_71.addWidget(self.MainContent)


        self.verticalLayout_70.addWidget(self.underFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.homeBtn_2.clicked.connect(self.homeBtn.click)
        self.addPatientBtn_2.clicked.connect(self.addPatientBtn.click)
        self.appointmentBtn_2.clicked.connect(self.appointmentBtn.click)
        self.schedVaxBtn_2.clicked.connect(self.schedVaxBtn.click)
        self.homeBtn.toggled.connect(self.homeBtn_2.setChecked)
        self.addPatientBtn.toggled.connect(self.addPatientBtn_2.setChecked)
        self.petRecordsBtn.toggled.connect(self.petRecordsBtn_2.setChecked)
        self.appointmentBtn.toggled.connect(self.appointmentBtn_2.setChecked)
        self.schedVaxBtn.toggled.connect(self.schedVaxBtn_2.setChecked)
        self.petRecordsBtn_2.clicked.connect(self.petRecordsBtn.click)
        self.settings_2.clicked.connect(self.settingsBtn.click)
        self.settingsBtn.toggled.connect(self.settings_2.setChecked)

        self.stackedWidget.setCurrentIndex(9)
        self.cityComboBox.setCurrentIndex(-1)
        self.walkInOrWeb.setCurrentIndex(1)
        self.webAppointmentStackWidget.setCurrentIndex(2)
        self.statusStackedWidget.setCurrentIndex(0)
        self.returnStackedWidget.setCurrentIndex(1)
        self.profileStackedWidget.setCurrentIndex(0)
        self.speciesComboBox.setCurrentIndex(0)
        self.serviceHistoryStackedWidget.setCurrentIndex(1)
        self.serviceTypeComboBox.setCurrentIndex(0)
        self.settingsStactWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PETMATE INFORMATION SYSTEM", None))
        self.fullNavBtn.setText("")
        self.PetmateLogo.setText("")
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u"   HOME", None))
        self.addPatientBtn.setText(QCoreApplication.translate("MainWindow", u"   ADD CLIENT", None))
        self.petRecordsBtn.setText(QCoreApplication.translate("MainWindow", u"   RECORDS", None))
        self.appointmentBtn.setText(QCoreApplication.translate("MainWindow", u"   APPOINTMENT", None))
        self.schedVaxBtn.setText(QCoreApplication.translate("MainWindow", u"   FOLLOW-UPS", None))
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"    SETTINGS", None))
        self.miniNavBtn.setText("")
        self.PetmateLogo_2.setText("")
#if QT_CONFIG(tooltip)
        self.homeBtn_2.setToolTip(QCoreApplication.translate("MainWindow", u"HOME", None))
#endif // QT_CONFIG(tooltip)
        self.homeBtn_2.setText("")
#if QT_CONFIG(tooltip)
        self.addPatientBtn_2.setToolTip(QCoreApplication.translate("MainWindow", u"ADD PATIENT", None))
#endif // QT_CONFIG(tooltip)
        self.addPatientBtn_2.setText("")
#if QT_CONFIG(tooltip)
        self.petRecordsBtn_2.setToolTip(QCoreApplication.translate("MainWindow", u"RECORDS", None))
#endif // QT_CONFIG(tooltip)
        self.petRecordsBtn_2.setText("")
#if QT_CONFIG(tooltip)
        self.appointmentBtn_2.setToolTip(QCoreApplication.translate("MainWindow", u"APPOINTMENT", None))
#endif // QT_CONFIG(tooltip)
        self.appointmentBtn_2.setText("")
#if QT_CONFIG(tooltip)
        self.schedVaxBtn_2.setToolTip(QCoreApplication.translate("MainWindow", u"SCHEDULED RETURNS", None))
#endif // QT_CONFIG(tooltip)
        self.schedVaxBtn_2.setText("")
#if QT_CONFIG(tooltip)
        self.settings_2.setToolTip(QCoreApplication.translate("MainWindow", u"SETTINGS", None))
#endif // QT_CONFIG(tooltip)
        self.settings_2.setText("")
#if QT_CONFIG(whatsthis)
        self.pageHeader1.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pageHeader1.setText(QCoreApplication.translate("MainWindow", u"ADD New Client", None))
        self.clinicIconP1.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"BASIC INFORMATION", None))
        self.firstNameEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"First name", None))
        self.lastNameEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Last name", None))
        self.middleNameEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Middle Name (optional)", None))
        self.emailEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.phoneNumberEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Phone number", None))
        self.secondaryPhoneEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Secondary Phone (optional)", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"ADDRESS", None))
        self.detailedAddressEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Subdivision/Ph/Blk-L", None))
        self.confirmButton.setText(QCoreApplication.translate("MainWindow", u"CONFIRM", None))
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", u"CANCEL", None))
        self.updateBasicInfo.setText(QCoreApplication.translate("MainWindow", u"UPDATE", None))
        self.pageHeader2.setText(QCoreApplication.translate("MainWindow", u"Client Records", None))
        self.clinicIconP2.setText("")
        self.searchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"search records.....", None))
        self.searchIcon.setText("")
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"NO RECORDS", None))
        self.pageHeader3.setText(QCoreApplication.translate("MainWindow", u"Appointments", None))
        self.clinicIconP3.setText("")
        self.websiteBtn.setText(QCoreApplication.translate("MainWindow", u"Appointment Request", None))
        self.walkInBtn.setText(QCoreApplication.translate("MainWindow", u"Appoinment Status", None))
        self.searchBar_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"search appointments.....", None))
        self.searchIcon_2.setText("")
        self.pendingWebBtn.setText(QCoreApplication.translate("MainWindow", u"Requests", None))
        self.AcceptedBtn.setText(QCoreApplication.translate("MainWindow", u"Accepted", None))
        self.DeclinedBtn.setText(QCoreApplication.translate("MainWindow", u"Declined", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"ADD APPOINTMENT", None))
        self.pendingBtn.setText(QCoreApplication.translate("MainWindow", u"Pending", None))
        self.completedBtn.setText(QCoreApplication.translate("MainWindow", u"Completed", None))
        self.overdueBtn.setText(QCoreApplication.translate("MainWindow", u"Overdue", None))
        self.cancelledBtn.setText(QCoreApplication.translate("MainWindow", u"Cancelled", None))
        self.pageHeader4.setText(QCoreApplication.translate("MainWindow", u"SCHEDULED RETURN VISIT", None))
        self.clinicIconP4.setText("")
        self.monthComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"January", None))
        self.monthComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"February", None))
        self.monthComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"March", None))
        self.monthComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"April", None))
        self.monthComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"May", None))
        self.monthComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"June", None))
        self.monthComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"July", None))
        self.monthComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"August", None))
        self.monthComboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"September", None))
        self.monthComboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"October", None))
        self.monthComboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"November", None))
        self.monthComboBox.setItemText(11, QCoreApplication.translate("MainWindow", u"December", None))

        self.monthComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"January", None))
        self.lineEdit_9.setText("")
        self.lineEdit_9.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.label_172.setText("")
        self.pendingReturnBtn.setText(QCoreApplication.translate("MainWindow", u"Pending", None))
        self.completeReurnBtn.setText(QCoreApplication.translate("MainWindow", u"Completed", None))
        self.overdueReturnBtn.setText(QCoreApplication.translate("MainWindow", u"Overdue", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.profileBackbutton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.profileNameLabel.setText(QCoreApplication.translate("MainWindow", u"Dredd Domasian", None))
        self.profileEmailLabel.setText(QCoreApplication.translate("MainWindow", u"DomasianDredd@gmail.com", None))
        self.addressLabel.setText(QCoreApplication.translate("MainWindow", u"San Francisco, General Trias Cavite", None))
        self.detailedAddressLabel.setText(QCoreApplication.translate("MainWindow", u"Detailed Address", None))
        self.phoneLabel.setText(QCoreApplication.translate("MainWindow", u"09272483891", None))
        self.profileEditBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.profileDeleteBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.profileIcon.setText("")
        self.plusSignBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.addpetQtoolBtn.setText(QCoreApplication.translate("MainWindow", u"ADD PET", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"PET DETAILS", None))
        self.petName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pet name", None))
        self.petColor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.breed.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Breed", None))
        self.speciesComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Select Species", None))
        self.speciesComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Cat", None))
        self.speciesComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Dog", None))
        self.speciesComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Others", None))

        self.speciesComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Select Species", None))
        self.otherSpeciesLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Specify species", None))
        self.clearSpeciesBtn.setText("")
        self.Bday.setSpecialValueText(QCoreApplication.translate("MainWindow", u"Birthday (optional)", None))
        self.age.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Age (estimated)", None))
        self.petSexComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Sex", None))
        self.petSexComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Male", None))
        self.petSexComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Female", None))

        self.petRemarks.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Remarks (optional)", None))
        self.backBtn.setText(QCoreApplication.translate("MainWindow", u"CANCEL", None))
        self.petConfirmButton.setText(QCoreApplication.translate("MainWindow", u"CONFIRM", None))
        self.petUpdateButton.setText(QCoreApplication.translate("MainWindow", u"UPDATE", None))
        self.petProfileBackBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.reminderBtn.setText("")
        self.petProfileIcon.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"NAME:", None))
        self.petProfileNameLabel.setText(QCoreApplication.translate("MainWindow", u"PET NAME", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"BREED:", None))
        self.breedLabel.setText(QCoreApplication.translate("MainWindow", u"BREED", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"REMARKS:", None))
        self.petRemarksLabel.setText(QCoreApplication.translate("MainWindow", u"REMARKS", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"BIRTHDAY:", None))
        self.petBirthdayOptional.setText(QCoreApplication.translate("MainWindow", u"AUG 26, 2025", None))
        self.petProfileEditBtn.setText(QCoreApplication.translate("MainWindow", u"EDIT DETAILS", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"COLOR:", None))
        self.petColorLabel.setText(QCoreApplication.translate("MainWindow", u"COLOR", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"SPECIES:", None))
        self.speciesLabel.setText(QCoreApplication.translate("MainWindow", u"CAT", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"SEX:", None))
        self.petSexLabel.setText(QCoreApplication.translate("MainWindow", u"SEX", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"AGE:", None))
        self.petAgeLabel.setText(QCoreApplication.translate("MainWindow", u"1 DAY OLD", None))
        self.petProfileDeleteBtn.setText(QCoreApplication.translate("MainWindow", u"DELETE PET", None))
        self.serviceHistoryBtn.setText(QCoreApplication.translate("MainWindow", u"Service History", None))
        self.addNewServiceBtn.setText(QCoreApplication.translate("MainWindow", u"Add New Service", None))
        self.searchBar_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"search service.....", None))
        self.searchIcon_3.setText("")
        self.label_157.setText(QCoreApplication.translate("MainWindow", u"Service", None))
        self.label_158.setText(QCoreApplication.translate("MainWindow", u"  Done On", None))
        self.label_159.setText(QCoreApplication.translate("MainWindow", u"Return Date", None))
        self.label_160.setText(QCoreApplication.translate("MainWindow", u"Open Notes", None))
        self.printBtn.setText("")
        self.label_138.setText(QCoreApplication.translate("MainWindow", u"EMPTY", None))
        self.label_137.setText(QCoreApplication.translate("MainWindow", u"Service Type", None))
        self.serviceTypeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Select Service", None))
        self.serviceTypeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Vaccination", None))
        self.serviceTypeComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Deworming", None))
        self.serviceTypeComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Tick & Flea Prevention", None))
        self.serviceTypeComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Consultation", None))
        self.serviceTypeComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Wellness Check", None))
        self.serviceTypeComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"Surgery", None))
        self.serviceTypeComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"CBC", None))
        self.serviceTypeComboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"Blood Chemistry", None))
        self.serviceTypeComboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"Progesterone test", None))
        self.serviceTypeComboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"Pregnancy test", None))
        self.serviceTypeComboBox.setItemText(11, QCoreApplication.translate("MainWindow", u"Diagnostic Microscopy", None))
        self.serviceTypeComboBox.setItemText(12, QCoreApplication.translate("MainWindow", u"Urinalysis", None))
        self.serviceTypeComboBox.setItemText(13, QCoreApplication.translate("MainWindow", u"Antigen/Antibody", None))

        self.serviceTypeComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Select Service", None))
        self.label_139.setText(QCoreApplication.translate("MainWindow", u"Done on", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"MMM d, yyyy", None))
        self.addNoteLabel.setText(QCoreApplication.translate("MainWindow", u"Note:", None))
        self.returnCheckBox.setText(QCoreApplication.translate("MainWindow", u"Return Date (Optional)", None))
        self.returnDateEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"MMM d, yyyy", None))
        self.returnDatePlaceholder.setPlaceholderText("")
        self.updateServiceBtn.setText(QCoreApplication.translate("MainWindow", u"UPDATE", None))
        self.addServiceBtn.setText(QCoreApplication.translate("MainWindow", u"ADD SERVICE", None))
        self.cancelAddServiceBtn.setText(QCoreApplication.translate("MainWindow", u"CANCEL", None))
        self.pageHeader5.setText(QCoreApplication.translate("MainWindow", u"Review Appointments", None))
        self.clinicIconP5.setText("")
        self.label_13.setText("")
        self.reviewFullname.setText(QCoreApplication.translate("MainWindow", u"FULL NAME", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"ID:", None))
        self.BookingId.setText(QCoreApplication.translate("MainWindow", u"Booking Id", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"EMAIL:", None))
        self.reviewEmail.setText(QCoreApplication.translate("MainWindow", u"Email Address", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"PHONE NO:", None))
        self.reviewPhoneNo.setText(QCoreApplication.translate("MainWindow", u"Phone no.", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"ADDRESS:", None))
        self.reviewAddress.setText(QCoreApplication.translate("MainWindow", u"Address", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"DETAILED ADD:", None))
        self.reviewDetailedAddress.setText(QCoreApplication.translate("MainWindow", u"Detailed Address", None))
        self.ReviewPetIcon.setText("")
        self.reviewPetName.setText(QCoreApplication.translate("MainWindow", u"PET NAME", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"SPECIES:", None))
        self.reviewSpecies.setText(QCoreApplication.translate("MainWindow", u"Species", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"SEX:", None))
        self.reviewSex.setText(QCoreApplication.translate("MainWindow", u"SEX", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"SERVICE:", None))
        self.reviewService.setText(QCoreApplication.translate("MainWindow", u"Service", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"DOCTOR:", None))
        self.reviewDoctor.setText(QCoreApplication.translate("MainWindow", u"Provider/Doctor", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"BREED:", None))
        self.reviewBreed.setText(QCoreApplication.translate("MainWindow", u"Breed", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"COLOR:", None))
        self.reviewColor.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"DATE:", None))
        self.reviewDate.setText(QCoreApplication.translate("MainWindow", u"Date ", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"TIME:", None))
        self.reviewTime.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.acceptAppointmentBtn.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.declineAppointmentBtn.setText(QCoreApplication.translate("MainWindow", u"Decline", None))
        self.pageHeader6.setText(QCoreApplication.translate("MainWindow", u"SETTINGS", None))
        self.clinicIconP6.setText("")
        self.profileTabBtn.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.securityTabBtn.setText(QCoreApplication.translate("MainWindow", u"Security", None))
        self.preferencesTabBtn.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.UserManagementTabBtn.setText(QCoreApplication.translate("MainWindow", u"User Management", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Profile Info", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Full Name", None))
        self.profileFullName.setText(QCoreApplication.translate("MainWindow", u"Dredd Domasian", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"User Name", None))
        self.profileUserName.setText(QCoreApplication.translate("MainWindow", u"TheSauceGod", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.profileEmail.setText(QCoreApplication.translate("MainWindow", u"DomasianDredd@Gmail.com", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Phone", None))
        self.profilePhone.setText(QCoreApplication.translate("MainWindow", u"09272483891", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Account Info", None))
        self.accountRole.setText(QCoreApplication.translate("MainWindow", u"Role: Staff/Admin", None))
        self.MemberSince.setText(QCoreApplication.translate("MainWindow", u"Member Since: Jan 2024 ", None))
        self.settingsProfileEditBtn.setText(QCoreApplication.translate("MainWindow", u"Edit Profile", None))
        self.settingsProfileSaveBtn.setText(QCoreApplication.translate("MainWindow", u"Save Changes", None))
        self.settingsProfileCancelBtn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Change Password", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Current Password:", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"New Password:", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Confirm Passowrd:", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Change Password", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"PREFERENCES TAB", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"USER MANAGEMENT TAB (ADMIN ONLY)", None))
        self.pageHeader7.setText(QCoreApplication.translate("MainWindow", u"NOTIFICATIONS", None))
        self.clinicIconP7.setText("")
    # retranslateUi


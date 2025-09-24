# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appointmentCard.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(793, 81)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 5, 0)
        self.appointmentRecord = QFrame(Form)
        self.appointmentRecord.setObjectName(u"appointmentRecord")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appointmentRecord.sizePolicy().hasHeightForWidth())
        self.appointmentRecord.setSizePolicy(sizePolicy)
        self.appointmentRecord.setMinimumSize(QSize(0, 0))
        self.appointmentRecord.setMaximumSize(QSize(16777215, 81))
        self.appointmentRecord.setStyleSheet(u"#appointmentRecord{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"	border-bottom:1px solid rgb(185, 185, 185);\n"
"	border-right:1px solid rgb(185, 185, 185);\n"
"}\n"
"\n"
"\n"
"#appointmentRecord:hover{\n"
"	background-color:rgb(179, 179, 179);\n"
"}")
        self.appointmentRecord.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.appointmentRecord)
        self.horizontalLayout.setSpacing(25)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.profileIcon = QLabel(self.appointmentRecord)
        self.profileIcon.setObjectName(u"profileIcon")
        self.profileIcon.setMaximumSize(QSize(40, 40))
        self.profileIcon.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.profileIcon.setScaledContents(True)

        self.horizontalLayout.addWidget(self.profileIcon)

        self.ownerName = QLabel(self.appointmentRecord)
        self.ownerName.setObjectName(u"ownerName")
        self.ownerName.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")
        self.ownerName.setWordWrap(True)

        self.horizontalLayout.addWidget(self.ownerName)

        self.petNameApp = QLabel(self.appointmentRecord)
        self.petNameApp.setObjectName(u"petNameApp")
        self.petNameApp.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")
        self.petNameApp.setAlignment(Qt.AlignCenter)
        self.petNameApp.setWordWrap(True)

        self.horizontalLayout.addWidget(self.petNameApp)

        self.serviceApp = QLabel(self.appointmentRecord)
        self.serviceApp.setObjectName(u"serviceApp")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.serviceApp.sizePolicy().hasHeightForWidth())
        self.serviceApp.setSizePolicy(sizePolicy1)
        self.serviceApp.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")
        self.serviceApp.setAlignment(Qt.AlignCenter)
        self.serviceApp.setWordWrap(True)

        self.horizontalLayout.addWidget(self.serviceApp)

        self.appDate = QLabel(self.appointmentRecord)
        self.appDate.setObjectName(u"appDate")
        self.appDate.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")
        self.appDate.setAlignment(Qt.AlignCenter)
        self.appDate.setWordWrap(True)

        self.horizontalLayout.addWidget(self.appDate)

        self.preferredTime = QLabel(self.appointmentRecord)
        self.preferredTime.setObjectName(u"preferredTime")
        self.preferredTime.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")
        self.preferredTime.setAlignment(Qt.AlignCenter)
        self.preferredTime.setWordWrap(True)

        self.horizontalLayout.addWidget(self.preferredTime)

        self.deleteButton = QToolButton(self.appointmentRecord)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setStyleSheet(u"background:transparent;\n"
"border:none;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.deleteButton)


        self.verticalLayout.addWidget(self.appointmentRecord)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.profileIcon.setText("")
        self.ownerName.setText(QCoreApplication.translate("Form", u"Robert Moleno", None))
        self.petNameApp.setText(QCoreApplication.translate("Form", u"Petname", None))
        self.serviceApp.setText(QCoreApplication.translate("Form", u"Service", None))
        self.appDate.setText(QCoreApplication.translate("Form", u"Aug, 2, 2025", None))
        self.preferredTime.setText(QCoreApplication.translate("Form", u"11:45 AM", None))
        self.deleteButton.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi


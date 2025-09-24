# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'webAppointmentCard.ui'
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
    QPushButton, QSizePolicy, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 81)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 5, 0)
        self.webAppointmentFrame = QFrame(Form)
        self.webAppointmentFrame.setObjectName(u"webAppointmentFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webAppointmentFrame.sizePolicy().hasHeightForWidth())
        self.webAppointmentFrame.setSizePolicy(sizePolicy)
        self.webAppointmentFrame.setMaximumSize(QSize(16777215, 81))
        self.webAppointmentFrame.setStyleSheet(u"#webAppointmentFrame{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"	border-bottom:1px solid rgb(185, 185, 185);\n"
"	border-right:1px solid rgb(185, 185, 185);\n"
"}\n"
"\n"
"")
        self.webAppointmentFrame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_35 = QHBoxLayout(self.webAppointmentFrame)
        self.horizontalLayout_35.setSpacing(25)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(20, 20, 20, 20)
        self.profileIcon = QLabel(self.webAppointmentFrame)
        self.profileIcon.setObjectName(u"profileIcon")
        self.profileIcon.setMaximumSize(QSize(40, 40))
        self.profileIcon.setStyleSheet(u"")
        self.profileIcon.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.profileIcon.setScaledContents(True)

        self.horizontalLayout_35.addWidget(self.profileIcon)

        self.ownerName = QLabel(self.webAppointmentFrame)
        self.ownerName.setObjectName(u"ownerName")
        self.ownerName.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")

        self.horizontalLayout_35.addWidget(self.ownerName)

        self.DateTime = QLabel(self.webAppointmentFrame)
        self.DateTime.setObjectName(u"DateTime")
        self.DateTime.setStyleSheet(u"	font: 57 14pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"")

        self.horizontalLayout_35.addWidget(self.DateTime)

        self.ReviewButton = QPushButton(self.webAppointmentFrame)
        self.ReviewButton.setObjectName(u"ReviewButton")
        self.ReviewButton.setStyleSheet(u"QPushButton{\n"
"	font: 57 14pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color: #FCD597;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"border-radius: 10px;\n"
"}")

        self.horizontalLayout_35.addWidget(self.ReviewButton)


        self.horizontalLayout.addWidget(self.webAppointmentFrame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.profileIcon.setText("")
        self.ownerName.setText(QCoreApplication.translate("Form", u"Robert Moleno", None))
        self.DateTime.setText(QCoreApplication.translate("Form", u"Date and Time", None))
        self.ReviewButton.setText(QCoreApplication.translate("Form", u"Review", None))
    # retranslateUi


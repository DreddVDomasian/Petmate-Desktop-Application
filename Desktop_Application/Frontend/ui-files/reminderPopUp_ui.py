# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reminderPopUp.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(813, 511)
        Form.setStyleSheet(u"background-color:rgb(255, 255, 255);")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.remidersChecklists = QFrame(Form)
        self.remidersChecklists.setObjectName(u"remidersChecklists")
        self.remidersChecklists.setStyleSheet(u"#remidersChecklists{\n"
"	border-radius:15px;	background-color: qlineargradient(\n"
"		 y1: 0, x1: 0, y2: 1, x2: 0,\n"
"		 stop: 0 #78B3CE, \n"
"    	 stop: 1 #D0F0FF\n"
"	);\n"
"}")
        self.remidersChecklists.setFrameShape(QFrame.StyledPanel)
        self.remidersChecklists.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.remidersChecklists)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleReminderFrame = QFrame(self.remidersChecklists)
        self.titleReminderFrame.setObjectName(u"titleReminderFrame")
        self.titleReminderFrame.setStyleSheet(u"background:none;")
        self.titleReminderFrame.setFrameShape(QFrame.StyledPanel)
        self.titleReminderFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.titleReminderFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.remiderIcon = QPushButton(self.titleReminderFrame)
        self.remiderIcon.setObjectName(u"remiderIcon")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remiderIcon.sizePolicy().hasHeightForWidth())
        self.remiderIcon.setSizePolicy(sizePolicy)
        self.remiderIcon.setStyleSheet(u"background:none;\n"
"border:none;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/checklist.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.remiderIcon.setIcon(icon)
        self.remiderIcon.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.remiderIcon, 0, Qt.AlignLeft)

        self.reminderForLabel = QLabel(self.titleReminderFrame)
        self.reminderForLabel.setObjectName(u"reminderForLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.reminderForLabel.sizePolicy().hasHeightForWidth())
        self.reminderForLabel.setSizePolicy(sizePolicy1)
        self.reminderForLabel.setStyleSheet(u"font: 81 16pt \"Montserrat ExtraBold\";\n"
"color:rgb(0, 0, 0);")
        self.reminderForLabel.setScaledContents(True)
        self.reminderForLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.reminderForLabel.setWordWrap(False)

        self.horizontalLayout.addWidget(self.reminderForLabel, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.titleReminderFrame, 0, Qt.AlignTop)

        self.reminderScrollArea = QScrollArea(self.remidersChecklists)
        self.reminderScrollArea.setObjectName(u"reminderScrollArea")
        self.reminderScrollArea.setStyleSheet(u"#reminderScrollArea{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border-radius: 5px;\n"
"    min-height: 50px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(86, 127, 145);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar::groove:vertical {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.reminderScrollArea.setWidgetResizable(True)
        self.reminderScrollAreaContents = QWidget()
        self.reminderScrollAreaContents.setObjectName(u"reminderScrollAreaContents")
        self.reminderScrollAreaContents.setGeometry(QRect(0, 0, 777, 368))
        self.reminderScrollAreaContents.setStyleSheet(u"background-color:transparent;")
        self.verticalLayout_3 = QVBoxLayout(self.reminderScrollAreaContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.reminderScrollArea.setWidget(self.reminderScrollAreaContents)

        self.verticalLayout.addWidget(self.reminderScrollArea)

        self.frame = QFrame(self.remidersChecklists)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.DoneBtn = QPushButton(self.frame)
        self.DoneBtn.setObjectName(u"DoneBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.DoneBtn.sizePolicy().hasHeightForWidth())
        self.DoneBtn.setSizePolicy(sizePolicy2)
        self.DoneBtn.setMinimumSize(QSize(0, 40))
        self.DoneBtn.setStyleSheet(u"QPushButton{\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color: #FCD597;\n"
"	border-radius: 5px;\n"
"	border-right:1px solid rgb(200, 200, 200);\n"
"	border-bottom:2px solid rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"\n"
"}")

        self.horizontalLayout_2.addWidget(self.DoneBtn)


        self.verticalLayout.addWidget(self.frame)


        self.verticalLayout_2.addWidget(self.remidersChecklists)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.remiderIcon.setText("")
        self.reminderForLabel.setText(QCoreApplication.translate("Form", u"REMINDER FOR PETNAME", None))
        self.DoneBtn.setText(QCoreApplication.translate("Form", u"DONE", None))
    # retranslateUi


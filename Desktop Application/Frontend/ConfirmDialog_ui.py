# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConfirmDialog.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(450, 200)
        Form.setMinimumSize(QSize(450, 200))
        Form.setMaximumSize(QSize(450, 200))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.confirmation = QFrame(Form)
        self.confirmation.setObjectName(u"confirmation")
        self.confirmation.setStyleSheet(u"#confirmation{\n"
"	border-radius:15px;\n"
"	background-color:rgb(255, 255, 255);\n"
"	border-bottom:1px solid rgb(199, 199, 199);\n"
"}")
        self.confirmation.setFrameShape(QFrame.StyledPanel)
        self.confirmation.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.confirmation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.confirmation)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color:transparent;\n"
"border:none;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.confirmationMessage = QLabel(self.frame_2)
        self.confirmationMessage.setObjectName(u"confirmationMessage")
        self.confirmationMessage.setStyleSheet(u"#confirmationMessage{\n"
"	font: 57 16pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"\n"
"}")
        self.confirmationMessage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.confirmationMessage)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.confirmation)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"\n"
"background-color:transparent;\n"
"border:none;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(40)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.yesButton = QPushButton(self.frame)
        self.yesButton.setObjectName(u"yesButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yesButton.sizePolicy().hasHeightForWidth())
        self.yesButton.setSizePolicy(sizePolicy)
        self.yesButton.setStyleSheet(u"#yesButton{\n"
"	padding:5px 25px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	border:none;\n"
"	border-radius:10px;\n"
"	background-color:	rgb(220, 90, 90);\n"
"}\n"
"#yesButton:hover{\n"
"	background-color:rgb(180, 120, 125);\n"
"}")

        self.horizontalLayout_2.addWidget(self.yesButton)

        self.noButton = QPushButton(self.frame)
        self.noButton.setObjectName(u"noButton")
        sizePolicy.setHeightForWidth(self.noButton.sizePolicy().hasHeightForWidth())
        self.noButton.setSizePolicy(sizePolicy)
        self.noButton.setStyleSheet(u"#noButton{\n"
"	padding:5px 25px;\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	border:none;\n"
"	border-radius:10px;\n"
"	background-color:rgb(129, 191, 218);\n"
"}	\n"
"\n"
"#noButton:hover{\n"
"	background-color:rgb(110, 163, 186);\n"
"\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.noButton)


        self.verticalLayout.addWidget(self.frame, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.confirmation)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.confirmationMessage.setText(QCoreApplication.translate("Form", u"Are you sure you want to delete \n"
"this record?", None))
        self.yesButton.setText(QCoreApplication.translate("Form", u"YES", None))
        self.noButton.setText(QCoreApplication.translate("Form", u"NO", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'duplicateCard.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(873, 255)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.duplicateCard = QFrame(Form)
        self.duplicateCard.setObjectName(u"duplicateCard")
        self.duplicateCard.setStyleSheet(u"#duplicateCard{\n"
"	border-radius:15px;\n"
"	background-color:rgb(231, 231, 231);\n"
"\n"
"}")
        self.duplicateCard.setFrameShape(QFrame.StyledPanel)
        self.duplicateCard.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.duplicateCard)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.frame_2 = QFrame(self.duplicateCard)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background:transparent;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.duplicateUpdateBtn = QPushButton(self.frame_2)
        self.duplicateUpdateBtn.setObjectName(u"duplicateUpdateBtn")
        self.duplicateUpdateBtn.setStyleSheet(u"QPushButton{\n"
"	font: 57 11pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color: #FCD597;\n"
"	border-radius: 10px;\n"
"	padding:10px 20px 10px 20px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(223, 188, 134);\n"
"border-radius: 10px;\n"
"}")

        self.horizontalLayout_2.addWidget(self.duplicateUpdateBtn)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 2, Qt.AlignHCenter|Qt.AlignBottom)

        self.frame_3 = QFrame(self.duplicateCard)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(415, 16777215))
        self.frame_3.setStyleSheet(u"background:transparent;")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 14pt \"Rubik Mono One\";\n"
"color:rgb(39,39,39);")

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout_2.addWidget(self.frame_4, 0, Qt.AlignTop)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.frame_5)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea{\n"
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
"    min-height: 10px;\n"
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
"    background-color: rgb(129, 191, 218);\n"
"    border-radi"
                        "us: 5px;\n"
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
        self.scrollArea.setWidgetResizable(True)
        self.petsScrollAreaWidgetContents = QWidget()
        self.petsScrollAreaWidgetContents.setObjectName(u"petsScrollAreaWidgetContents")
        self.petsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 385, 132))
        self.verticalLayout_3 = QVBoxLayout(self.petsScrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.petsScrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 57 11pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_3.addWidget(self.label)

        self.label_3 = QLabel(self.petsScrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 57 11pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.petsScrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 57 11pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.petsScrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 57 11pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_3.addWidget(self.label_5)

        self.scrollArea.setWidget(self.petsScrollAreaWidgetContents)

        self.horizontalLayout_4.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.frame_5)


        self.gridLayout.addWidget(self.frame_3, 0, 1, 1, 1)

        self.frame = QFrame(self.duplicateCard)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"font: 57 11pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);\n"
"background:transparent;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fullnameLabel = QLabel(self.frame)
        self.fullnameLabel.setObjectName(u"fullnameLabel")

        self.verticalLayout.addWidget(self.fullnameLabel)

        self.emailLabel = QLabel(self.frame)
        self.emailLabel.setObjectName(u"emailLabel")

        self.verticalLayout.addWidget(self.emailLabel)

        self.address = QLabel(self.frame)
        self.address.setObjectName(u"address")

        self.verticalLayout.addWidget(self.address)

        self.contactNo = QLabel(self.frame)
        self.contactNo.setObjectName(u"contactNo")

        self.verticalLayout.addWidget(self.contactNo)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.duplicateCard)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.duplicateUpdateBtn.setText(QCoreApplication.translate("Form", u"Update this record", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"PETS:", None))
        self.label.setText(QCoreApplication.translate("Form", u"OREO", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"TREVOR", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"SCOTTIE", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.fullnameLabel.setText(QCoreApplication.translate("Form", u"Domasian, Dredd Villarba", None))
        self.emailLabel.setText(QCoreApplication.translate("Form", u"DomasianDredd@gmail.com", None))
        self.address.setText(QCoreApplication.translate("Form", u"San Francisco, General Trias Cavite", None))
        self.contactNo.setText(QCoreApplication.translate("Form", u"09272483891/038265186", None))
    # retranslateUi


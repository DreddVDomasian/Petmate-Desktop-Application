# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reminderCard.ui'
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
import resource_rc
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(770, 75)
        Form.setMaximumSize(QSize(770, 16777215))
        Form.setStyleSheet(u"border-radius:10px;")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.reminderCard = QFrame(Form)
        self.reminderCard.setObjectName(u"reminderCard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reminderCard.sizePolicy().hasHeightForWidth())
        self.reminderCard.setSizePolicy(sizePolicy)
        self.reminderCard.setMinimumSize(QSize(0, 0))
        self.reminderCard.setMaximumSize(QSize(770, 81))
        self.reminderCard.setStyleSheet(u"#reminderCard{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"\n"
"}\n"
"\n"
"QLabel{\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(52, 52, 52);\n"
"	background:none;\n"
"\n"
"}\n"
"\n"
"\n"
"")
        self.reminderCard.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.reminderCard)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(15, 15, 15, 15)
        self.typeReq = QLabel(self.reminderCard)
        self.typeReq.setObjectName(u"typeReq")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.typeReq.sizePolicy().hasHeightForWidth())
        self.typeReq.setSizePolicy(sizePolicy1)
        self.typeReq.setStyleSheet(u"font: 81 12pt \"Montserrat ExtraBold\";\n"
"	color:rgb(52, 52, 52);\n"
"background:none;")
        self.typeReq.setWordWrap(True)

        self.horizontalLayout.addWidget(self.typeReq, 0, Qt.AlignHCenter)

        self.dateReq = QLabel(self.reminderCard)
        self.dateReq.setObjectName(u"dateReq")
        sizePolicy1.setHeightForWidth(self.dateReq.sizePolicy().hasHeightForWidth())
        self.dateReq.setSizePolicy(sizePolicy1)
        self.dateReq.setStyleSheet(u"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(52, 52, 52);\n"
"	background:none;")
        self.dateReq.setAlignment(Qt.AlignCenter)
        self.dateReq.setWordWrap(True)

        self.horizontalLayout.addWidget(self.dateReq, 0, Qt.AlignHCenter)

        self.timeOptional = QLabel(self.reminderCard)
        self.timeOptional.setObjectName(u"timeOptional")
        sizePolicy1.setHeightForWidth(self.timeOptional.sizePolicy().hasHeightForWidth())
        self.timeOptional.setSizePolicy(sizePolicy1)
        self.timeOptional.setStyleSheet(u"")
        self.timeOptional.setAlignment(Qt.AlignCenter)
        self.timeOptional.setWordWrap(True)

        self.horizontalLayout.addWidget(self.timeOptional)

        self.serviceOptional = QLabel(self.reminderCard)
        self.serviceOptional.setObjectName(u"serviceOptional")
        sizePolicy1.setHeightForWidth(self.serviceOptional.sizePolicy().hasHeightForWidth())
        self.serviceOptional.setSizePolicy(sizePolicy1)
        self.serviceOptional.setStyleSheet(u"")
        self.serviceOptional.setAlignment(Qt.AlignCenter)
        self.serviceOptional.setWordWrap(True)

        self.horizontalLayout.addWidget(self.serviceOptional, 0, Qt.AlignHCenter)

        self.markAsDone = QPushButton(self.reminderCard)
        self.markAsDone.setObjectName(u"markAsDone")
        self.markAsDone.setMaximumSize(QSize(154, 16777215))
        self.markAsDone.setStyleSheet(u"#markAsDone{\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(52, 52, 52);\n"
"	background:none;\n"
"	padding:10px 20px 10px 20px;\n"
"	border:none;\n"
"	border-radius:15px;\n"
"	background-color:rgb(129, 191, 218);\n"
"}\n"
"\n"
"#markAsDone:hover{\n"
"	background-color:rgb(109, 164, 185);\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.markAsDone)


        self.verticalLayout.addWidget(self.reminderCard)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.typeReq.setText(QCoreApplication.translate("Form", u"TYPE", None))
        self.dateReq.setText(QCoreApplication.translate("Form", u"DATE", None))
        self.timeOptional.setText(QCoreApplication.translate("Form", u"TIME", None))
        self.serviceOptional.setText(QCoreApplication.translate("Form", u"SERVICE", None))
        self.markAsDone.setText(QCoreApplication.translate("Form", u"Mark as Done", None))
    # retranslateUi


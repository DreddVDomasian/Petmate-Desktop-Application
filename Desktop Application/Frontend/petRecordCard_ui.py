# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'petRecordCard.ui'
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
    QSizePolicy, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(419, 100)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.petRecordCard = QFrame(Form)
        self.petRecordCard.setObjectName(u"petRecordCard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.petRecordCard.sizePolicy().hasHeightForWidth())
        self.petRecordCard.setSizePolicy(sizePolicy)
        self.petRecordCard.setMinimumSize(QSize(401, 100))
        self.petRecordCard.setStyleSheet(u"#petRecordCard{\n"
"	border-radius:15px;\n"
"	background-color:rgb(244, 244, 244);\n"
"\n"
"}\n"
"#petRecordCard:hover{\n"
"	background-color:rgb(226, 226, 226);\n"
"\n"
"}")
        self.petRecordCard.setFrameShape(QFrame.StyledPanel)
        self.petRecordCard.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.petRecordCard)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 0, 0, 0)
        self.petCardIcon = QLabel(self.petRecordCard)
        self.petCardIcon.setObjectName(u"petCardIcon")
        self.petCardIcon.setMinimumSize(QSize(30, 30))
        self.petCardIcon.setMaximumSize(QSize(60, 60))
        self.petCardIcon.setPixmap(QPixmap(u"Icons/catIcon.png"))
        self.petCardIcon.setScaledContents(True)

        self.horizontalLayout.addWidget(self.petCardIcon)

        self.petNameCard = QLabel(self.petRecordCard)
        self.petNameCard.setObjectName(u"petNameCard")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.petNameCard.sizePolicy().hasHeightForWidth())
        self.petNameCard.setSizePolicy(sizePolicy1)
        self.petNameCard.setMinimumSize(QSize(318, 0))
        self.petNameCard.setStyleSheet(u"font: 22pt \"Montserrat Black\";\n"
"color:rgb(39, 39, 39);")
        self.petNameCard.setScaledContents(False)
        self.petNameCard.setAlignment(Qt.AlignCenter)
        self.petNameCard.setWordWrap(True)

        self.horizontalLayout.addWidget(self.petNameCard)


        self.horizontalLayout_2.addWidget(self.petRecordCard, 0, Qt.AlignTop)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.petCardIcon.setText("")
        self.petNameCard.setText(QCoreApplication.translate("Form", u"Petname", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'schedCard.ui'
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
    QSizePolicy, QToolButton, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(853, 81)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 5, 0)
        self.SchedCard = QFrame(Form)
        self.SchedCard.setObjectName(u"SchedCard")
        sizePolicy.setHeightForWidth(self.SchedCard.sizePolicy().hasHeightForWidth())
        self.SchedCard.setSizePolicy(sizePolicy)
        self.SchedCard.setMinimumSize(QSize(0, 81))
        self.SchedCard.setMaximumSize(QSize(16777215, 81))
        self.SchedCard.setStyleSheet(u"#SchedCard{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"\n"
"}\n"
"#SchedCard:hover{\n"
"	background-color:#FBD496;\n"
"}")
        self.SchedCard.setFrameShape(QFrame.StyledPanel)
        self.SchedCard.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.SchedCard)
        self.horizontalLayout_2.setSpacing(25)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.SchedCardProfileIcon = QLabel(self.SchedCard)
        self.SchedCardProfileIcon.setObjectName(u"SchedCardProfileIcon")
        self.SchedCardProfileIcon.setMaximumSize(QSize(40, 40))
        self.SchedCardProfileIcon.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.SchedCardProfileIcon.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.SchedCardProfileIcon)

        self.ReturnNameLabel = QLabel(self.SchedCard)
        self.ReturnNameLabel.setObjectName(u"ReturnNameLabel")
        self.ReturnNameLabel.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")
        self.ReturnNameLabel.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.ReturnNameLabel)

        self.petName = QLabel(self.SchedCard)
        self.petName.setObjectName(u"petName")
        self.petName.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")
        self.petName.setAlignment(Qt.AlignCenter)
        self.petName.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.petName)

        self.ReturnServiceLabel = QLabel(self.SchedCard)
        self.ReturnServiceLabel.setObjectName(u"ReturnServiceLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ReturnServiceLabel.sizePolicy().hasHeightForWidth())
        self.ReturnServiceLabel.setSizePolicy(sizePolicy1)
        self.ReturnServiceLabel.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")
        self.ReturnServiceLabel.setAlignment(Qt.AlignCenter)
        self.ReturnServiceLabel.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.ReturnServiceLabel)

        self.ReturnDateCardLabel = QLabel(self.SchedCard)
        self.ReturnDateCardLabel.setObjectName(u"ReturnDateCardLabel")
        self.ReturnDateCardLabel.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")
        self.ReturnDateCardLabel.setAlignment(Qt.AlignCenter)
        self.ReturnDateCardLabel.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.ReturnDateCardLabel)

        self.deleteButton = QToolButton(self.SchedCard)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setStyleSheet(u"background:transparent;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon)
        self.deleteButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.deleteButton)


        self.horizontalLayout.addWidget(self.SchedCard)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SchedCardProfileIcon.setText("")
        self.ReturnNameLabel.setText(QCoreApplication.translate("Form", u"Robert Moleno", None))
        self.petName.setText(QCoreApplication.translate("Form", u"Petname", None))
        self.ReturnServiceLabel.setText(QCoreApplication.translate("Form", u"Check up", None))
        self.ReturnDateCardLabel.setText(QCoreApplication.translate("Form", u"Aug 1, 2025", None))
        self.deleteButton.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi


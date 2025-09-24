# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PatientCard.ui'
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
    QLayout, QSizePolicy, QToolButton, QWidget)
import resource_rc
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(980, 81)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 81))
        Form.setMaximumSize(QSize(16777215, 81))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 5, 0)
        self.RecordList = QFrame(Form)
        self.RecordList.setObjectName(u"RecordList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RecordList.sizePolicy().hasHeightForWidth())
        self.RecordList.setSizePolicy(sizePolicy1)
        self.RecordList.setMaximumSize(QSize(16777215, 81))
        self.RecordList.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.RecordList.setStyleSheet(u"#RecordList{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"}\n"
"#RecordList:hover{\n"
"	background-color:rgb(179, 179, 179);\n"
"}")
        self.RecordList.setFrameShape(QFrame.StyledPanel)
        self.RecordList.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.RecordList)
        self.horizontalLayout_8.setSpacing(25)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setContentsMargins(20, 20, 20, 20)
        self.profileIcon = QLabel(self.RecordList)
        self.profileIcon.setObjectName(u"profileIcon")
        self.profileIcon.setMaximumSize(QSize(40, 40))
        self.profileIcon.setStyleSheet(u"")
        self.profileIcon.setPixmap(QPixmap(u":/Icons/Icons/UserIcon.png"))
        self.profileIcon.setScaledContents(True)

        self.horizontalLayout_8.addWidget(self.profileIcon)

        self.nameLabel = QLabel(self.RecordList)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(57, 57, 57);")

        self.horizontalLayout_8.addWidget(self.nameLabel, 0, Qt.AlignLeft)

        self.emailLabel = QLabel(self.RecordList)
        self.emailLabel.setObjectName(u"emailLabel")
        self.emailLabel.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout_8.addWidget(self.emailLabel, 0, Qt.AlignHCenter)

        self.actionBtn = QFrame(self.RecordList)
        self.actionBtn.setObjectName(u"actionBtn")
        self.actionBtn.setStyleSheet(u"border:none;\n"
"background:transparent;")
        self.actionBtn.setFrameShape(QFrame.StyledPanel)
        self.actionBtn.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.actionBtn)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.editBtn = QToolButton(self.actionBtn)
        self.editBtn.setObjectName(u"editBtn")
        self.editBtn.setStyleSheet(u"background:transparent;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/UpdateIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editBtn.setIcon(icon)
        self.editBtn.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.editBtn, 0, Qt.AlignRight)

        self.deleteButton = QToolButton(self.actionBtn)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setStyleSheet(u"background:transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon1)
        self.deleteButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.deleteButton)


        self.horizontalLayout_8.addWidget(self.actionBtn, 0, Qt.AlignRight)


        self.horizontalLayout.addWidget(self.RecordList, 0, Qt.AlignTop)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.profileIcon.setText("")
        self.nameLabel.setText(QCoreApplication.translate("Form", u"Dredd Domasian", None))
        self.emailLabel.setText(QCoreApplication.translate("Form", u"DomasianDredd@gmail.com", None))
        self.editBtn.setText(QCoreApplication.translate("Form", u"...", None))
        self.deleteButton.setText(QCoreApplication.translate("Form", u"...", None))
    # retranslateUi


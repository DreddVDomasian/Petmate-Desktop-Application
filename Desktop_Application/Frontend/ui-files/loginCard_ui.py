# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginCard.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1055, 750)
        Form.setMinimumSize(QSize(1055, 750))
        Form.setMaximumSize(QSize(1055, 750))
        icon = QIcon()
        icon.addFile(u":/images/image/desktopIcon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"QFrame{\n"
"	background:transparent;\n"
"	border:none;\n"
"}")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.loginFrame = QFrame(Form)
        self.loginFrame.setObjectName(u"loginFrame")
        self.loginFrame.setStyleSheet(u"#loginFrame{\n"
"\n"
"	\n"
"	background-image: url(:/images/image/loginBG.png);\n"
"\n"
"}")
        self.loginFrame.setFrameShape(QFrame.StyledPanel)
        self.loginFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.loginFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.loginFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.closeLoginBtn = QPushButton(self.frame)
        self.closeLoginBtn.setObjectName(u"closeLoginBtn")
        self.closeLoginBtn.setStyleSheet(u"#closeLoginBtn{\n"
"	background:transparent;\n"
"	border:none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeLoginBtn.setIcon(icon1)
        self.closeLoginBtn.setIconSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.closeLoginBtn)


        self.verticalLayout_2.addWidget(self.frame, 0, Qt.AlignRight|Qt.AlignTop)

        self.frame_2 = QFrame(self.loginFrame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 500))
        self.frame_2.setStyleSheet(u"QLineEdit{\n"
"	border-top-right-radius:25px;\n"
"	border-bottom-right-radius:25px;\n"
"	background-color:#ECECEC;\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	padding-left:10px;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(50, -1, -1, 100)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.userIcon = QFrame(self.frame_3)
        self.userIcon.setObjectName(u"userIcon")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.userIcon.sizePolicy().hasHeightForWidth())
        self.userIcon.setSizePolicy(sizePolicy1)
        self.userIcon.setMaximumSize(QSize(60, 70))
        self.userIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.userIcon.setFrameShape(QFrame.StyledPanel)
        self.userIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.userIcon)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(25, 15, 0, 15)
        self.label = QLabel(self.userIcon)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/Icons/Icons/usernameIcon.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.userIcon)

        self.loginUserName = QLineEdit(self.frame_3)
        self.loginUserName.setObjectName(u"loginUserName")
        sizePolicy1.setHeightForWidth(self.loginUserName.sizePolicy().hasHeightForWidth())
        self.loginUserName.setSizePolicy(sizePolicy1)
        self.loginUserName.setMinimumSize(QSize(533, 70))
        self.loginUserName.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.loginUserName)


        self.verticalLayout_3.addWidget(self.frame_3, 0, Qt.AlignLeft)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.passwordIcon = QFrame(self.frame_4)
        self.passwordIcon.setObjectName(u"passwordIcon")
        sizePolicy1.setHeightForWidth(self.passwordIcon.sizePolicy().hasHeightForWidth())
        self.passwordIcon.setSizePolicy(sizePolicy1)
        self.passwordIcon.setMinimumSize(QSize(40, 70))
        self.passwordIcon.setMaximumSize(QSize(60, 70))
        self.passwordIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.passwordIcon.setFrameShape(QFrame.StyledPanel)
        self.passwordIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.passwordIcon)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(25, 15, 5, 15)
        self.label_2 = QLabel(self.passwordIcon)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u":/Icons/Icons/lockIcon.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.label_2)


        self.horizontalLayout_2.addWidget(self.passwordIcon)

        self.loginPassword = QLineEdit(self.frame_4)
        self.loginPassword.setObjectName(u"loginPassword")
        sizePolicy1.setHeightForWidth(self.loginPassword.sizePolicy().hasHeightForWidth())
        self.loginPassword.setSizePolicy(sizePolicy1)
        self.loginPassword.setMinimumSize(QSize(533, 70))
        self.loginPassword.setDragEnabled(False)

        self.horizontalLayout_2.addWidget(self.loginPassword)


        self.verticalLayout_3.addWidget(self.frame_4, 0, Qt.AlignLeft)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy1.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy1)
        self.frame_5.setMinimumSize(QSize(595, 0))
        self.frame_5.setMaximumSize(QSize(595, 16777215))
        self.frame_5.setStyleSheet(u"font: 57 10pt \"Montserrat Medium\";")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_5)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.staySignedIn = QCheckBox(self.frame_6)
        self.staySignedIn.setObjectName(u"staySignedIn")

        self.horizontalLayout_7.addWidget(self.staySignedIn)


        self.horizontalLayout_8.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 57 10pt \"Montserrat Medium\";\n"
"text-decoration: underline;")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_3)


        self.horizontalLayout_8.addWidget(self.frame_7)


        self.verticalLayout_3.addWidget(self.frame_5, 0, Qt.AlignLeft)

        self.loginBtn = QPushButton(self.frame_2)
        self.loginBtn.setObjectName(u"loginBtn")
        sizePolicy1.setHeightForWidth(self.loginBtn.sizePolicy().hasHeightForWidth())
        self.loginBtn.setSizePolicy(sizePolicy1)
        self.loginBtn.setMinimumSize(QSize(595, 0))
        self.loginBtn.setStyleSheet(u"QPushButton{\n"
"	padding:5px;\n"
"	background-color:#0C8AA7;\n"
"	border:none;\n"
"	border-radius:20px;\n"
"	font: 87 20pt \"Montserrat Black\";\n"
"	color:rgb(255, 255, 255);\n"
"}")

        self.verticalLayout_3.addWidget(self.loginBtn)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.loginFrame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.closeLoginBtn.setText("")
        self.label.setText("")
        self.loginUserName.setPlaceholderText(QCoreApplication.translate("Form", u"Enter username", None))
        self.label_2.setText("")
        self.loginPassword.setPlaceholderText(QCoreApplication.translate("Form", u"Enter password", None))
        self.staySignedIn.setText(QCoreApplication.translate("Form", u"Stay signed in", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Forgot password?", None))
        self.loginBtn.setText(QCoreApplication.translate("Form", u"LOG IN", None))
        pass
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'firstTime-setup.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
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
        self.firstLoginFrame = QFrame(Form)
        self.firstLoginFrame.setObjectName(u"firstLoginFrame")
        self.firstLoginFrame.setStyleSheet(u"#firstLoginFrame{\n"
"	background-image: url(:/images/image/loginBG.png);\n"
"}")
        self.firstLoginFrame.setFrameShape(QFrame.StyledPanel)
        self.firstLoginFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.firstLoginFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.firstLoginFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.close = QPushButton(self.frame)
        self.close.setObjectName(u"close")
        self.close.setStyleSheet(u"#close{\n"
"	background:transparent;\n"
"	border:none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close.setIcon(icon1)
        self.close.setIconSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.close)


        self.verticalLayout_2.addWidget(self.frame, 0, Qt.AlignRight|Qt.AlignTop)

        self.frame_2 = QFrame(self.firstLoginFrame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 500))
        self.frame_2.setStyleSheet(u"QLineEdit{\n"
"	border-top-right-radius:25px;\n"
"	border-bottom-right-radius:25px;\n"
"	background-color:#ECECEC;\n"
"	font: 63 15pt \"Montserrat SemiBold\";\n"
"	padding-left:10px;\n"
"	padding-right:5px;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, -1, 0, 20)
        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(738, 0))
        self.label_9.setStyleSheet(u"	font: 87 20pt \"Montserrat Black\";\n"
"	color:rgb(52,52,52);")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_9)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fullnameUsernameFrame = QFrame(self.frame_5)
        self.fullnameUsernameFrame.setObjectName(u"fullnameUsernameFrame")
        sizePolicy.setHeightForWidth(self.fullnameUsernameFrame.sizePolicy().hasHeightForWidth())
        self.fullnameUsernameFrame.setSizePolicy(sizePolicy)
        self.fullnameUsernameFrame.setFrameShape(QFrame.StyledPanel)
        self.fullnameUsernameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.fullnameUsernameFrame)
        self.horizontalLayout_14.setSpacing(10)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.fullNameFrame = QFrame(self.fullnameUsernameFrame)
        self.fullNameFrame.setObjectName(u"fullNameFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fullNameFrame.sizePolicy().hasHeightForWidth())
        self.fullNameFrame.setSizePolicy(sizePolicy1)
        self.fullNameFrame.setFrameShape(QFrame.StyledPanel)
        self.fullNameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.fullNameFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.fullnameIcon = QFrame(self.fullNameFrame)
        self.fullnameIcon.setObjectName(u"fullnameIcon")
        sizePolicy.setHeightForWidth(self.fullnameIcon.sizePolicy().hasHeightForWidth())
        self.fullnameIcon.setSizePolicy(sizePolicy)
        self.fullnameIcon.setMaximumSize(QSize(60, 70))
        self.fullnameIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.fullnameIcon.setFrameShape(QFrame.StyledPanel)
        self.fullnameIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.fullnameIcon)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(25, 15, 0, 15)
        self.label = QLabel(self.fullnameIcon)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/Icons/Icons/usernameIcon.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.fullnameIcon)

        self.fullName = QLineEdit(self.fullNameFrame)
        self.fullName.setObjectName(u"fullName")
        sizePolicy.setHeightForWidth(self.fullName.sizePolicy().hasHeightForWidth())
        self.fullName.setSizePolicy(sizePolicy)
        self.fullName.setMinimumSize(QSize(300, 70))
        self.fullName.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.fullName)


        self.horizontalLayout_14.addWidget(self.fullNameFrame, 0, Qt.AlignLeft)

        self.usernameFrame = QFrame(self.fullnameUsernameFrame)
        self.usernameFrame.setObjectName(u"usernameFrame")
        sizePolicy1.setHeightForWidth(self.usernameFrame.sizePolicy().hasHeightForWidth())
        self.usernameFrame.setSizePolicy(sizePolicy1)
        self.usernameFrame.setFrameShape(QFrame.StyledPanel)
        self.usernameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.usernameFrame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.usernameIcon = QFrame(self.usernameFrame)
        self.usernameIcon.setObjectName(u"usernameIcon")
        sizePolicy.setHeightForWidth(self.usernameIcon.sizePolicy().hasHeightForWidth())
        self.usernameIcon.setSizePolicy(sizePolicy)
        self.usernameIcon.setMaximumSize(QSize(60, 70))
        self.usernameIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.usernameIcon.setFrameShape(QFrame.StyledPanel)
        self.usernameIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.usernameIcon)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(25, 15, 0, 15)
        self.label_2 = QLabel(self.usernameIcon)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u":/Icons/Icons/usernameIcon.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.label_2)


        self.horizontalLayout_2.addWidget(self.usernameIcon)

        self.username = QLineEdit(self.usernameFrame)
        self.username.setObjectName(u"username")
        sizePolicy.setHeightForWidth(self.username.sizePolicy().hasHeightForWidth())
        self.username.setSizePolicy(sizePolicy)
        self.username.setMinimumSize(QSize(300, 70))
        self.username.setDragEnabled(False)

        self.horizontalLayout_2.addWidget(self.username)


        self.horizontalLayout_14.addWidget(self.usernameFrame, 0, Qt.AlignRight)


        self.verticalLayout_4.addWidget(self.fullnameUsernameFrame)

        self.emailPhoneNumFrame = QFrame(self.frame_5)
        self.emailPhoneNumFrame.setObjectName(u"emailPhoneNumFrame")
        sizePolicy.setHeightForWidth(self.emailPhoneNumFrame.sizePolicy().hasHeightForWidth())
        self.emailPhoneNumFrame.setSizePolicy(sizePolicy)
        self.emailPhoneNumFrame.setFrameShape(QFrame.StyledPanel)
        self.emailPhoneNumFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.emailPhoneNumFrame)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.emailFrame = QFrame(self.emailPhoneNumFrame)
        self.emailFrame.setObjectName(u"emailFrame")
        sizePolicy1.setHeightForWidth(self.emailFrame.sizePolicy().hasHeightForWidth())
        self.emailFrame.setSizePolicy(sizePolicy1)
        self.emailFrame.setFrameShape(QFrame.StyledPanel)
        self.emailFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.emailFrame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.emailIcon = QFrame(self.emailFrame)
        self.emailIcon.setObjectName(u"emailIcon")
        sizePolicy.setHeightForWidth(self.emailIcon.sizePolicy().hasHeightForWidth())
        self.emailIcon.setSizePolicy(sizePolicy)
        self.emailIcon.setMaximumSize(QSize(60, 70))
        self.emailIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.emailIcon.setFrameShape(QFrame.StyledPanel)
        self.emailIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.emailIcon)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(20, 20, 0, 20)
        self.label_3 = QLabel(self.emailIcon)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap(u":/Icons/Icons/emailIcon.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout_7.addWidget(self.label_3)


        self.horizontalLayout_6.addWidget(self.emailIcon)

        self.email = QLineEdit(self.emailFrame)
        self.email.setObjectName(u"email")
        sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
        self.email.setSizePolicy(sizePolicy)
        self.email.setMinimumSize(QSize(300, 70))
        self.email.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.email)


        self.horizontalLayout_15.addWidget(self.emailFrame, 0, Qt.AlignLeft)

        self.PhoneNumFrame = QFrame(self.emailPhoneNumFrame)
        self.PhoneNumFrame.setObjectName(u"PhoneNumFrame")
        sizePolicy1.setHeightForWidth(self.PhoneNumFrame.sizePolicy().hasHeightForWidth())
        self.PhoneNumFrame.setSizePolicy(sizePolicy1)
        self.PhoneNumFrame.setFrameShape(QFrame.StyledPanel)
        self.PhoneNumFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.PhoneNumFrame)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.phoneNumIcon = QFrame(self.PhoneNumFrame)
        self.phoneNumIcon.setObjectName(u"phoneNumIcon")
        sizePolicy.setHeightForWidth(self.phoneNumIcon.sizePolicy().hasHeightForWidth())
        self.phoneNumIcon.setSizePolicy(sizePolicy)
        self.phoneNumIcon.setMinimumSize(QSize(40, 70))
        self.phoneNumIcon.setMaximumSize(QSize(60, 70))
        self.phoneNumIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.phoneNumIcon.setFrameShape(QFrame.StyledPanel)
        self.phoneNumIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.phoneNumIcon)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(20, 20, 5, 15)
        self.label_4 = QLabel(self.phoneNumIcon)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u":/Icons/Icons/phoneNumIcon.png"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout_9.addWidget(self.label_4)


        self.horizontalLayout_8.addWidget(self.phoneNumIcon)

        self.PhoneNum = QLineEdit(self.PhoneNumFrame)
        self.PhoneNum.setObjectName(u"PhoneNum")
        sizePolicy.setHeightForWidth(self.PhoneNum.sizePolicy().hasHeightForWidth())
        self.PhoneNum.setSizePolicy(sizePolicy)
        self.PhoneNum.setMinimumSize(QSize(300, 70))
        self.PhoneNum.setDragEnabled(False)

        self.horizontalLayout_8.addWidget(self.PhoneNum)


        self.horizontalLayout_15.addWidget(self.PhoneNumFrame, 0, Qt.AlignRight)


        self.verticalLayout_4.addWidget(self.emailPhoneNumFrame)

        self.newPassConfirmPass = QFrame(self.frame_5)
        self.newPassConfirmPass.setObjectName(u"newPassConfirmPass")
        sizePolicy.setHeightForWidth(self.newPassConfirmPass.sizePolicy().hasHeightForWidth())
        self.newPassConfirmPass.setSizePolicy(sizePolicy)
        self.newPassConfirmPass.setFrameShape(QFrame.StyledPanel)
        self.newPassConfirmPass.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.newPassConfirmPass)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.NewPassFrame = QFrame(self.newPassConfirmPass)
        self.NewPassFrame.setObjectName(u"NewPassFrame")
        sizePolicy1.setHeightForWidth(self.NewPassFrame.sizePolicy().hasHeightForWidth())
        self.NewPassFrame.setSizePolicy(sizePolicy1)
        self.NewPassFrame.setFrameShape(QFrame.StyledPanel)
        self.NewPassFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.NewPassFrame)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.newPassIcon = QFrame(self.NewPassFrame)
        self.newPassIcon.setObjectName(u"newPassIcon")
        sizePolicy.setHeightForWidth(self.newPassIcon.sizePolicy().hasHeightForWidth())
        self.newPassIcon.setSizePolicy(sizePolicy)
        self.newPassIcon.setMinimumSize(QSize(40, 70))
        self.newPassIcon.setMaximumSize(QSize(60, 70))
        self.newPassIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.newPassIcon.setFrameShape(QFrame.StyledPanel)
        self.newPassIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.newPassIcon)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(25, 15, 5, 15)
        self.label_10 = QLabel(self.newPassIcon)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setPixmap(QPixmap(u":/Icons/Icons/lockIcon.png"))
        self.label_10.setScaledContents(True)

        self.horizontalLayout_17.addWidget(self.label_10)


        self.horizontalLayout_18.addWidget(self.newPassIcon)

        self.newPassword = QLineEdit(self.NewPassFrame)
        self.newPassword.setObjectName(u"newPassword")
        sizePolicy.setHeightForWidth(self.newPassword.sizePolicy().hasHeightForWidth())
        self.newPassword.setSizePolicy(sizePolicy)
        self.newPassword.setMinimumSize(QSize(300, 70))
        self.newPassword.setStyleSheet(u"")

        self.horizontalLayout_18.addWidget(self.newPassword)


        self.horizontalLayout_16.addWidget(self.NewPassFrame, 0, Qt.AlignLeft)

        self.confirmPassFrame = QFrame(self.newPassConfirmPass)
        self.confirmPassFrame.setObjectName(u"confirmPassFrame")
        sizePolicy1.setHeightForWidth(self.confirmPassFrame.sizePolicy().hasHeightForWidth())
        self.confirmPassFrame.setSizePolicy(sizePolicy1)
        self.confirmPassFrame.setFrameShape(QFrame.StyledPanel)
        self.confirmPassFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.confirmPassFrame)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.confirmpassIcon = QFrame(self.confirmPassFrame)
        self.confirmpassIcon.setObjectName(u"confirmpassIcon")
        sizePolicy.setHeightForWidth(self.confirmpassIcon.sizePolicy().hasHeightForWidth())
        self.confirmpassIcon.setSizePolicy(sizePolicy)
        self.confirmpassIcon.setMinimumSize(QSize(40, 70))
        self.confirmpassIcon.setMaximumSize(QSize(60, 70))
        self.confirmpassIcon.setStyleSheet(u"background-color: rgb(235, 235, 235);\n"
"border-top-left-radius:25px;\n"
"border-bottom-left-radius:25px;")
        self.confirmpassIcon.setFrameShape(QFrame.StyledPanel)
        self.confirmpassIcon.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.confirmpassIcon)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(25, 15, 5, 15)
        self.label_8 = QLabel(self.confirmpassIcon)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setPixmap(QPixmap(u":/Icons/Icons/lockIcon.png"))
        self.label_8.setScaledContents(True)

        self.horizontalLayout_20.addWidget(self.label_8)


        self.horizontalLayout_19.addWidget(self.confirmpassIcon, 0, Qt.AlignRight)

        self.confirmPassword = QLineEdit(self.confirmPassFrame)
        self.confirmPassword.setObjectName(u"confirmPassword")
        sizePolicy.setHeightForWidth(self.confirmPassword.sizePolicy().hasHeightForWidth())
        self.confirmPassword.setSizePolicy(sizePolicy)
        self.confirmPassword.setMinimumSize(QSize(300, 70))
        self.confirmPassword.setDragEnabled(False)

        self.horizontalLayout_19.addWidget(self.confirmPassword)


        self.horizontalLayout_16.addWidget(self.confirmPassFrame, 0, Qt.AlignRight)


        self.verticalLayout_4.addWidget(self.newPassConfirmPass)


        self.verticalLayout_3.addWidget(self.frame_5, 0, Qt.AlignLeft)

        self.completeSetupBtn = QPushButton(self.frame_2)
        self.completeSetupBtn.setObjectName(u"completeSetupBtn")
        sizePolicy.setHeightForWidth(self.completeSetupBtn.sizePolicy().hasHeightForWidth())
        self.completeSetupBtn.setSizePolicy(sizePolicy)
        self.completeSetupBtn.setMinimumSize(QSize(732, 0))
        self.completeSetupBtn.setStyleSheet(u"QPushButton{\n"
"	padding:5px;\n"
"	background-color:#0C8AA7;\n"
"	border:none;\n"
"	border-radius:20px;\n"
"	font: 87 20pt \"Montserrat Black\";\n"
"	color:rgb(255, 255, 255);\n"
"}")

        self.verticalLayout_3.addWidget(self.completeSetupBtn)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.firstLoginFrame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.close.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"FIRST-TIME ACCOUNT SETUP", None))
        self.label.setText("")
        self.fullName.setPlaceholderText(QCoreApplication.translate("Form", u"Full name", None))
        self.label_2.setText("")
        self.username.setPlaceholderText(QCoreApplication.translate("Form", u"Username", None))
        self.label_3.setText("")
        self.email.setPlaceholderText(QCoreApplication.translate("Form", u"Email (for recovery)", None))
        self.label_4.setText("")
        self.PhoneNum.setPlaceholderText(QCoreApplication.translate("Form", u"Enter password", None))
        self.label_10.setText("")
        self.newPassword.setPlaceholderText(QCoreApplication.translate("Form", u"New password", None))
        self.label_8.setText("")
        self.confirmPassword.setPlaceholderText(QCoreApplication.translate("Form", u"Confirm password", None))
        self.completeSetupBtn.setText(QCoreApplication.translate("Form", u"COMPLETE SETUP", None))
        pass
    # retranslateUi


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
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(462, 522)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(440, 500))
        self.frame.setStyleSheet(u"background-color: #FCFCFC;\n"
"border-radius: 10px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color: transparent;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(140, 60))
        self.label.setPixmap(QPixmap(u"image/petmateLogo.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frame_2, 0, Qt.AlignRight)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 63 10pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_3.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.frame_6)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 45))
        self.lineEdit.setStyleSheet(u"QLineEdit{\n"
"	border-right: 2px solid #cccccc;\n"
"    border-bottom: 2px solid #cccccc;\n"
"    border-radius: 5px;\n"
"	\n"
"	font: 57 8pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"}")

        self.verticalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout_2.addWidget(self.frame_6)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 63 10pt \"Montserrat SemiBold\";\n"
"color:rgb(39, 39, 39);")

        self.verticalLayout_4.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.frame_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 45))
        self.lineEdit_2.setMaximumSize(QSize(16777215, 45))
        self.lineEdit_2.setStyleSheet(u"QLineEdit{\n"
"	border-right: 2px solid #cccccc;\n"
"    border-bottom: 2px solid #cccccc;\n"
"    border-radius: 5px;\n"
"	\n"
"	font: 8pt \"Montserrat SemiBold\";\n"
"	color:rgb(39, 39, 39);\n"
"	padding-left: 10px;\n"
"}")

        self.verticalLayout_4.addWidget(self.lineEdit_2)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox = QCheckBox(self.frame_3)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"#label_4{\n"
"color: #019AC8;\n"
"}\n"
"#label_4:hover{\n"
"color: #007598;\n"
"}")

        self.horizontalLayout_2.addWidget(self.label_4, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"background-color: #81BFDA;\n"
"border-radius: 10px;\n"
"padding-left: 80px;\n"
"padding-right: 80px;")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: bold 10pt \"Montserrat\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout_3.addWidget(self.label_5, 0, Qt.AlignHCenter)


        self.verticalLayout_2.addWidget(self.frame_5, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.frame, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Username", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Enter Username", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Password", None))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Form", u"Enter Password", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Remember me", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Forget password?", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"LOG IN", None))
    # retranslateUi


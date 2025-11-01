# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paginationUi.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(787, 65)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_59 = QFrame(Form)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setStyleSheet(u"QPushButton{\n"
"font: 11pt \"Rubik Mono One\";\n"
"color:rgb(56, 56, 56);\n"
"}\n"
"")
        self.frame_59.setFrameShape(QFrame.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_82 = QHBoxLayout(self.frame_59)
        self.horizontalLayout_82.setSpacing(10)
        self.horizontalLayout_82.setObjectName(u"horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(10, 5, 10, 5)
        self.PrevPage = QPushButton(self.frame_59)
        self.PrevPage.setObjectName(u"PrevPage")
        self.PrevPage.setStyleSheet(u"border:none; background-color:transparent;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/prevPage.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.PrevPage.setIcon(icon)
        self.PrevPage.setIconSize(QSize(35, 35))

        self.horizontalLayout_82.addWidget(self.PrevPage)

        self.pageButtonsContainer = QWidget(self.frame_59)
        self.pageButtonsContainer.setObjectName(u"pageButtonsContainer")
        self.pageButtonsLayout = QHBoxLayout(self.pageButtonsContainer)
        self.pageButtonsLayout.setSpacing(5)
        self.pageButtonsLayout.setObjectName(u"pageButtonsLayout")
        self.pageButtonsLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_82.addWidget(self.pageButtonsContainer, 0, Qt.AlignHCenter)

        self.NextPage = QPushButton(self.frame_59)
        self.NextPage.setObjectName(u"NextPage")
        self.NextPage.setStyleSheet(u"border:none; background-color:transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/NextPage.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.NextPage.setIcon(icon1)
        self.NextPage.setIconSize(QSize(35, 35))

        self.horizontalLayout_82.addWidget(self.NextPage)


        self.verticalLayout.addWidget(self.frame_59)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi


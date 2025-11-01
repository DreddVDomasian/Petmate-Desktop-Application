# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serviceCard.ui'
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
    QPushButton, QSizePolicy, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(935, 258)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 0, 5, 5)
        self.wholeFrameCard = QFrame(Form)
        self.wholeFrameCard.setObjectName(u"wholeFrameCard")
        self.wholeFrameCard.setStyleSheet(u"#wholeFrameCard{\n"
"	border-radius:10px;\n"
"}")
        self.wholeFrameCard.setFrameShape(QFrame.StyledPanel)
        self.wholeFrameCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.wholeFrameCard)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.upperFrame = QFrame(self.wholeFrameCard)
        self.upperFrame.setObjectName(u"upperFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upperFrame.sizePolicy().hasHeightForWidth())
        self.upperFrame.setSizePolicy(sizePolicy)
        self.upperFrame.setStyleSheet(u"#upperFrame{\n"
"	border-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"}")
        self.upperFrame.setFrameShape(QFrame.StyledPanel)
        self.upperFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.upperFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.serviceLabel = QLabel(self.upperFrame)
        self.serviceLabel.setObjectName(u"serviceLabel")
        sizePolicy.setHeightForWidth(self.serviceLabel.sizePolicy().hasHeightForWidth())
        self.serviceLabel.setSizePolicy(sizePolicy)
        self.serviceLabel.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout.addWidget(self.serviceLabel)

        self.doneOnLabel = QLabel(self.upperFrame)
        self.doneOnLabel.setObjectName(u"doneOnLabel")
        sizePolicy.setHeightForWidth(self.doneOnLabel.sizePolicy().hasHeightForWidth())
        self.doneOnLabel.setSizePolicy(sizePolicy)
        self.doneOnLabel.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout.addWidget(self.doneOnLabel)

        self.returnDateLabel = QLabel(self.upperFrame)
        self.returnDateLabel.setObjectName(u"returnDateLabel")
        sizePolicy.setHeightForWidth(self.returnDateLabel.sizePolicy().hasHeightForWidth())
        self.returnDateLabel.setSizePolicy(sizePolicy)
        self.returnDateLabel.setStyleSheet(u"font: 57 14pt \"Montserrat Medium\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout.addWidget(self.returnDateLabel)

        self.OpenNoteBtn = QToolButton(self.upperFrame)
        self.OpenNoteBtn.setObjectName(u"OpenNoteBtn")
        self.OpenNoteBtn.setLayoutDirection(Qt.RightToLeft)
        self.OpenNoteBtn.setStyleSheet(u"QToolButton{\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:rgb(252, 213, 151);\n"
"	border-radius:10px;\n"
"	border-bottom: 2px solid rgb(235, 198, 141);\n"
"	border-right: 1px solid rgb(235, 198, 141);\n"
"	padding:10px;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color:rgb(252, 205, 127);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/downArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.OpenNoteBtn.setIcon(icon)
        self.OpenNoteBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.OpenNoteBtn)

        self.closeNotesBtn = QToolButton(self.upperFrame)
        self.closeNotesBtn.setObjectName(u"closeNotesBtn")
        self.closeNotesBtn.setLayoutDirection(Qt.RightToLeft)
        self.closeNotesBtn.setStyleSheet(u"QToolButton{\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	background-color:rgb(252, 213, 151);\n"
"	border-radius:10px;\n"
"	border-bottom: 2px solid rgb(235, 198, 141);\n"
"	border-right: 1px solid rgb(235, 198, 141);\n"
"	padding:10px;\n"
"}\n"
"QToolButton:hover{\n"
"	background-color:rgb(252, 205, 127);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/upArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeNotesBtn.setIcon(icon1)
        self.closeNotesBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.closeNotesBtn)


        self.verticalLayout_2.addWidget(self.upperFrame)

        self.lowerFrame = QFrame(self.wholeFrameCard)
        self.lowerFrame.setObjectName(u"lowerFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lowerFrame.sizePolicy().hasHeightForWidth())
        self.lowerFrame.setSizePolicy(sizePolicy1)
        self.lowerFrame.setStyleSheet(u"#lowerFrame{\n"
"	border-bottom-left-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"	background-color:rgb(231, 231, 231);\n"
"}")
        self.lowerFrame.setFrameShape(QFrame.StyledPanel)
        self.lowerFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.lowerFrame)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, -1, 20, -1)
        self.noteFrame = QFrame(self.lowerFrame)
        self.noteFrame.setObjectName(u"noteFrame")
        sizePolicy1.setHeightForWidth(self.noteFrame.sizePolicy().hasHeightForWidth())
        self.noteFrame.setSizePolicy(sizePolicy1)
        self.noteFrame.setMinimumSize(QSize(0, 120))
        self.noteFrame.setFrameShape(QFrame.StyledPanel)
        self.noteFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.noteFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.noteTitle = QFrame(self.noteFrame)
        self.noteTitle.setObjectName(u"noteTitle")
        self.noteTitle.setFrameShape(QFrame.StyledPanel)
        self.noteTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.noteTitle)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.noteTitle)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setStyleSheet(u"font: 81 14pt \"Montserrat ExtraBold\";\n"
"color:rgb(39, 39, 39);")

        self.horizontalLayout_5.addWidget(self.label_4, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.noteTitle, 0, Qt.AlignTop)

        self.mainNoteFrame = QFrame(self.noteFrame)
        self.mainNoteFrame.setObjectName(u"mainNoteFrame")
        sizePolicy1.setHeightForWidth(self.mainNoteFrame.sizePolicy().hasHeightForWidth())
        self.mainNoteFrame.setSizePolicy(sizePolicy1)
        self.mainNoteFrame.setFrameShape(QFrame.StyledPanel)
        self.mainNoteFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.mainNoteFrame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 10, 0, 0)
        self.noteLabel = QTextEdit(self.mainNoteFrame)
        self.noteLabel.setObjectName(u"noteLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.noteLabel.sizePolicy().hasHeightForWidth())
        self.noteLabel.setSizePolicy(sizePolicy2)
        self.noteLabel.setStyleSheet(u"\n"
"QTextEdit{\n"
"	font: 57 12pt \"Montserrat Medium\";\n"
"	color:rgb(39, 39, 39);\n"
"	border:none;\n"
"	background:transparent\n"
"\n"
"}")
        self.noteLabel.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.noteLabel, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.mainNoteFrame)


        self.verticalLayout_3.addWidget(self.noteFrame, 0, Qt.AlignTop)

        self.btnNoteFrame = QFrame(self.lowerFrame)
        self.btnNoteFrame.setObjectName(u"btnNoteFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnNoteFrame.sizePolicy().hasHeightForWidth())
        self.btnNoteFrame.setSizePolicy(sizePolicy3)
        self.btnNoteFrame.setFrameShape(QFrame.StyledPanel)
        self.btnNoteFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.btnNoteFrame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.btnNoteFrame)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy3.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy3)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.updateServiceCardBtn = QPushButton(self.frame_6)
        self.updateServiceCardBtn.setObjectName(u"updateServiceCardBtn")
        sizePolicy3.setHeightForWidth(self.updateServiceCardBtn.sizePolicy().hasHeightForWidth())
        self.updateServiceCardBtn.setSizePolicy(sizePolicy3)
        self.updateServiceCardBtn.setStyleSheet(u"background:transparent;")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/Icons/editPeDetails.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.updateServiceCardBtn.setIcon(icon2)
        self.updateServiceCardBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout_8.addWidget(self.updateServiceCardBtn)

        self.serviceDeleteBtn = QPushButton(self.frame_6)
        self.serviceDeleteBtn.setObjectName(u"serviceDeleteBtn")
        sizePolicy3.setHeightForWidth(self.serviceDeleteBtn.sizePolicy().hasHeightForWidth())
        self.serviceDeleteBtn.setSizePolicy(sizePolicy3)
        self.serviceDeleteBtn.setStyleSheet(u"background:transparent;")
        icon3 = QIcon()
        icon3.addFile(u":/Icons/Icons/deleteBlack.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.serviceDeleteBtn.setIcon(icon3)
        self.serviceDeleteBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout_8.addWidget(self.serviceDeleteBtn, 0, Qt.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_6)


        self.verticalLayout_3.addWidget(self.btnNoteFrame, 0, Qt.AlignRight|Qt.AlignBottom)


        self.verticalLayout_2.addWidget(self.lowerFrame)


        self.horizontalLayout_3.addWidget(self.wholeFrameCard)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.serviceLabel.setText(QCoreApplication.translate("Form", u"Service Label", None))
        self.doneOnLabel.setText(QCoreApplication.translate("Form", u"Done on:", None))
        self.returnDateLabel.setText(QCoreApplication.translate("Form", u"Return Date", None))
        self.OpenNoteBtn.setText(QCoreApplication.translate("Form", u"Open Note", None))
        self.closeNotesBtn.setText(QCoreApplication.translate("Form", u"Close Note", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Note:", None))
        self.noteLabel.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Montserrat Medium'; font-size:12pt; font-weight:56; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400;\">To whoever comes across these words, my heartfelt wish is that whatever troubles you, whatever burdens your heart, may soon find solace. May clarity wash away the fog of uncertainty, and may serenity reign in your life.</span></p></body></html>", None))
        self.updateServiceCardBtn.setText("")
        self.serviceDeleteBtn.setText("")
    # retranslateUi


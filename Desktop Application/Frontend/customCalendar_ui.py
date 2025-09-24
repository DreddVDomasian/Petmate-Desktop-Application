# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'customCalendar.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QSizePolicy, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(390, 306)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet(u"background:transparent;\n"
"border:none;")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.calendarWidget = QCalendarWidget(Form)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setStyleSheet(u"QCalendarWidget {\n"
"    background-color: white;\n"
"    border: 1px solid gray;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
"    background-color: rgb(129, 191, 218);\n"
"    border: none;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    icon-size: 16px;\n"
"    background-color: transparent;\n"
"	padding:6px;\n"
"}\n"
"\n"
"QCalendarWidget QMenu {\n"
"    font: 57 10pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    background-color: white;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox {\n"
"    font: 57 12pt \"Montserrat Medium\";\n"
"    color: rgb(39, 39, 39);\n"
"    width: 70px;\n"
"}\n"
"QSpinBox::up-button {\n"
"	image: url(:/Icons/Icons/upArrow.png);\n"
"	width:13px;\n"
"}\n"
"QSpinBox::down-button {\n"
"	image: url(:/Icons/Icons/downArrow.png);\n"
"	width:13px;\n"
"}\n"
"QCalendarWidget QToolButton#qt_calendar_prevmonth {\n"
"    qproperty-icon: url(:/Icon"
                        "s/Icons/left-arrow.png);\n"
"}\n"
"\n"
"QCalendarWidget QToolButton#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(:/Icons/Icons/right-arrow.png);\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView:enabled {\n"
"    font: 57 14pt \"Montserrat Medium\";\n"
"    color: black;\n"
"    background-color: rgb(255, 255, 255); \n"
"}\n"
"\n"
"\n"
"QCalendarWidget QAbstractItemView::item:selected {\n"
"    background-color: rgb(252, 213, 151);\n"
"    color: black;              \n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView::item:hover {\n"
"    background-color: rgba(252, 213, 151,0.4);\n"
"}\n"
"")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setSelectionMode(QCalendarWidget.SingleSelection)
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)

        self.verticalLayout.addWidget(self.calendarWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi


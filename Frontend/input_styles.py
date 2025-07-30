from PyQt6.QtWidgets import QDateEdit

default_style = """
            QLineEdit {
                border-right: 2px solid #cccccc;
                border-bottom: 2px solid #cccccc;
                border-radius: 5px;

	            font: 57 12pt 'Montserrat Medium';
	            color:rgb(39, 39, 39);
	            padding-left: 10px;
            }"""

default_combobox_style = """
            QComboBox {
                border-right: 2px solid #cccccc;
                border-bottom: 2px solid #cccccc;
                border-radius: 5px;
                font: 63 12pt "Montserrat SemiBold";
                padding-left: 5px;
                color: rgb(39, 39, 39);
            }

            QComboBox::drop-down {
                background-color: white;
                border: none;
            }

            QComboBox::down-arrow {
                image: url(:/Icons/Icons/downArrow.png);
                width: 12px;
                height: 12px;
                padding-right: 10px;
            }

            /* Dropdown list */
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: rgb(193, 193, 193); 
                selection-color: black;
                font: 63 12pt "Montserrat SemiBold";
                outline: none;
                border:none;
            }

            /* List items */
            QComboBox QAbstractItemView::item {
                background-color: white;
                color: black;
                height: 25px;
                font: 63 12pt "Montserrat SemiBold";
            }

            QComboBox QAbstractItemView::item:hover {
                background-color: rgb(193, 193, 193);
                color: black;
            }

            /* Scrollbar inside dropdown */
            QComboBox QAbstractItemView QScrollBar:vertical {
                background-color: transparent; /* or set a solid color */
                width: 10px;
                border: none;
            }

            QComboBox QAbstractItemView QScrollBar::handle:vertical {
                background-color: rgb(129, 191, 218);
                border-radius: 5px;
                min-height: 120px;
            }

            QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
                background-color: rgb(86, 127, 145);
            }

            QComboBox QAbstractItemView QScrollBar::add-line:vertical,
            QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }

            QComboBox QAbstractItemView QScrollBar::groove:vertical {
                background: transparent;
                outline: none;
                border: none;
            }
            QComboBox QAbstractItemView QScrollBar,
            QComboBox QAbstractItemView QScrollBar::handle,
            QComboBox QAbstractItemView QScrollBar::groove {
                outline: none;
                border: none;
            }

        """

error_combobox_style = """
                    QComboBox {
                        border: 1px solid #ff4f61;
                        border-radius: 5px;
                        font: 63 12pt "Montserrat SemiBold";
                        padding-left: 5px;
                        color: rgb(39, 39, 39);
                    }

                    QComboBox::drop-down {
                        background-color: white;
                        border: none;
                    }

                    QComboBox::down-arrow {
                        image: url(:/Icons/Icons/downArrow.png);
                        width: 12px;
                        height: 12px;
                        padding-right: 10px;
                    }

                    /* Dropdown list */
                    QComboBox QAbstractItemView {
                        background-color: white;
                        selection-background-color: rgb(193, 193, 193); 
                        selection-color: black;
                        font: 63 12pt "Montserrat SemiBold";
                        outline: none;
                        border:none;
                    }

                    /* List items */
                    QComboBox QAbstractItemView::item {
                        background-color: white;
                        color: black;
                        height: 25px;
                        font: 63 12pt "Montserrat SemiBold";
                    }

                    QComboBox QAbstractItemView::item:hover {
                        background-color: rgb(193, 193, 193);
                        color: black;
                    }

                    /* Scrollbar inside dropdown */
                    QComboBox QAbstractItemView QScrollBar:vertical {
                        background-color: transparent; /* or set a solid color */
                        width: 10px;
                        border: none;
                    }

                    QComboBox QAbstractItemView QScrollBar::handle:vertical {
                        background-color: rgb(129, 191, 218);
                        border-radius: 5px;
                        min-height: 120px;
                    }

                    QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
                        background-color: rgb(86, 127, 145);
                    }

                    QComboBox QAbstractItemView QScrollBar::add-line:vertical,
                    QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                        height: 0px;
                        background: none;
                        border: none;
                    }

                    QComboBox QAbstractItemView QScrollBar::groove:vertical {
                        background: transparent;
                        outline: none;
                        border: none;
                    }
                    QComboBox QAbstractItemView QScrollBar,
                    QComboBox QAbstractItemView QScrollBar::handle,
                    QComboBox QAbstractItemView QScrollBar::groove {
                        outline: none;
                        border: none;
                    }

                """
error_style = """
            QLineEdit {
                border: 1px solid #ff4f61;
                border-radius: 5px;

                font: 57 12pt 'Montserrat Medium';
                color:rgb(39, 39, 39);
                padding-left: 10px;
            }"""


calendar_style = """
QCalendarWidget {
    background-color: white;
    border: 1px solid gray;
    border-radius: 8px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(129, 191, 218);
    border: none;
}

QCalendarWidget QToolButton {
    font: 57 12pt "Montserrat Medium";
    color: rgb(39, 39, 39);
    icon-size: 24px;
    background-color: transparent;
}

QCalendarWidget QMenu {
    background-color: white;
}

QCalendarWidget QSpinBox {
    width: 70px;
}
QCalendarWidget QAbstractItemView:enabled {
    font: 57 14pt "Montserrat Medium";
    color: black;
    background-color: white;
	selection-background-color: #86C5FF;
    selection-color: black;
}



QCalendarWidget QToolButton#qt_calendar_prevmonth {
    qproperty-icon: url(:/Icons/Icons/left-arrow.png);
}

QCalendarWidget QToolButton#qt_calendar_nextmonth {
    qproperty-icon: url(:/Icons/Icons/right-arrow.png);
}

"""

QframeStyle = """
QFrame {border:none;}
"""

completer_popup_style = """
QListView {
    background-color: white;
    selection-background-color: rgb(193, 193, 193);
    selection-color: black;
    font: 63 12pt "Montserrat SemiBold";
    border: 1px solid rgb(209, 209, 209);
    outline: none;
}

/* List items */
QListView::item {
    background-color: white;
    color: black;
    height: 25px;
    font: 63 12pt "Montserrat SemiBold";
}

QListView::item:hover {
    background-color: rgb(193, 193, 193);
    color: black;
}

/* Scrollbar inside completer */
QScrollBar:vertical {
    background-color: transparent;
    width: 10px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: rgb(129, 191, 218);
    border-radius: 5px;
    min-height: 120px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgb(86, 127, 145);
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
    border: none;
}

QScrollBar::groove:vertical {
    background: transparent;
    outline: none;
    border: none;
}

QScrollBar, QScrollBar::handle, QScrollBar::groove {
    outline: none;
    border: none;
}
"""

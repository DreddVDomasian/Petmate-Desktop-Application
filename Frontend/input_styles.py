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
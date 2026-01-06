"""Shared UI helper utilities for the Desktop_Application frontend.

Keep small, reusable UI helpers here to avoid copying logic across screens
and to reduce circular import risks.
"""

from __future__ import annotations

from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import QLineEdit


def setup_password_toggle(
    line_edit: QLineEdit,
    tool_button,
    icon_show: str = "Icons/eye.png",
    icon_hide: str = "Icons/hide.png",
) -> None:


    # Store toggle state inside the button so it's reusable
    tool_button.password_visible = False

    def toggle() -> None:
        if getattr(tool_button, "password_visible", False):
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            tool_button.setIcon(QIcon(icon_show))
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            tool_button.setIcon(QIcon(icon_hide))

        tool_button.password_visible = not getattr(tool_button, "password_visible", False)

    tool_button.clicked.connect(toggle)


def setup_phone_input(line_edit: QLineEdit) -> None:
    """Apply PH phone validation + normalization to a QLineEdit.

    Supports typing in these common formats:
    - 09XXXXXXXXX (11 digits)
    - 9XXXXXXXXX (10 digits)
    - 63XXXXXXXXXX (12 digits)
    - +63XXXXXXXXXX (13 chars)

    Normalizes to: +63XXXXXXXXXX and prevents appending extra digits.
    """

    validator = QRegularExpressionValidator(
        QRegularExpression(r'^(?:0\d{0,10}|9\d{0,9}|63\d{0,10}|\+63\d{0,10})$')
    )
    line_edit.setMaxLength(13)
    line_edit.setValidator(validator)

    def on_changed(text: str) -> None:
        if not text:
            return

        cursor_pos = line_edit.cursorPosition()

        if text.startswith('+63'):
            digits_after = ''.join(ch for ch in text[3:] if ch.isdigit())
            if len(digits_after) > 10:
                digits_after = digits_after[:10]
            normalized = '+63' + digits_after
            if normalized != text:
                line_edit.blockSignals(True)
                line_edit.setText(normalized)
                line_edit.blockSignals(False)
                line_edit.setCursorPosition(len(normalized))
            return

        if text.startswith('63'):
            rest = ''.join(ch for ch in text[2:] if ch.isdigit())
            if len(rest) > 10:
                rest = rest[:10]
            normalized = '+63' + rest
            if normalized != text:
                line_edit.blockSignals(True)
                line_edit.setText(normalized)
                line_edit.blockSignals(False)
                line_edit.setCursorPosition(len(normalized))
            return

        if text.startswith('09'):
            if len(text) == 11:
                normalized = '+63' + text[1:]
                if normalized != text:
                    line_edit.blockSignals(True)
                    line_edit.setText(normalized)
                    line_edit.blockSignals(False)
                    line_edit.setCursorPosition(len(normalized))
            elif len(text) > 11:
                line_edit.blockSignals(True)
                line_edit.setText(text[:11])
                line_edit.blockSignals(False)
                line_edit.setCursorPosition(cursor_pos)
            return

        if text.startswith('9'):
            digits_only = ''.join(ch for ch in text if ch.isdigit())
            if len(digits_only) == 10:
                normalized = '+63' + digits_only
                line_edit.blockSignals(True)
                line_edit.setText(normalized)
                line_edit.blockSignals(False)
                line_edit.setCursorPosition(len(normalized))
            elif len(digits_only) > 10:
                line_edit.blockSignals(True)
                line_edit.setText(digits_only[:10])
                line_edit.blockSignals(False)
                line_edit.setCursorPosition(min(cursor_pos, 10))
            return

        # Fallback: enforce max length for any other valid partial pattern.
        if len(text) > 13:
            line_edit.blockSignals(True)
            line_edit.setText(text[:13])
            line_edit.blockSignals(False)
            line_edit.setCursorPosition(min(cursor_pos, 13))

    line_edit.textChanged.connect(on_changed)

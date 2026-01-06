"""Shared UI helper utilities for the Desktop_Application frontend.

Keep small, reusable UI helpers here to avoid copying logic across screens
and to reduce circular import risks.
"""

from __future__ import annotations

from PyQt6.QtGui import QIcon
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

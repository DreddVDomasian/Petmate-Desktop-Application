"""DEPRECATED.

This HTTP client is used by the desktop UI (Frontend) to call the deployed backend.
It should live in Desktop_Application/Frontend.

Kept only for backward compatibility in case some old code still imports
Desktop_Application.Backend.api_client.
"""

from __future__ import annotations

try:
    # Preferred location
    from Desktop_Application.Frontend.api_client import *  # noqa: F403
except Exception as _e:  # pragma: no cover
    raise ImportError(
        "Desktop_Application.Backend.api_client is deprecated. "
        "Import from Desktop_Application.Frontend.api_client instead. "
        f"(Original import error: {_e})"
    )

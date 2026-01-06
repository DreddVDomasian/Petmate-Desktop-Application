"""HTTP client helpers for the Desktop_Application frontend.

This module is used by the PyQt desktop UI to talk to the deployed backend API.
It should live in the Frontend (not Backend) to avoid circular dependencies.
"""

from __future__ import annotations

from typing import Any

import requests

from Desktop_Application.Frontend.config_loader import API_BASE_URL


BASE_URL = API_BASE_URL


def _post_json(path: str, payload: dict[str, Any], timeout: int = 10):
    url = f"{BASE_URL}{path}"
    return requests.post(url, json=payload, timeout=timeout)


def _get(path: str, timeout: int = 10):
    url = f"{BASE_URL}{path}"
    return requests.get(url, timeout=timeout)


def send_otp(email: str):
    """Send OTP to user's email for password reset."""
    try:
        response = _post_json(
            "/api/send-reset-otp/",
            {
                "email": email,
                "source": "desktop",
            },
            timeout=15,
        )

        if response.status_code == 200:
            return True, response.json()
        return False, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def verify_otp_and_reset_password(email: str, otp: str, new_password: str | None):
    """Verify OTP and reset password."""
    try:
        response = _post_json(
            "/api/verify-reset-otp/",
            {
                "email": email,
                "otp": otp,
                "new_password": new_password,
            },
            timeout=15,
        )

        if response.status_code == 200:
            return True, response.json()
        return False, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def desktop_login(username: str, password: str):
    """Login for desktop users (admin/staff)."""
    try:
        response = _post_json(
            "/api/desktop-login/",
            {
                "username": username,
                "password": password,
            },
            timeout=10,
        )

        data = response.json()
        return (response.status_code == 200), data
    except Exception as e:
        return False, {"error": f"Connection error: {str(e)}"}


def first_time_setup(user_id: int, full_name: str, email: str, phone: str, username: str, new_password: str):
    """Complete first-time setup for desktop users."""
    try:
        response = _post_json(
            "/api/desktop-first-time-setup/",
            {
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "username": username,
                "new_password": new_password,
            },
            timeout=15,
        )

        data = response.json()
        return (response.status_code == 200), data
    except Exception as e:
        return False, {"error": f"Connection error: {str(e)}"}


def add_new_patient(data: dict[str, Any]) -> bool:
    try:
        response = _post_json("/api/patients/", data, timeout=20)
        return response.status_code == 201
    except Exception:
        return False


def add_new_pet(data: dict[str, Any]) -> bool:
    try:
        response = _post_json("/api/pets/", data, timeout=20)
        return response.status_code == 201
    except Exception:
        return False


def get_all_patients() -> list[dict[str, Any]]:
    try:
        response = _get("/api/patients/", timeout=15)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def add_new_service(data: dict[str, Any]) -> bool:
    try:
        response = _post_json("/api/services/", data, timeout=20)
        return response.status_code == 201
    except Exception:
        return False


def add_new_appointment(appointment_data: dict[str, Any]) -> bool:
    """Send walk-in appointment data to API."""
    try:
        response = _post_json("/api/walkIn/", appointment_data, timeout=20)
        return response.status_code == 201
    except Exception:
        return False

import os, sys
# Ensure Python can find your project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from ..Frontend.config_loader import API_BASE_URL


BASE_URL = API_BASE_URL  # later change to your real server url

def send_otp(email):
    """Send OTP to user's email for password reset"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/send-reset-otp/",
            json={
                'email': email,
                'source': 'desktop'
            }
        )

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()

    except Exception as e:
        return False, {'error': str(e)}


def verify_otp_and_reset_password(email, otp, new_password):
    """Verify OTP and reset password"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/verify-reset-otp/",
            json={
                'email': email,
                'otp': otp,
                'new_password': new_password
            }
        )

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()

    except Exception as e:
        return False, {'error': str(e)}
def desktop_login(username, password):
    """Login for desktop users (admin/staff)"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/desktop-login/",
            json={
                'username': username,
                'password': password
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            data = response.json()
            return False, data

    except Exception as e:
        return False, {'error': f'Connection error: {str(e)}'}


def first_time_setup(user_id, full_name, email, phone, username, new_password):
    """Complete first-time setup for desktop users"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/desktop-first-time-setup/",
            json={
                'user_id': user_id,
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'username': username,
                'new_password': new_password
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            data = response.json()
            return False, data

    except Exception as e:
        return False, {'error': f'Connection error: {str(e)}'}

def add_new_patient(data):
    """
    data: dict with all patient info
    """
    try:
        response = requests.post(f"{BASE_URL}/api/patients/", json=data)
        if response.status_code == 201:
            print("Successfully added!")
            return True
        else:
            print("Failed to add patient:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Error:", e)
        return False


def add_new_pet(data):
    """
    data: dict with all patient info
    """
    try:
        response = requests.post(f"{BASE_URL}/api/pets/", json=data)
        if response.status_code == 201:
            print("Successfully added!")
            return True
        else:
            print("Failed to add patient:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Error:", e)
        return False


def get_all_patients():
    try:
        response = requests.get(f"{BASE_URL}/api/patients/")
        if response.status_code == 200:
            return response.json()  # this will be a list of dicts
        else:
            print("Failed to fetch patients:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Error:", e)
        return []


def add_new_service(data):
    """
    data: dict with service info
    """
    try:
        response = requests.post(f"{BASE_URL}/api/services/", json=data)
        if response.status_code == 201:
            print("Successfully added service!")
            return True
        else:
            print("Failed to add service:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Error:", e)
        return False


def add_new_appointment(appointment_data):
    """Send appointment data to API"""
    try:
        print(f"DEBUG: Sending to API: {appointment_data}")

        response = requests.post(
            f"{API_BASE_URL}/api/walkIn/",
            json=appointment_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"DEBUG: API Response Status: {response.status_code}")
        print(f"DEBUG: API Response Text: {response.text}")

        if response.status_code == 201:
            return True
        else:
            # Log the error
            try:
                error_data = response.json()
                print(f"DEBUG: API Error: {error_data}")
            except:
                print(f"DEBUG: API Error (raw): {response.text}")
            return False
    except Exception as e:
        print(f"DEBUG: Exception in add_new_appointment: {e}")
        return False
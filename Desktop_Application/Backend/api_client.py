import requests


BASE_URL = "http://127.0.0.1:8000/api"   # later change to your real server url

def add_new_patient(data):
    """
    data: dict with all patient info
    """
    try:
        response = requests.post(f"{BASE_URL}/patients/", json=data)
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
        response = requests.post(f"{BASE_URL}/pets/", json=data)
        if response.status_code == 201:
            print("Successfully added!")
            return True
        else:
            print("Failed to add patient:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Error:", e)
        return False


def get_all_patients(page=1, page_size=10):
    try:
        response = requests.get(f"{BASE_URL}/patients/?page={page}&page_size={page_size}")
        if response.status_code == 200:
            data = response.json()
            return {
                "patients": data.get("results", []),
                "count": data.get("count", 0),
                "next": data.get("next"),
                "previous": data.get("previous")
            }
        else:
            print("Failed to fetch patients:", response.status_code, response.text)
            return {"patients": [], "count": 0, "next": None, "previous": None}
    except Exception as e:
        print("Error:", e)
        return {"patients": [], "count": 0, "next": None, "previous": None}


def add_new_service(data):
    """
    data: dict with service info
    """
    try:
        response = requests.post(f"{BASE_URL}/services/", json=data)
        if response.status_code == 201:
            print("Successfully added service!")
            return True
        else:
            print("Failed to add service:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Error:", e)
        return False

def add_new_appointment(data):
    response = requests.post("http://127.0.0.1:8000/api/walkIn/", json=data)
    return response.status_code == 201

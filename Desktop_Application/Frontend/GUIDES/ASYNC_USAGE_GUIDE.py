"""
ASYNC HELPER - USAGE EXAMPLES
========================================

This helper makes all API calls non-blocking (smooth UI)

SETUP (Do once in __init__):
-----------------------------
from async_helper import AsyncHelper
from config_loader import API_BASE_URL

class MainWindow:
    def __init__(self):
        # Create async helper
        self.api = AsyncHelper(self, base_url=API_BASE_URL)


BASIC USAGE:
-----------

# ❌ OLD WAY (blocks UI):
def load_patients(self):
    response = requests.get(f"{API_BASE_URL}/api/patients/")
    data = response.json()
    self.create_patient_cards(data['results'])

# ✅ NEW WAY (smooth):
def load_patients(self):
    self.api.get('/api/patients/', 
                 on_success=self.on_patients_loaded,
                 on_error=self.on_load_error)

def on_patients_loaded(self, data):
    patients = data.get('results', [])
    self.create_patient_cards(patients)

def on_load_error(self, error_msg):
    print(f"Error: {error_msg}")
    self.show_empty_state(error=True)


WITH LOADING INDICATOR:
----------------------
def load_patients(self):
    # Show skeleton loader while loading
    self.api.get('/api/patients/',
                 on_success=self.on_patients_loaded,
                 show_loading=True,
                 loading_widget=self.patientScrollArea)


WITH SEARCH PARAMS:
------------------
def search_patients(self, term):
    self.api.get('/api/patient-search/',
                 on_success=self.on_search_results,
                 params={'search': term, 'page': 1})


POST REQUEST:
------------
def save_patient(self, patient_data):
    self.api.post('/api/patients/',
                  data=patient_data,
                  on_success=self.on_save_success,
                  on_error=self.on_save_error)

def on_save_success(self, response):
    self.show_toast("Patient saved!", "success")
    self.load_patients()  # Reload list


PUT/PATCH REQUEST:
-----------------
def update_service(self, service_id, updates):
    self.api.patch(f'/api/services/{service_id}/',
                   data=updates,
                   on_success=lambda r: self.show_toast("Updated!"))


DELETE REQUEST:
--------------
def delete_patient(self, patient_id):
    self.api.delete(f'/api/patients/{patient_id}/',
                    on_success=lambda r: self.reload_patients())


WITH CUSTOM TIMEOUT:
-------------------
def send_reminders(self):
    # Long operation needs more time
    self.api.post('/api/desktop-manual-reminder/',
                  data={'appointment_ids': [1, 2, 3]},
                  on_success=self.on_reminders_sent,
                  timeout=120)  # 2 minutes


INLINE CALLBACKS (Lambda):
--------------------------
def quick_check(self):
    self.api.get('/api/office-hours/',
                 on_success=lambda data: print(data),
                 on_error=lambda e: print(f"Error: {e}"))


CONVERSION EXAMPLES:
===================

1. LOAD PATIENTS:
   OLD: def load_patients(self, page=1):
            url = f"{API_BASE_URL}/api/patients/?page={page}"
            response = requests.get(url)
            data = response.json()
            self.create_patient_cards(data['results'])
   
   NEW: def load_patients(self, page=1):
            self.api.get(f'/api/patients/?page={page}',
                        on_success=lambda d: self.create_patient_cards(d['results']))


2. LOAD PETS FOR OWNER:
   OLD: def load_pets(self, owner_id):
            response = requests.get(f"{API_BASE_URL}/api/pets/?owner_id={owner_id}")
            pets = response.json()
            self.populate_pet_combo(pets)
   
   NEW: def load_pets(self, owner_id):
            self.api.get(f'/api/pets/?owner_id={owner_id}',
                        on_success=self.populate_pet_combo)


3. DELETE ITEM:
   OLD: def delete_service(self, service_id):
            response = requests.delete(f"{API_BASE_URL}/api/services/{service_id}/")
            if response.status_code == 204:
                self.reload_services()
   
   NEW: def delete_service(self, service_id):
            self.api.delete(f'/api/services/{service_id}/',
                          on_success=lambda r: self.reload_services())


4. SAVE WITH VALIDATION:
   OLD: def save_appointment(self, data):
            try:
                response = requests.post(f"{API_BASE_URL}/api/walkIn/", json=data)
                if response.status_code == 201:
                    self.show_toast("Saved!")
                else:
                    self.show_toast("Failed!")
            except Exception as e:
                self.show_toast(f"Error: {e}")
   
   NEW: def save_appointment(self, data):
            self.api.post('/api/walkIn/',
                         data=data,
                         on_success=lambda r: self.show_toast("Saved!"),
                         on_error=lambda e: self.show_toast(f"Error: {e}"))


TIPS:
=====
1. Always use trailing slashes in URLs: '/api/patients/' not '/api/patients'
2. Use lambda for simple callbacks, named functions for complex ones
3. Set timeout=120 for operations like sending emails/SMS
4. Use show_loading=True for better UX
5. Handle errors with on_error callback

"""

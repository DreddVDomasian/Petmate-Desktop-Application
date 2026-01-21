"""
EXAMPLE: How to Add Loading Modals to app.py
==============================================

This file shows BEFORE and AFTER examples for common operations.
Copy these patterns to your own code.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Load Patients (Most Important)
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE: No loading indicator - UI might freeze if list is large
def load_patients_BEFORE(self, page=1, search_term=None):
    """Load patients without loading modal"""
    response = requests.get(
        f"{API_BASE_URL}/api/patients/?page={page}&search={search_term}"
    )
    patients = response.json()
    # ... display patients


# AFTER: With loading modal - User knows something is happening
def load_patients_AFTER(self, page=1, search_term=None):
    """Load patients WITH loading modal"""
    self.api.get(
        url=f"/api/patients/?page={page}&search={search_term}",
        on_success=self._on_patients_loaded,
        on_error=self._on_patients_error,
        # ← ADD THESE 3 LINES:
        show_loading=True,
        loading_title="Loading patients...",
        loading_subtitle="Please wait while we fetch the patient list"
    )

def _on_patients_loaded(self, response):
    """Handle successful patient load"""
    patients = response.get('results', [])
    # ... update UI with patients
    print(f"✅ Loaded {len(patients)} patients")

def _on_patients_error(self, error_msg):
    """Handle error loading patients"""
    print(f"❌ Error: {error_msg}")
    Toast(self, "Failed to load patients", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Submit Patient Data (Create)
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE: No feedback during submission
def submit_data_BEFORE(self):
    """Submit patient data without loading"""
    data = self.collect_form_data()
    response = requests.post(f"{API_BASE_URL}/api/patients/", json=data)
    patient = response.json()
    # ... show success


# AFTER: With loading modal - User won't think app froze
def submit_data_AFTER(self):
    """Submit patient data WITH loading modal"""
    data = self.collect_form_data()
    # Validate form first...
    if not data:
        return
    
    self.api.post(
        url="/api/patients/",
        data=data,
        on_success=self._on_patient_added,
        on_error=self._on_patient_error,
        # ← ADD THESE 3 LINES:
        show_loading=True,
        loading_title="Adding patient...",
        loading_subtitle="Please wait while we save the patient information"
    )

def _on_patient_added(self, response):
    """Handle successful patient creation"""
    self.navigate_to_page(2)  # Go to patient list
    self.load_patients(1, search_term=None)  # Reload list
    Toast(self, icon_path="Icons/check.png").show_toast()

def _on_patient_error(self, error_msg):
    """Handle error creating patient"""
    Toast(self, "Failed to add patient!", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Load Scheduled Services
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE: No loading indicator
def load_scheduled_services_BEFORE(self, page=1, search_term=None):
    response = requests.get(f"{API_BASE_URL}/api/services/?status=scheduled&page={page}")
    # ... process response


# AFTER: With loading modal
def load_scheduled_services_AFTER(self, page=1, search_term=None):
    self.api.get(
        url=f"/api/services/?status=scheduled&page={page}&search={search_term}",
        on_success=self._on_services_loaded,
        on_error=self._on_error,
        show_loading=True,
        loading_title="Loading scheduled services...",
        loading_subtitle="Please wait"
    )

def _on_services_loaded(self, response):
    services = response.get('results', [])
    # ... display services


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Delete Operation
# ═══════════════════════════════════════════════════════════════════════════════

# In delete.py - Replace synchronous delete with async:

# BEFORE: Synchronous (UI freezes)
def delete_patient_BEFORE(self, patient_id):
    response = requests.delete(f"{API_BASE_URL}/api/patients/{patient_id}/")
    if response.status_code == 204:
        # Success
        pass


# AFTER: Async with loading (UI responsive)
def delete_patient_AFTER(self, patient_id):
    self.main_window.api.delete(
        url=f"/api/patients/{patient_id}/",
        on_success=lambda r: self._on_delete_success(patient_id),
        on_error=self._on_delete_error,
        show_loading=True,
        loading_title="Deleting patient...",
        loading_subtitle="This action cannot be undone"
    )

def _on_delete_success(self, patient_id):
    print(f"✅ Deleted patient {patient_id}")
    self.main_window.load_patients(1)  # Reload list
    Toast(self.main_window, "Patient deleted", icon_path="Icons/check.png").show_toast()

def _on_delete_error(self, error_msg):
    print(f"❌ Delete error: {error_msg}")
    Toast(self.main_window, "Failed to delete patient", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Update Operation
# ═══════════════════════════════════════════════════════════════════════════════

# In updateFunction.py - Update patient info:

# BEFORE: Synchronous update
def update_patient_BEFORE(self, patient_id, data):
    response = requests.put(
        f"{API_BASE_URL}/api/patients/{patient_id}/",
        json=data
    )
    return response.json()


# AFTER: Async with loading
def update_patient_AFTER(self, patient_id, data):
    self.main_window.api.put(
        url=f"/api/patients/{patient_id}/",
        data=data,
        on_success=self._on_update_success,
        on_error=self._on_update_error,
        show_loading=True,
        loading_title="Saving changes...",
        loading_subtitle="Please don't close the app"
    )

def _on_update_success(self, response):
    print("✅ Patient updated successfully")
    self.main_window.load_patients(1)  # Reload
    Toast(self.main_window, "Changes saved", icon_path="Icons/check.png").show_toast()

def _on_update_error(self, error_msg):
    print(f"❌ Update error: {error_msg}")
    Toast(self.main_window, "Failed to save changes", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Search Operation (with debouncing + loading)
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE: Search without loading
def on_search_BEFORE(self, search_term):
    if not search_term:
        self.load_patients(1)
        return
    
    response = requests.get(f"{API_BASE_URL}/api/patients/?search={search_term}")
    # ... display results


# AFTER: Search with debouncing and loading
def on_search_AFTER(self, search_term):
    if not search_term:
        self.load_patients(1)
        return
    
    self.api.get(
        url=f"/api/patients/?search={search_term}",
        on_success=self._on_search_results,
        on_error=self._on_search_error,
        show_loading=True,
        loading_title="Searching...",
        loading_subtitle="Please wait while we search records"
    )

def _on_search_results(self, response):
    results = response.get('results', [])
    print(f"✅ Found {len(results)} results")
    # ... display results

def _on_search_error(self, error_msg):
    print(f"❌ Search error: {error_msg}")
    Toast(self, "Search failed", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Send Email/SMS Reminders
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE: No feedback while sending
def send_reminder_BEFORE(self, reminder_id):
    response = requests.post(f"{API_BASE_URL}/api/send-reminder/", json={'id': reminder_id})
    # ... handle response


# AFTER: Show loading while sending
def send_reminder_AFTER(self, reminder_id):
    self.api.post(
        url="/api/send-reminder/",
        data={'reminder_id': reminder_id},
        on_success=lambda r: self._on_reminder_sent(reminder_id),
        on_error=self._on_reminder_error,
        show_loading=True,
        loading_title="Sending reminder...",
        loading_subtitle="Please don't close the app"
    )

def _on_reminder_sent(self, reminder_id):
    print(f"✅ Reminder {reminder_id} sent successfully")
    Toast(self, "Reminder sent!", icon_path="Icons/check.png").show_toast()

def _on_reminder_error(self, error_msg):
    print(f"❌ Send error: {error_msg}")
    Toast(self, "Failed to send reminder", icon_path="Icons/warning.png").show_toast()


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE: API Methods with Loading
# ═══════════════════════════════════════════════════════════════════════════════

QUICK_REFERENCE = """
GET (Read):
    self.api.get(
        url="/api/resource/",
        on_success=callback,
        on_error=error_callback,
        show_loading=True,
        loading_title="Loading...",
        loading_subtitle="Please wait"
    )

POST (Create):
    self.api.post(
        url="/api/resource/",
        data=payload,
        on_success=callback,
        on_error=error_callback,
        show_loading=True,
        loading_title="Creating...",
        loading_subtitle="Please wait"
    )

PUT (Replace):
    self.api.put(
        url="/api/resource/{id}/",
        data=payload,
        on_success=callback,
        on_error=error_callback,
        show_loading=True,
        loading_title="Updating...",
        loading_subtitle="Please wait"
    )

PATCH (Partial update):
    self.api.patch(
        url="/api/resource/{id}/",
        data=payload,
        on_success=callback,
        on_error=error_callback,
        show_loading=True,
        loading_title="Saving...",
        loading_subtitle="Please wait"
    )

DELETE (Remove):
    self.api.delete(
        url="/api/resource/{id}/",
        on_success=callback,
        on_error=error_callback,
        show_loading=True,
        loading_title="Deleting...",
        loading_subtitle="Please wait"
    )
"""

print("✅ Examples loaded!")
print("📖 Reference these examples when adding loading to your app")
print("⚡ Copy the AFTER patterns to your code")

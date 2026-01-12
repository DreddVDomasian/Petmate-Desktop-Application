"""
LOADING MODAL INTEGRATION GUIDE
================================

This guide shows how to add loading modals to prevent UI freezing during API calls.

Three approaches, from simplest to most advanced:
1. Quick Implementation - Add loading to existing async calls
2. Smart Manager - Auto-show/hide with minimal delay
3. Batch Operations - Track progress for multiple items
"""

# ═══════════════════════════════════════════════════════════════════════════════
# APPROACH 1: SIMPLE - Add loading_title to async calls (RECOMMENDED)
# ═══════════════════════════════════════════════════════════════════════════════

# BEFORE (no loading indicator):
"""
def load_patients(self, page=1, search_term=None):
    self.api.get(
        url=f"/api/patients/?page={page}&search={search_term}",
        on_success=self._on_patients_loaded,
        on_error=self._on_error
    )
"""

# AFTER (with loading modal):
"""
def load_patients(self, page=1, search_term=None):
    self.api.get(
        url=f"/api/patients/?page={page}&search={search_term}",
        on_success=self._on_patients_loaded,
        on_error=self._on_error,
        show_loading=True,
        loading_title="Loading patients...",
        loading_subtitle="Please wait while we fetch the patient list"
    )
"""

# Available parameters for all methods (get, post, put, delete):
LOADING_PARAMETERS = {
    'show_loading': True,              # Enable loading modal
    'loading_title': "Loading...",     # Main message
    'loading_subtitle': None,          # Secondary message (optional)
}

# Examples for different operations:
EXAMPLES = """
# Load data
self.api.get(
    url="/api/patients/",
    on_success=callback,
    show_loading=True,
    loading_title="Loading patients...",
    loading_subtitle="This may take a moment"
)

# Create new record
self.api.post(
    url="/api/patients/",
    data=patient_data,
    on_success=callback,
    show_loading=True,
    loading_title="Adding patient...",
    loading_subtitle="Please wait"
)

# Update record
self.api.put(
    url=f"/api/patients/{patient_id}/",
    data=updated_data,
    on_success=callback,
    show_loading=True,
    loading_title="Saving changes...",
    loading_subtitle="Please don't close the app"
)

# Delete record
self.api.delete(
    url=f"/api/patients/{patient_id}/",
    on_success=callback,
    show_loading=True,
    loading_title="Deleting patient...",
    loading_subtitle="This action cannot be undone"
)

# Send email/SMS
self.api.post(
    url="/api/send-reminder/",
    data=reminder_data,
    on_success=callback,
    show_loading=True,
    loading_title="Sending reminders...",
    loading_subtitle="Don't close the app"
)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# APPROACH 2: SMART MANAGER - Auto-show after delay
# ═══════════════════════════════════════════════════════════════════════════════

"""
Use SmartLoadingManager for better UX - only shows if request takes >500ms

Benefits:
- Fast requests don't show loading (no flashing)
- Slow requests show loading after 500ms
- Automatic hide with minimum 500ms display
- Less code than manual show/hide
"""

# In MainUI.__init__:
from smart_loading import SmartLoadingManager

self.loading_manager = SmartLoadingManager(self)

# Usage in any function:
def submit_patient_data(self):
    self.loading_manager.start(
        title="Adding patient...",
        subtitle="Please wait while we save your information"
    )
    
    self.api.post(
        url="/api/patients/",
        data=patient_data,
        on_success=self._on_patient_added,
        on_error=self._on_patient_error
    )

def _on_patient_added(self, response):
    self.loading_manager.stop()  # Auto-hides with minimum display time
    # Handle success


# ═══════════════════════════════════════════════════════════════════════════════
# APPROACH 3: BATCH OPERATIONS - Show progress for multiple items
# ═══════════════════════════════════════════════════════════════════════════════

"""
Use BatchOperationLoader for operations that process multiple items
Shows: Current progress / Total items

Example: Sending reminders to 50 patients
"""

from smart_loading import BatchOperationLoader

def send_reminders_to_all(self):
    patients = self.get_selected_patients()  # Get list of patients
    total = len(patients)
    
    loader = BatchOperationLoader(self, total_items=total)
    loader.start("Sending reminders...")
    
    for i, patient in enumerate(patients):
        self.send_reminder(patient)
        loader.update(increment=1)
        QApplication.processEvents()  # Keep UI responsive
    
    loader.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# RECOMMENDED LOADING MESSAGES BY OPERATION
# ═══════════════════════════════════════════════════════════════════════════════

MESSAGES = {
    # READ operations
    'load_patients': {
        'title': "Loading patients...",
        'subtitle': "Please wait while we fetch the patient list"
    },
    'load_pets': {
        'title': "Loading pet records...",
        'subtitle': "Retrieving pet information"
    },
    'load_services': {
        'title': "Loading services...",
        'subtitle': "Please wait while we fetch service records"
    },
    'load_appointments': {
        'title': "Loading appointments...",
        'subtitle': "Please wait"
    },
    
    # CREATE operations
    'add_patient': {
        'title': "Adding patient...",
        'subtitle': "Please wait while we save the patient information"
    },
    'add_pet': {
        'title': "Adding pet...",
        'subtitle': "Please wait while we register the pet"
    },
    'add_service': {
        'title': "Adding service...",
        'subtitle': "Please wait while we create the service record"
    },
    
    # UPDATE operations
    'update_patient': {
        'title': "Saving changes...",
        'subtitle': "Please don't close the app"
    },
    'update_pet': {
        'title': "Updating pet information...",
        'subtitle': "Please wait"
    },
    'update_service': {
        'title': "Saving service changes...",
        'subtitle': "Please wait"
    },
    
    # DELETE operations
    'delete_patient': {
        'title': "Deleting patient...",
        'subtitle': "This action cannot be undone"
    },
    'delete_pet': {
        'title': "Deleting pet record...",
        'subtitle': "This action cannot be undone"
    },
    'delete_service': {
        'title': "Deleting service...",
        'subtitle': "This action cannot be undone"
    },
    
    # SPECIAL operations
    'send_reminder': {
        'title': "Sending reminders...",
        'subtitle': "Don't close the app"
    },
    'send_sms': {
        'title': "Sending SMS...",
        'subtitle': "Please wait"
    },
    'print_document': {
        'title': "Generating document...",
        'subtitle': "Please wait while we prepare the file"
    },
    'export_data': {
        'title': "Exporting data...",
        'subtitle': "Please wait while we prepare your file"
    },
    'search': {
        'title': "Searching...",
        'subtitle': "Please wait while we search records"
    },
    'sync_data': {
        'title': "Synchronizing...",
        'subtitle': "Updating data from server"
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════════

"""
Quick checklist for adding loading to your app:

Priority 1 (CRITICAL - Most used):
☐ load_patients() - Most called function
☐ load_scheduled_services()
☐ load_staff_accounts()
☐ submit_data() - Patient creation
☐ submit_pet_data() - Pet creation
☐ submit_service_data() - Service creation

Priority 2 (HIGH - Frequent operations):
☐ updateFunction.py - All update operations
☐ delete.py - All delete operations
☐ ReminderPopUp.py - Reminder operations
☐ send_reminder() - SMS/Email sending
☐ search() - Search operations

Priority 3 (MEDIUM - Occasional operations):
☐ appointmentPopUp.py - Appointment operations
☐ addServicePopUp.py - Service addition
☐ Print operations
☐ Export operations
☐ Sync operations

Priority 4 (LOW - Admin/rare operations):
☐ User management operations
☐ Settings updates
☐ Office hours updates
"""


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK IMPLEMENTATION TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

"""
Copy and modify this template for any API call:

def operation_name(self, arg1, arg2):
    # Add loading modal to async call
    self.api.METHOD(  # METHOD = get, post, put, delete, patch
        url="/api/endpoint/",
        data=data_dict,  # Only for post/put/patch
        on_success=self._on_operation_success,
        on_error=self._on_operation_error,
        # Add these 3 lines for loading:
        show_loading=True,
        loading_title="Operation description...",
        loading_subtitle="Please wait"
    )

def _on_operation_success(self, response):
    # Handle successful response
    print(f"Success: {response}")
    Toast(self, icon_path="Icons/check.png").show_toast()

def _on_operation_error(self, error_msg):
    # Handle error
    print(f"Error: {error_msg}")
    Toast(self, f"Failed: {error_msg}", icon_path="Icons/warning.png").show_toast()
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING LOADING MODALS
# ═══════════════════════════════════════════════════════════════════════════════

"""
To test that loading modals work:

1. Fast request (should NOT show loading):
   - Load from cache (takes <500ms)
   - Loading modal should NOT appear
   
2. Slow request (should show loading):
   - Throttle network (DevTools → Network → Slow 3G)
   - Perform operation
   - Loading modal should appear after 500ms
   - Modal should stay for minimum 500ms

3. Error handling:
   - Disconnect internet
   - Perform operation
   - Modal should appear
   - Error should be shown after modal hides
   - Error message should be displayed

4. Multiple concurrent requests:
   - Make 2-3 simultaneous requests
   - Only one loading modal should show
   - Both operations should complete
"""

print("✅ Loading Modal Integration Guide Ready!")
print("📖 Follow the examples above to add loading to your app")
print("⚡ Start with Priority 1 operations first")

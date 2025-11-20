from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views



urlpatterns = [
    path('patients/', BasicInfoListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', BasicInfoRetrieveUpdateDestroyView.as_view(), name='patients-detail'),
    path('patient-search/', PatientSearchView.as_view(), name='patient-search'),
    path("check-duplicate/", check_duplicate_patient),

    path('pets/', PetListCreateView.as_view(), name='pets-list-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pets-detail'),
    #path('pets/', views.create_pet, name='api_create_pet'), # REACT ADD PETS

    path('services/', ServiceListCreateView.as_view(), name='services-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='services-detail'),
    path('scheduled-services/', ScheduledServiceListView.as_view(), name='scheduled-services'),

    path('patient-combobox-data/', views.patient_combobox_data, name='patient-combobox-data'),
    path('check-time-slot/', views.check_time_slot_availability_api, name='check-time-slot'),

    path('walkIn/', WalkInListCreateView.as_view(), name='walk-in'),
    path('walkIn/<int:pk>/', WalkInRetrieveUpdateDestroyView.as_view(), name='walkIn-detail'),

    path("print/<int:owner_id>/<int:pet_id>/", views.print_record, name="print_record"),
    path("reminders/", views.reminders, name="reminders"),
    
    

    # Main booking endpoint for your HTML form
    #path('bookings/', BookingCreateView.as_view(), name='create_booking'),


    # Auth endpoints for frontend (final paths: /api/csrf/, /api/register/, /api/login/, /api/logout/)
    path('csrf/', views.csrf_token, name='api_csrf'),
    path('register/', views.register_view, name='api_register'),
    path('login/', views.login_view, name='api_login'),
    path('logout/', views.logout_view, name='api_logout'),
    path('user/', views.current_user, name='api_current_user'),

    # Desktop Authentication
    path('desktop-login/', views.DesktopLoginView.as_view(), name='desktop_login'),
    path('desktop-first-time-setup/', views.FirstTimeSetupView.as_view(), name='desktop_first_time_setup'),
    path('desktop-change-password/', views.ChangePasswordView.as_view(), name='desktop_change_password'),
    path('desktop-create-staff/', views.CreateStaffView.as_view(), name='desktop_create_staff'),
    path('desktop-users/', views.DesktopUserListView.as_view(), name='desktop_users_list'),
    path('desktop-users/<int:pk>/', views.DesktopUserRetrieveUpdateDestroyView.as_view(), name='desktop-users-detail'),
    path('desktop-reset-password/', views.ResetStaffPasswordView.as_view(), name='desktop_reset_password'),

    # EMAIL REMINDERS
    path('desktop-reminder-status/', ReminderStatusView.as_view(), name='desktop_reminder_status'),
    path('desktop-manual-reminder/', ManualReminderView.as_view(), name='desktop_manual_reminder'),

    #   Password Reset Endpoints
    path('send-reset-otp/', views.send_reset_otp, name='send_reset_otp'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),

    #   WEB PASSWORD RESET VIEW
    path('web-reset-password/', views.web_reset_password, name='web_reset_password'),


    #Settings endpoints
    path('user/profile/', views.user_profile, name='user-profile'),

    # CONTACT US MESSAGE ENDPOINT (WEBSITE)
    path('contact-us_message/', views.contact_us_message, name='contact_us_message'),
]

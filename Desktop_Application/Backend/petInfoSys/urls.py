from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('patients/', BasicInfoListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', BasicInfoRetrieveUpdateDestroyView.as_view(), name='patients-detail'),
    path('patient-search/', PatientSearchView.as_view(), name='patient-search'),
    path("check-duplicate/", check_duplicate_patient),

    path('pets/', PetListCreateView.as_view(), name='pets-list-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pets-detail'),

    path('services/', ServiceListCreateView.as_view(), name='services-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='services-detail'),
    path('scheduled-services/', ScheduledServiceListView.as_view(), name='scheduled-services'),

    path('patient-combobox-data/', views.patient_combobox_data, name='patient-combobox-data'),
    path('walkIn/', WalkInListCreateView.as_view(), name='walk-in'),
    path('walkIn/<int:pk>/', WalkInRetrieveUpdateDestroyView.as_view(), name='walkIn-detail'),

    path("print/<int:owner_id>/<int:pet_id>/", views.print_record, name="print_record"),
    path("reminders/", views.reminders, name="reminders"),
    # WEB APP URlS
    # Main booking endpoint for your HTML form
    path('bookings/', BookingCreateView.as_view(), name='create_booking'),
    path('clients/', ClientListView.as_view(), name='get_clients'),
    path('pets-web/', PetWebListView.as_view(), name='get_pets'),
    path('appointments/', AppointmentListView.as_view(), name='get_appointments'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:pk>/statusUpdate/', update_appointment_status, name='update_appointment_status'),

    # Auth endpoints for frontend (final paths: /api/csrf/, /api/register/, /api/login/, /api/logout/)
    path('csrf/', views.csrf_token, name='api_csrf'),
    path('register/', views.register_view, name='api_register'),
    path('login/', views.login_view, name='api_login'),
    path('logout/', views.logout_view, name='api_logout'),
    path('user/', views.current_user, name='api_current_user'),

]

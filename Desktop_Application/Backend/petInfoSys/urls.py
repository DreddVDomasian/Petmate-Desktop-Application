from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('patients/', BasicInfoListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', BasicInfoRetrieveUpdateDestroyView.as_view(), name='patients-detail'),

    path("check-duplicate/", check_duplicate_patient),

    path('pets/', PetListCreateView.as_view(), name='pets-list-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pets-detail'),

    path('services/', ServiceListCreateView.as_view(), name='services-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='services-detail'),
    path('scheduled-services/', ScheduledServiceListView.as_view(), name='scheduled-services'),

    path('walkIn/', WalkInListCreateView.as_view(), name='walk-in'),
    path('walkIn/<int:pk>/', WalkInRetrieveUpdateDestroyView.as_view(), name='walkIn-detail'),

    path("print/<int:owner_id>/<int:pet_id>/", views.print_record, name="print_record"),
    path("reminders/", views.reminders, name="reminders"),
    # WEB APP URlS
    # Main booking endpoint for your HTML form
    path('bookings/', views.create_booking, name='create_booking'),


    path('clients/', views.get_clients, name='get_clients'),
    path('pets-web/', views.get_pets, name='get_pets'),

    path('appointments/', views.get_appointments, name='get_appointments'),
    path('appointments/<int:pk>/', views.get_appointment_detail, name='appointment-detail'),
    path('appointments/<int:pk>/statusUpdate/', views.update_appointment_status, name='update_appointment_status'),

]

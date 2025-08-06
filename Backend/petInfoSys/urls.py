from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('patients/', BasicInfoListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', BasicInfoRetrieveUpdateDestroyView.as_view(), name='patients-detail'),

    path('pets/', PetListCreateView.as_view(), name='pets-list-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pets-detail'),

    path('services/', ServiceListCreateView.as_view(), name='services-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='services-detail'),
    path('scheduled-services/', ScheduledServiceListView.as_view(), name='scheduled-services'),

    path('walkIn/', WalkInListCreateView.as_view(), name='walk-in'),
    path('walkIn/', WalkInRetrieveUpdateDestroyView.as_view(), name='walkIn-detail'),

    path("print/<int:owner_id>/<int:pet_id>/", views.print_record, name="print_record"),

]

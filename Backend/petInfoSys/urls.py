from django.urls import path
from .views import BasicInfoListCreateView, BasicInfoRetrieveUpdateDestroyView, PetListCreateView, PetRetrieveUpdateDestroyView

urlpatterns = [
    path('patients/', BasicInfoListCreateView.as_view(), name='patients-list-create'),
    path('patients/<int:pk>/', BasicInfoRetrieveUpdateDestroyView.as_view(), name='patients-detail'),

    path('pets/', PetListCreateView.as_view(), name='pets-list-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pets-detail'),
]

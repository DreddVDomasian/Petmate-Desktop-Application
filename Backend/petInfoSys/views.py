from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from .models import *
from django.shortcuts import render, get_object_or_404
from .serializers import *



def print_record(request, owner_id, pet_id):
    owner = get_object_or_404(basicInfo, id=owner_id)
    pet = get_object_or_404(Pet, id=pet_id, owner=owner)
    services = Service.objects.filter(pet=pet).order_by("date")

    return render(request, "print_template.html", {
        "owner": owner,
        "pet": pet,
        "services": services
    })


@api_view(['GET'])
def reminders(request):
    reminders = []

    # Pending/overdue appointments
    appointments = WalkInAppointment.objects.filter(status__in=["pending", "overdue"])

    for appt in appointments:
        reminders.append({
            "id": appt.id,
            "type": "appointment",
            "date": appt.date.strftime("%Y-%m-%d"),
            "time": appt.prefTime.strftime("%I:%M %p") if appt.prefTime else None,
            "service": appt.service_name,
            "pet_id": appt.pet.id,
            "status": appt.status
        })

    # Pending service returns
    services = Service.objects.filter(return_date__isnull=False)
    for svc in services:
        # dynamically calculate status
        if svc.return_date < date.today():
            status = "overdue"
        else:
            status = "pending"

        reminders.append({
            "id": svc.id,
            "type": "Service Return",
            "date": svc.return_date.strftime("%Y-%m-%d"),
            "time": None,
            "service": svc.service_type,
            "pet_id": svc.pet.id,
            "status": status
        })

    # Sort by date
    reminders = sorted(reminders, key=lambda x: x["date"])
    return Response(reminders)

# GET all & POST new patient
class BasicInfoListCreateView(generics.ListCreateAPIView):
    queryset = basicInfo.objects.all()
    serializer_class = BasicInfoSerializer

# GET / PUT / DELETE single patient by id
class BasicInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = basicInfo.objects.all()
    serializer_class = BasicInfoSerializer

class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            return Pet.objects.filter(owner_id=owner_id)
        return Pet.objects.all()


class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        pet_id = self.request.query_params.get('pet_id')
        owner_id = self.request.query_params.get('owner_id')
        queryset = Service.objects.all()
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        return queryset

class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ScheduledServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        pet_id = self.request.query_params.get('pet_id')
        owner_id = self.request.query_params.get('owner_id')
        queryset = Service.objects.filter(return_date__isnull=False)
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        return queryset


class WalkInListCreateView(generics.ListCreateAPIView):
    queryset = WalkInAppointment.objects.all()
    serializer_class = WalkInSerializer

# GET / PUT / DELETE single patient by id
class WalkInRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WalkInAppointment.objects.all()
    serializer_class = WalkInSerializer


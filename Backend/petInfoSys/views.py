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

    pet_id = request.query_params.get("pet_id", None)

    # Appointments (only show pending/overdue)
    appointments = WalkInAppointment.objects.filter(status__in=["pending", "overdue"])
    if pet_id:
        appointments = appointments.filter(pet_id=pet_id)

    for appt in appointments:
        reminders.append({
            "id": appt.id,
            "type": "Appointment",
            "date": appt.date.strftime("%Y-%m-%d"),
            "time": appt.prefTime.strftime("%I:%M %p") if appt.prefTime else None,
            "service": appt.service_name,
            "pet_id": appt.pet.id,
            "pet_name": appt.pet.petName,
            "status": appt.status
        })

    # Services
    services = Service.objects.filter(return_date__isnull=False)

    if pet_id:
        services = services.filter(pet_id=pet_id)

    for svc in services:
        # if already completed, skip it
        if svc.status == "completed":
            continue

            # otherwise, dynamically calculate
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
            "pet_name": svc.pet.petName,
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
    queryset = Service.objects.all()

    def get_queryset(self):
        today = date.today()
        services = Service.objects.all()

        for svc in services:
            if svc.status not in ["completed", "cancelled"]:
                if svc.return_date and svc.return_date < today and svc.status != "overdue":
                    svc.status = "overdue"
                    svc.save(update_fields=["status"])
        return services


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
    serializer_class = WalkInSerializer

    def get_queryset(self):
        today = date.today()
        appointments = WalkInAppointment.objects.all()

        for appt in appointments:
            if appt.status not in ["completed", "cancelled"]:
                if appt.date < today and appt.status != "overdue":
                    appt.status = "overdue"
                    appt.save(update_fields=["status"])

        return appointments


class WalkInRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalkInSerializer
    queryset = WalkInAppointment.objects.all()

    def get_object(self):
        obj = super().get_object()
        today = date.today()
        if obj.status not in ["completed", "cancelled"]:
            if obj.date < today and obj.status != "overdue":
                obj.status = "overdue"
                obj.save(update_fields=["status"])
        return obj

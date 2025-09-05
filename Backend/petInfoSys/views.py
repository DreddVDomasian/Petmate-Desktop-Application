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

        # 🔎 Filter by pet_id if provided in query params
        pet_id = self.request.query_params.get("pet_id")
        if pet_id:
            services = services.filter(pet_id=pet_id)

        # 🔄 Auto-update status to overdue if needed
        for svc in services:
            if svc.status not in ["completed", "cancelled"]:
                if svc.return_date and svc.return_date < today and svc.status != "overdue":
                    svc.status = "overdue"
                    svc.save(update_fields=["status"])

        return services.order_by("date")



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


#------------------------------WEB APPOINTMENT VIEWS----------------------------------------------------

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
import json
from .models import Client, Pet, AppointmentType


@csrf_exempt
@require_http_methods(["POST"])
def create_booking(request):
    try:
        # Parse JSON data from request
        data = json.loads(request.body)

        # Use database transaction to ensure data integrity
        with transaction.atomic():
            # 1. Create or get client
            client_data = {
                'client_type': data.get('client_type'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'emergency_contact': data.get('emergency_contact'),
                'province': data.get('province'),
                'city': data.get('city'),
                'barangay': data.get('barangay'),
                'detailed_address': data.get('detailed_address'),
            }

            # Check if client already exists by email
            client, created = Client.objects.get_or_create(
                email=client_data['email'],
                defaults=client_data
            )

            # If client exists, update their information
            if not created:
                for key, value in client_data.items():
                    if key != 'email':  # Don't update email
                        setattr(client, key, value)
                client.save()

            # 2. Create pet
            pet = PetWeb.objects.create(
                client=client,
                pet_name=data.get('pet_name'),
                species=data.get('species'),
                breed=data.get('breed'),
                color=data.get('color'),
                sex=data.get('sex'),
            )

            # 3. Create appointment
            appointment = AppointmentType.objects.create(
                client=client,
                pet=pet,
                appointment_reason=data.get('appointment_reason'),
                provider=data.get('provider'),
                appointment_datetime=data.get('appointment_datetime'),
                comments=data.get('comments', ''),
                status='pending'
            )

        return JsonResponse({
            'status': 'success',
            'message': 'Booking created successfully',
            'data': {
                'client_id': client.id,
                'pet_id': pet.id,
                'appointment_id': appointment.id,
                'client_name': client.full_name,
                'pet_name': pet.pet_name,
                'appointment_datetime': appointment.appointment_datetime,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
def get_clients(request):
    """Get all clients"""
    try:
        clients = Client.objects.all().order_by('-created_at')
        clients_data = []

        for client in clients:
            clients_data.append({
                'id': client.id,
                'client_type': client.client_type,
                'full_name': client.full_name,
                'email': client.email,
                'phone': client.phone,
                'emergency_contact': client.emergency_contact,
                'full_address': client.full_address,
                'total_pets': client.pets.count(),
                'total_appointments': client.appointments.count(),
                'created_at': client.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'status': 'success',
            'clients': clients_data,
            'total': len(clients_data)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
def get_pets(request):
    """Get all pets"""
    try:
        pets = PetWeb.objects.select_related('client').all().order_by('-created_at')
        pets_data = []

        for pet in pets:
            pets_data.append({
                'id': pet.id,
                'pet_name': pet.pet_name,
                'species': pet.species,
                'breed': pet.breed,
                'color': pet.color,
                'sex': pet.sex,
                'client_name': pet.client.full_name,
                'client_id': pet.client.id,
                'total_appointments': pet.appointments.count(),
                'created_at': pet.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'status': 'success',
            'pets': pets_data,
            'total': len(pets_data)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
def get_appointments(request):
    """Get all appointments"""
    try:
        appointments = AppointmentType.objects.select_related('client', 'pet').all().order_by('-created_at')
        appointments_data = []

        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'client_name': appointment.client.full_name,
                'pet_name': appointment.pet.pet_name,
                'appointment_reason': appointment.appointment_reason,
                'provider': appointment.provider,
                'appointment_datetime': appointment.appointment_datetime,
                'status': appointment.status,
                'comments': appointment.comments,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'status': 'success',
            'appointments': appointments_data,
            'total': len(appointments_data)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

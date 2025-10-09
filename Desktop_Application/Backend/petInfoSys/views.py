from rest_framework import generics, status
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import date
from .models import *
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .serializers import *


class StandardPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

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

@api_view(["POST"])
def check_duplicate_patient(request):
    try:
        first = (request.data.get("firstName") or "").strip()
        last = (request.data.get("lastName") or "").strip()
        middle = (request.data.get("middleName") or "").strip()

        query = Q(firstName__iexact=first, lastName__iexact=last)

        if middle:
            query &= (
                Q(middleName__iexact=middle) |
                Q(middleName__isnull=True) |
                Q(middleName__exact="")
            )

        duplicates = basicInfo.objects.filter(query)

        patients = []
        for patient in duplicates:
            # ✅ handle related_name properly
            try:
                pets_qs = patient.pets.all()   # if you used related_name="pets"
            except AttributeError:
                pets_qs = patient.pet_set.all()  # fallback to default

            pets = PetSerializer(pets_qs, many=True).data
            patients.append({
                "patient": BasicInfoSerializer(patient).data,
                "pets": pets
            })

        return Response({"duplicates": patients}, status=200)

    except Exception as e:
        print("Error checking duplicates:", e)  # will show full error in console
        return Response({"error": str(e)}, status=500)


# GET all & POST new patient
class BasicInfoListCreateView(generics.ListCreateAPIView):
    queryset = basicInfo.objects.all().order_by('-id')
    serializer_class = BasicInfoSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Check if client wants to disable pagination (for combobox)
        disable_pagination = self.request.query_params.get('no_pagination')
        if disable_pagination:
            self.pagination_class = None

        return queryset


class PatientSearchView(generics.ListAPIView):
    serializer_class = BasicInfoSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '').strip()

        queryset = basicInfo.objects.all().order_by('firstName')

        if search_term:
            # Remove extra spaces and split
            search_terms = ' '.join(search_term.split()).split()

            if search_terms:
                query = Q()
                for term in search_terms:
                    # Search each term in all name fields
                    term_query = (
                            Q(firstName__icontains=term) |
                            Q(lastName__icontains=term) |
                            Q(middleName__icontains=term)
                    )
                    query &= term_query

                queryset = queryset.filter(query)

        return queryset

# GET / PUT / DELETE single patient by id
class BasicInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = basicInfo.objects.all()
    serializer_class = BasicInfoSerializer


@api_view(['GET'])
def patient_combobox_data(request):
    patients = basicInfo.objects.all().order_by('-id')

    patient_data = []
    for patient in patients:
        parts = [patient.firstName, patient.middleName, patient.lastName]
        full_name = " ".join(p for p in parts if p)
        patient_data.append({
            'id': patient.id,
            'full_name': full_name,
            'firstName': patient.firstName,
            'lastName': patient.lastName
        })

    return Response(patient_data)

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
    pagination_class = StandardPagination

    def get_queryset(self):
        today = date.today()

        # Start with a base queryset, ordered by date
        queryset = WalkInAppointment.objects.all().order_by('-date', '-prefTime')

        # Filter by status if the 'status' query parameter is provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Auto-update status to overdue if needed
        for appt in queryset:
            if appt.status not in ["completed", "cancelled", "overdue"]:
                if appt.date < today:
                    appt.status = "overdue"
                    appt.save(update_fields=["status"])

        return queryset

    def list(self, request, *args, **kwargs):
        # Get the filtered queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Check if client wants to disable pagination
        disable_pagination = request.query_params.get('no_pagination')
        if disable_pagination:
            self.pagination_class = None

        # Paginate the queryset if pagination is enabled
        if self.pagination_class is None:
            page = queryset
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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



# ------------------------------WEB APPOINTMENT VIEWS----------------------------------------------------



# REPLACE create_booking with DRF version
class BookingCreateView(generics.CreateAPIView):
    queryset = AppointmentType.objects.all()
    serializer_class = AppointmentTypeSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data

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

            return Response({
                'status': 'success',
                'message': 'Booking created successfully',
                'booking_id': appointment.booking_id,
                'data': {
                    'client_id': client.id,
                    'pet_id': pet.id,
                    'appointment_id': appointment.id,
                    'client_name': client.full_name,
                    'pet_name': pet.pet_name,
                    'appointment_datetime': appointment.appointment_datetime,
                    'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# CONVERT get_clients to DRF
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer

    def list(self, request, *args, **kwargs):
        clients = self.get_queryset()


        # Add your custom response format
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

        return Response({
            'status': 'success',
            'clients': clients_data,
            'total': len(clients_data)
        })


# CONVERT get_pets to DRF
class PetWebListView(generics.ListAPIView):
    queryset = PetWeb.objects.select_related('client').all().order_by('-created_at')
    serializer_class = PetWebSerializer

    def list(self, request, *args, **kwargs):
        pets = self.get_queryset()

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

        return Response({
            'status': 'success',
            'pets': pets_data,
            'total': len(pets_data)
        })


# CONVERT get_appointments to DRF
class AppointmentListView(generics.ListAPIView):
    queryset = AppointmentType.objects.select_related('client', 'pet').all().order_by('-created_at')
    serializer_class = AppointmentTypeSerializer

    def list(self, request, *args, **kwargs):
        appointments = self.get_queryset()

        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'booking_id': appointment.booking_id,
                'client_name': appointment.client.full_name,
                'email': appointment.client.email,
                'phone': appointment.client.phone,
                'province': appointment.client.province,
                'city': appointment.client.city,
                'barangay': appointment.client.barangay,
                'detailed_address': appointment.client.detailed_address,
                'pet_name': appointment.pet.pet_name,
                'species': appointment.pet.species,
                'breed': appointment.pet.breed,
                'color': appointment.pet.color,
                'sex': appointment.pet.sex,
                'provider': appointment.provider,
                'appointment_reason': appointment.appointment_reason,
                'appointment_datetime': appointment.appointment_datetime,
                'status': appointment.status,
                'comments': appointment.comments,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return Response({
            'status': 'success',
            'appointments': appointments_data,
            'total': len(appointments_data)
        })


# CONVERT get_appointment_detail to DRF
class AppointmentDetailView(generics.RetrieveAPIView):
    queryset = AppointmentType.objects.select_related('client', 'pet').all()
    serializer_class = AppointmentTypeSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            appointment = self.get_object()
            data = {
                'id': appointment.id,
                'client_name': appointment.client.full_name,
                'pet_name': appointment.pet.pet_name,
                'appointment_reason': appointment.appointment_reason,
                'provider': appointment.provider,
                'appointment_datetime': appointment.appointment_datetime,
                'status': appointment.status,
                'comments': appointment.comments,
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return Response({'status': 'success', 'appointment': data})
        except AppointmentType.DoesNotExist:
            return Response({
                'status': 'error',
                'message': f'Appointment with id {kwargs["pk"]} not found.'
            }, status=status.HTTP_404_NOT_FOUND)


# CONVERT update_appointment_status to DRF
@api_view(['PATCH'])
def update_appointment_status(request, pk):
    """Update only the status of an appointment"""
    try:
        appointment = AppointmentType.objects.get(pk=pk)
        new_status = request.data.get("status")

        if not new_status:
            return Response({
                "status": "error",
                "message": "Missing 'status' field"
            }, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        appointment.save()

        return Response({
            "status": "success",
            "message": f"Appointment {pk} status updated to {new_status}"
        })

    except AppointmentType.DoesNotExist:
        return Response({
            "status": "error",
            "message": f"Appointment with id {pk} not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, status, permissions, viewsets
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import date
from .models import *
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .serializers import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import re
import os



from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.middleware.csrf import get_token
from rest_framework import status as drf_status


class StandardPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        # ✅ Handle empty queryset without crashing
        count = queryset.count()
        if count == 0:
            self.page = None
            return []

        # ✅ If page number exceeds total pages, return last valid page
        try:
            return super().paginate_queryset(queryset, request, view)
        except Exception:
            # Fallback to first page on error
            self.page = None
            return list(queryset[:self.page_size])

    def get_paginated_response(self, data):
        if not self.page:
            return Response({
                'count': 0,
                'total_pages': 1,  # ✅ Always return at least 1 page
                'current_page': 1,
                'next': None,
                'previous': None,
                'results': []
            })
        return Response({
            'count': self.page.paginator.count,
            'total_pages': max(1, self.page.paginator.num_pages),  # ✅ Minimum 1 page
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


def print_record(request, owner_id, pet_id):
    owner = get_object_or_404(basicInfo, id=owner_id)
    pet = get_object_or_404(Pet, id=pet_id, owner=owner)
    services = Service.objects.filter(pet=pet).order_by("date")

    # Render the HTML template into a string
    html_string = render_to_string("print_template.html", {
        "owner": owner,
        "pet": pet,
        "services": services
    })

    # Generate PDF
    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()  # allows {% static %} to resolve correctly
    ).write_pdf(
        stylesheets=[CSS(os.path.join(settings.STATIC_ROOT, 'style.css'))]
    )

    # Sanitize owner name for filename
    owner_name_safe = re.sub(r'[^a-zA-Z0-9_-]', '_', owner.firstName + "_" + owner.lastName).upper()

    # Return as HTTP response to open in browser
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={owner_name_safe}_RECORD.pdf"
    return response


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

        duplicates = basicInfo.objects.filter(query).filter(desktop_record='show')

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


# -------------------- Auth endpoints (JSON + session) --------------------
@api_view(["GET"])
def csrf_token(request):
    """Return a CSRF token for the frontend to use in subsequent POSTs."""
    token = get_token(request)
    return Response({"csrfToken": token})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Web client registration - creates both User account and basicInfo profile
    """
    data = request.data if hasattr(request, 'data') else request.POST

    # Extract user account data
    first_name = data.get('first_name') or data.get('firstName') or ''
    last_name = data.get('last_name') or data.get('lastName') or ''
    email = data.get('email', '').strip().lower()
    password = data.get('password')

    # Extract basicInfo profile data
    middle_name = data.get('middleName') or ''
    phone_number = data.get('phoneNum') or ''
    secondary_number = data.get('phoneNum2') or ''  # Secondary phone as emergency number
    province = data.get('province') or ''
    city = data.get('city') or ''
    barangay = data.get('barangay') or ''
    detailed_address = data.get('detailedAdd') or ''

    # Validation
    if not email or not password:
        return Response({'error': 'Missing email or password'}, status=status.HTTP_400_BAD_REQUEST)

    if not first_name or not last_name:
        return Response({'error': 'First name and last name are required'}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
        return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if basicInfo already exists with this email
    if basicInfo.objects.filter(email=email).exists():
        return Response({'error': 'Patient profile with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # 1. Create User account
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # 2. Create basicInfo profile linked to User
            patient_profile = basicInfo.objects.create(
                # Personal Info
                firstName=first_name,
                lastName=last_name,
                middleName=middle_name if middle_name else None,
                email=email,
                phoneNumber=phone_number,
                SecondaryNumber=secondary_number if secondary_number else None,

                # Address Info
                province=province,
                city=city,
                barangay=barangay,
                detailedAddress=detailed_address,

                # System Fields
                source='web',
                desktop_record='hide',  # Hidden until appointments are accepted
                user_account=user  # Link to User account
            )

            # 3. Log the user in
            try:
                auth_request = request._request if hasattr(request, '_request') else request
                django_login(auth_request, user)
            except Exception as e:
                print(f"Login failed but user created: {e}")

            return Response({
                'ok': True,
                'message': 'Registration successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'patient_profile': {
                    'id': patient_profile.id,
                    'full_name': f"{patient_profile.firstName} {patient_profile.lastName}",
                    'desktop_record': patient_profile.desktop_record
                }
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def login_view(request):
    """
    POST JSON { email, password } -> authenticate and set session cookie
    """
    try:
        data = request.data if hasattr(request, 'data') else request.POST
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'error': 'Missing email or password'}, status=status.HTTP_400_BAD_REQUEST)

        # authenticate; use underlying WSGI request for Django auth
        auth_request = request._request if hasattr(request, '_request') else request
        user = authenticate(auth_request, username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        django_login(auth_request, user)
        return Response({'ok': True, 'username': user.username})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def logout_view(request):
    try:
        auth_request = request._request if hasattr(request, '_request') else request
        django_logout(auth_request)
        return Response({"ok": True})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def current_user(request):
    """Return basic info about the currently authenticated user and their patient profile."""
    if request.user.is_authenticated:
        # Get the patient profile if it exists
        patient_profile = None
        if hasattr(request.user, 'patient_profiles'):
            # User might have multiple profiles, get the first one
            patient_profile = request.user.patient_profiles.first()

        response_data = {
            "is_authenticated": True,
            "username": request.user.get_username(),
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        if patient_profile:
            response_data["patient_profile"] = {
                "id": patient_profile.id,
                "firstName": patient_profile.firstName,
                "lastName": patient_profile.lastName,
                "desktop_record": patient_profile.desktop_record,
                "source": patient_profile.source
            }

        return Response(response_data)
    else:
        return Response({"is_authenticated": False})



# GET all & POST new patient
class BasicInfoListCreateView(generics.ListCreateAPIView):
    queryset = basicInfo.objects.filter(desktop_record='show').order_by('-id')
    serializer_class = BasicInfoSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = basicInfo.objects.filter(desktop_record='show').order_by('-id')

        # Check if client wants to disable pagination (for combobox)
        disable_pagination = self.request.query_params.get('no_pagination')
        if disable_pagination:
            self.pagination_class = None

        return queryset

    def create(self, request, *args, **kwargs):
        # Create a mutable copy of the data instead of modifying request.data directly
        data = request.data.copy()

        # Force desktop settings when creating from desktop
        data['source'] = 'desktop'
        data['desktop_record'] = 'show'
        data['user_account'] = None  # No user account for desktop patients

        # Pass the modified data to the serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PatientSearchView(generics.ListAPIView):
    serializer_class = BasicInfoSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '').strip()

        queryset = basicInfo.objects.filter(desktop_record='show').order_by('firstName')

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

        # For desktop: filter by owner_id
        if owner_id:
            return Pet.objects.filter(owner_id=owner_id)

        # For web: get pets for logged-in user's basicInfo profile
        if self.request.user.is_authenticated:
            user_profile = basicInfo.objects.filter(user_account=self.request.user).first()
            if user_profile:
                return Pet.objects.filter(owner=user_profile)

        return Pet.objects.none()

    def perform_create(self, serializer):

        # For web: auto-link to user's basicInfo profile
        if self.request.user.is_authenticated:
            user_profile = basicInfo.objects.filter(user_account=self.request.user).first()
            if user_profile:
                serializer.save(owner=user_profile)
                return
            else:
                print("No basicInfo profile found for web user")

        # For desktop: use owner_id from request data
        print("Using desktop logic - expecting owner_id in request data")
        serializer.save()

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

        # 🔄 Auto-update status based on return_date logic
        for svc in services:
            if svc.return_date:  # Only check status for services with return dates
                if svc.status not in ["completed", "cancelled"]:
                    if svc.return_date < today and svc.status != "overdue":
                        svc.status = "overdue"
                        svc.save(update_fields=["status"])
            else:  # No return date = one-time service, auto-complete
                if svc.status != "completed":
                    svc.status = "completed"
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
        # Base queryset ordered (most recent first)
        queryset = WalkInAppointment.objects.all().order_by('-date', '-prefTime')

        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Search functionality - similar to patient search
        search_term = self.request.query_params.get('search', '').strip()
        if search_term:
            # Remove extra spaces and split
            search_terms = ' '.join(search_term.split()).split()

            if search_terms:
                query = Q()
                for term in search_terms:
                    # Search in owner name, pet name, and service name
                    term_query = (
                            Q(owner__firstName__icontains=term) |
                            Q(owner__lastName__icontains=term) |
                            Q(owner__middleName__icontains=term) |
                            Q(pet__petName__icontains=term) |
                            Q(service_name__icontains=term)
                    )
                    query &= term_query

                queryset = queryset.filter(query)

        # Auto-update status to overdue where necessary
        for appt in queryset:
            if appt.status not in ["completed", "cancelled", "overdue"]:
                if appt.date < today:
                    appt.status = "overdue"
                    appt.save(update_fields=["status"])

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Allow client to disable pagination
        disable_pagination = request.query_params.get('no_pagination')
        if disable_pagination:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

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



# REACT NA ITO
class ReactPetViewSet(viewsets.ModelViewSet): #URLS.PY
    serializer_class = ReactPetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReactPet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
from rest_framework import generics, status, permissions, viewsets
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import date,datetime,time,timedelta
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import pytz
import re
import os
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model, update_session_auth_hash
from django.middleware.csrf import get_token
from rest_framework import status as drf_status
import threading
import random
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.contrib.auth.models import User

from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import WalkInAppointment, Pet
from django.db.models import Count
from datetime import datetime


# Desktop Authentication Views
class DesktopLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = DesktopUser.objects.get(username=username, is_active=True)
            if user.check_password(password):
                # Update last login
                user.last_login = timezone.now()
                user.save()

                return Response({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'full_name': user.full_name,
                        'email': user.email,
                        'phone': user.phone,
                        'role': user.role,
                        'force_password_change': user.force_password_change,
                        'created_at': user.created_at.isoformat(),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Invalid password'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except DesktopUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
class ChangePasswordView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        try:
            user = DesktopUser.objects.get(id=user_id)

            if not user.check_password(current_password):
                return Response({
                    'success': False,
                    'error': 'Current password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({
                'success': True,
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)

        except DesktopUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)


# Admin-only views
class CreateStaffView(APIView):
    def post(self, request):
        admin_id = request.data.get('admin_id')
        full_name = request.data.get('full_name')

        try:
            admin = DesktopUser.objects.get(id=admin_id, role='admin')

            # Find the highest staff number that currently EXISTS in the database
            existing_staff = DesktopUser.objects.filter(
                username__regex=r'^staff\d+$',  # Only match staff followed by numbers
                role='staff',
                is_active=True
            ).order_by('username').last()

            if existing_staff:
                # Extract the number from the username
                match = re.search(r'staff(\d+)', existing_staff.username)
                if match:
                    next_num = int(match.group(1)) + 1
                else:
                    next_num = 1
            else:
                # No existing staff users found, start from 1
                next_num = 1

            username = f'staff{next_num}'
            temp_password = f'staff{random.randint(100, 999)}'

            # Double-check that the username doesn't already exist (just in case)
            if DesktopUser.objects.filter(username=username).exists():
                # If it exists, find the next available number
                all_staff_usernames = DesktopUser.objects.filter(
                    username__regex=r'^staff\d+$',
                    role='staff',
                    is_active=True
                ).values_list('username', flat=True)

                # Extract all numbers and find the next available
                used_numbers = []
                for uname in all_staff_usernames:
                    match = re.search(r'staff(\d+)', uname)
                    if match:
                        used_numbers.append(int(match.group(1)))

                if used_numbers:
                    next_num = max(used_numbers) + 1
                else:
                    next_num = 1

                username = f'staff{next_num}'

            staff = DesktopUser(
                username=username,
                full_name=full_name,
                email='',
                phone='',
                role='staff',
                force_password_change=True,
                created_by=admin,
                temp_password=temp_password,  # Store temp password
                temp_password_created_at=timezone.now()
            )
            staff.set_password(temp_password)  # This hashes the password for auth
            staff.save()

            return Response({
                'success': True,
                'staff_account': {
                    'id': staff.id,
                    'username': username,
                    'temp_password': temp_password,  # Return plain text for display
                    'full_name': full_name,
                    'force_password_change': staff.force_password_change,
                    'created_at': staff.created_at
                }
            }, status=status.HTTP_201_CREATED)

        except DesktopUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Admin not found or unauthorized'
            }, status=status.HTTP_403_FORBIDDEN)
class DesktopUserListView(APIView):
    def get(self, request):
        users = DesktopUser.objects.filter(is_active=True).order_by('-created_at')
        user_data = []

        for user in users:
            # Show temp password only if it was created recently (e.g., last 24 hours)
            show_temp_password = (
                    user.force_password_change and
                    user.temp_password and
                    user.temp_password_created_at and
                    (timezone.now() - user.temp_password_created_at).days < 1
            )

            user_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'last_login': user.last_login,
                'created_at': user.created_at,
                'force_password_change': user.force_password_change,
                'temp_password': user.temp_password if show_temp_password else None,
                'show_temp_password': show_temp_password,
            })

        return Response({
            'success': True,
            'users': user_data
        }, status=status.HTTP_200_OK)
class ResetStaffPasswordView(APIView):
    def post(self, request):
        admin_id = request.data.get('admin_id')
        staff_id = request.data.get('staff_id')

        try:
            admin = DesktopUser.objects.get(id=admin_id, role='admin')
            staff = DesktopUser.objects.get(id=staff_id, role='staff')

            # Generate new temporary password
            temp_password = f'staff{random.randint(100, 999)}'

            # Reset staff account
            staff.set_password(temp_password)
            staff.force_password_change = True
            staff.email = ''
            staff.phone = ''
            staff.full_name = f"Staff User"
            staff.temp_password = temp_password  # Store new temp password
            staff.temp_password_created_at = timezone.now()
            staff.save()

            return Response({
                'success': True,
                'new_password': temp_password,
                'staff_account': {
                    'id': staff.id,
                    'username': staff.username,
                    'force_password_change': staff.force_password_change
                }
            }, status=status.HTTP_200_OK)

        except DesktopUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Admin or staff not found'
            }, status=status.HTTP_404_NOT_FOUND)
class FirstTimeSetupView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        try:
            user = DesktopUser.objects.get(id=user_id, force_password_change=True)

            # Check if username is already taken
            if DesktopUser.objects.filter(username=username).exclude(id=user_id).exists():
                return Response({
                    'success': False,
                    'error': 'Username already taken'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update user details and clear temp password
            user.full_name = full_name
            user.email = email
            user.phone = phone
            user.username = username
            user.set_password(new_password)
            user.force_password_change = False
            user.temp_password = None  # Clear temp password after setup
            user.temp_password_created_at = None
            user.save()

            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role,
                    'force_password_change': user.force_password_change,
                    'created_at': user.created_at.isoformat(),
                }
            }, status=status.HTTP_200_OK)

        except DesktopUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found or already setup'
            }, status=status.HTTP_404_NOT_FOUND)


class DesktopUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DesktopUser.objects.all()
    serializer_class = DesktopUserSerializer

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

    try:
        # Appointments (only show pending/overdue)
        appointments = WalkInAppointment.objects.filter(
            status__in=["pending", "overdue"],
            request="accepted"
        ).select_related('service_type', 'pet')

        if pet_id:
            appointments = appointments.filter(pet_id=pet_id)

        for appt in appointments:
            reminders.append({
                "id": appt.id,
                "type": "Appointment",
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.prefTime.strftime("%I:%M %p") if appt.prefTime else None,
                "service": appt.service_type.name if appt.service_type else "Unknown",
                "pet_id": appt.pet.id,
                "pet_name": appt.pet.petName,
                "status": appt.status
            })

        # Services
        services = Service.objects.filter(
            return_date__isnull=False
        ).select_related('service_type', 'pet')

        if pet_id:
            services = services.filter(pet_id=pet_id)

        for svc in services:
            if svc.status == "completed":
                continue

            if svc.return_date < date.today():
                status = "overdue"
            else:
                status = "pending"

            # Get service name with fallback
            service_name = "Unknown"
            if svc.service_type:
                service_name = svc.service_type.name
            elif hasattr(svc, 'service_type_name') and svc.service_type_name:
                service_name = svc.service_type_name

            reminders.append({
                "id": svc.id,
                "type": "Service Return",
                "date": svc.return_date.strftime("%Y-%m-%d"),
                "time": None,
                "service": service_name,
                "pet_id": svc.pet.id,
                "pet_name": svc.pet.petName,
                "status": status
            })

        # Sort by date
        reminders = sorted(reminders, key=lambda x: x["date"])
        return Response(reminders)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def check_duplicate_patient(request):
    try:
        first = (request.data.get("firstName") or "").strip()
        last = (request.data.get("lastName") or "").strip()
        middle = (request.data.get("middleName") or "").strip()
        email = (request.data.get("email") or "").strip().lower()
        current_id = request.data.get("current_id")

        email_conflict = None
        patients = []

        # NAME MATCH CHECK
        query = Q(firstName__iexact=first, lastName__iexact=last)

        if middle:
            query &= (
                Q(middleName__iexact=middle) |
                Q(middleName__isnull=True) |
                Q(middleName__exact="")
            )

        duplicates = basicInfo.objects.filter(query, desktop_record='show')

        if current_id:
            duplicates = duplicates.exclude(id=current_id)

        # EMAIL MATCH CHECK (strict unique)
        email_conflict = basicInfo.objects.filter(email__iexact=email)

        if current_id:
            email_conflict = email_conflict.exclude(id=current_id)

        email_conflict = email_conflict.first()

        # Build name-duplicate list
        for patient in duplicates:
            try:
                pets_qs = patient.pets.all()
            except AttributeError:
                pets_qs = patient.pet_set.all()

            pets = PetSerializer(pets_qs, many=True).data
            patients.append({
                "patient": BasicInfoSerializer(patient).data,
                "pets": pets
            })

        return Response({
            "duplicates": patients,
            "email_conflict": BasicInfoSerializer(email_conflict).data if email_conflict else None
        }, status=200)

    except Exception as e:
        print("Error checking duplicates:", e)
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


class BasicInfoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = basicInfo.objects.all()
    serializer_class = BasicInfoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)

        # Save the basicInfo first
        self.perform_update(serializer)

        # Then sync to linked User if exists
        if instance.user_account:
            user = instance.user_account
            user.first_name = instance.firstName
            user.last_name = instance.lastName
            user.email = instance.email
            user.save()
            print(f"Auto-synced to User {user.id}")

        return Response(serializer.data)
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



@api_view(['GET'])
def patient_combobox_data(request):
    patients = basicInfo.objects.filter(desktop_record="show").order_by('-id')

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


@api_view(['GET'])
def check_time_slot_availability_api(request):
    """API endpoint to check time slot availability"""
    date = request.GET.get('date')
    time_str = request.GET.get('time')

    if not date or not time_str:
        return Response({'error': 'Date and time required'}, status=400)

    try:
        # Check availability using the enhanced function
        is_available, is_past, is_full = check_time_slot_availability(date, time_str)

        # Determine message
        if is_past:
            message = 'Time slot has passed'
        elif is_full:
            message = 'Fully booked'
        else:
            message = 'Available'

        return Response({
            'date': date,
            'time': time_str,
            'available': is_available and not is_past,
            'is_past': is_past,
            'is_full': is_full,
            'message': message
        })

    except Exception as e:
        return Response({
            'date': date,
            'time': time_str,
            'available': True,  # Default to available on error
            'is_past': False,
            'is_full': False,
            'message': 'Available',
            'error': str(e)
        })
def check_time_slot_availability(date, time_str):
    """Check if a time slot has available capacity (max 4 appointments per slot) and is not in the past"""
    try:
        # Convert to date object if it's a string
        if isinstance(date, str):
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date_obj = date

        # Convert time string to time object
        time_obj = datetime.strptime(time_str, '%H:%M:%S').time()

        # Create datetime object for the appointment slot
        appointment_datetime = datetime.combine(date_obj, time_obj)

        # Set Philippines timezone
        ph_tz = pytz.timezone('Asia/Manila')
        appointment_datetime_ph = ph_tz.localize(appointment_datetime)

        # Get current time in Philippines timezone
        now_ph = timezone.now().astimezone(ph_tz)

        # Check if the appointment is in the past
        is_past = appointment_datetime_ph < now_ph

        # If it's in the past, no need to check capacity
        if is_past:
            return False, True, False  # Not available, is past, not full

        # Count appointments for this date and time (only if not in past)
        appointment_count = WalkInAppointment.objects.filter(
            date=date_obj,
            prefTime=time_str,
            request='accepted'
        ).exclude(status='cancelled').count()

        # Return availability status
        is_available = appointment_count < 4
        return is_available, False, not is_available

    except Exception as e:
        print(f"Error checking time slot availability: {e}")
        return True, False, False  # Default to available if there's an error

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

    def get_queryset(self):
        today = date.today()

        # Start with base queryset
        services = Service.objects.all().select_related('service_type', 'owner', 'pet')

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

        return services.order_by("-date")

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
        user = self.request.user

        # Start with base queryset
        queryset = WalkInAppointment.objects.all().select_related(
            'service_type', 'owner', 'pet'
        )

        # Check if user has staff permissions (desktop or admin)
        is_staff_user = user.is_authenticated and (user.is_staff or user.is_superuser)

        # Base queryset logic
        if user.is_authenticated:
            if is_staff_user:
                # Staff/Desktop: see ALL appointments for management
                queryset = queryset.order_by('-created_at')
            else:
                # Regular web user: only show their own appointments
                queryset = queryset.filter(
                    owner__user_account=user
                ).order_by('-created_at')
        else:
            # Unauthenticated request (desktop system) - treat as staff
            queryset = queryset.order_by('-created_at')

        # Rest of your filtering logic...
        request_filter = self.request.query_params.get('request', None)
        if request_filter:
            queryset = queryset.filter(request=request_filter)

        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search_term = self.request.query_params.get('search', '').strip()
        if search_term:
            search_terms = ' '.join(search_term.split()).split()
            if search_terms:
                query = Q()
                for term in search_terms:
                    term_query = (
                            Q(owner__firstName__icontains=term) |
                            Q(owner__lastName__icontains=term) |
                            Q(owner__middleName__icontains=term) |
                            Q(pet__petName__icontains=term) |
                            Q(service_type__name__icontains=term)  # CHANGED: Use service_type__name
                    )
                    query &= term_query
                queryset = queryset.filter(query)

        # Auto-update overdue
        for appt in queryset:
            if appt.status not in ["completed", "cancelled", "overdue"]:
                if appt.date < today:
                    appt.status = "overdue"
                    appt.save(update_fields=["status"])

        return queryset

    def perform_create(self, serializer):
        # Check if user has staff permissions
        is_staff_user = self.request.user.is_authenticated and (
                self.request.user.is_staff or self.request.user.is_superuser
        )

        if self.request.user.is_authenticated and not is_staff_user:
            # Regular web user: pending review
            appointment = serializer.save(request='pending', status='pending')
        else:
            # Staff/Desktop: auto-approved
            appointment = serializer.save(request='accepted')

        # Schedule reminders for the new appointment
        schedule_reminders_for_appointment(appointment)
        send_immediate_reminder_for_today(appointment)


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



#VIEW APPOINTMENTS FOR REACT
class ViewAppointments(generics.ListAPIView):
    serializer_class = WalkInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the basicInfo entry tied to the logged-in user
        user_profile = basicInfo.objects.filter(user_account=self.request.user).first()

        # If user has no profile yet, return empty queryset
        if not user_profile:
            return WalkInAppointment.objects.none()

        # Return only appointments that belong to this owner
        return WalkInAppointment.objects.filter(owner=user_profile).order_by('-date')


class PetListView(generics.ListAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = basicInfo.objects.filter(user_account=self.request.user).first()
        return Pet.objects.filter(owner=user_profile)



# ---- SEND OTP with HTML Email ----
@api_view(['POST'])
def send_reset_otp(request):
    email = request.data.get('email')
    source = request.data.get('source')  # 'web' or 'desktop'

    if not email:
        return Response({'error': 'Email is required.'}, status=400)

    expiry_time = timezone.now() - timezone.timedelta(minutes=10)
    PasswordResetOTP.objects.filter(
        Q(web_user__email=email) | Q(desktop_user__email=email),
        created_at__lt=expiry_time
    ).delete()
    user = None
    user_type = None

    # Check based on source parameter
    if source == 'web':
        try:
            user = User.objects.get(email=email)
            user_type = 'web'
        except User.DoesNotExist:
            return Response({'error': 'No web account found with this email.'}, status=404)

    elif source == 'desktop':
        try:
            user = DesktopUser.objects.get(email=email, is_active=True)
            user_type = 'desktop'
        except DesktopUser.DoesNotExist:
            return Response({'error': 'No desktop account found with this email.'}, status=404)

    else:
        return Response({'error': 'Source parameter is required. Use "web" or "desktop".'}, status=400)

    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Store OTP based on user type with correct field
    if user_type == 'web':
        PasswordResetOTP.objects.create(
            web_user=user,
            otp=otp,
            user_type=user_type
        )
    else:
        PasswordResetOTP.objects.create(
            desktop_user=user,
            otp=otp,
            user_type=user_type
        )

    try:
        subject = "🐾 PetMate Animal Clinic - Password Reset OTP"
        from_email = 'petmateanimalclinic@gmail.com'
        to = [email]

        # Render HTML template (with OTP)
        html_content = render_to_string('otp_email.html', {'otp': otp})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({'message': 'OTP sent successfully to your email.'}, status=200)
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=500)


@api_view(['POST'])
def verify_reset_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not email or not otp:
        return Response({'error': 'Email and OTP are required.'}, status=400)

    try:
        # Try to find OTP record for web user
        web_user = User.objects.get(email=email)
        otp_record = PasswordResetOTP.objects.filter(
            web_user=web_user,
            otp=otp
        ).latest('created_at')
    except User.DoesNotExist:
        # Try to find OTP record for desktop user
        try:
            desktop_user = DesktopUser.objects.get(email=email, is_active=True)
            otp_record = PasswordResetOTP.objects.filter(
                desktop_user=desktop_user,
                otp=otp
            ).latest('created_at')
        except DesktopUser.DoesNotExist:
            return Response({'error': 'No account found with this email.'}, status=404)
    except PasswordResetOTP.DoesNotExist:
        return Response({'error': 'Invalid OTP.'}, status=400)

    # Check if OTP is expired
    if otp_record.is_expired():
        return Response({'error': 'OTP has expired.'}, status=400)

    # If just verifying OTP (no new_password provided)
    if not new_password:
        return Response({'message': 'OTP verified successfully.'}, status=200)

    # If resetting password
    if otp_record.user_type == 'web':
        user = otp_record.web_user
        user.set_password(new_password)
        user.save()
    else:
        user = otp_record.desktop_user
        user.set_password(new_password)
        user.save()

    # Delete used OTP
    otp_record.delete()

    return Response({'message': 'Password reset successfully.'}, status=200)

# GET user info for profile display (Settings)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile = basicInfo.objects.filter(user_account=user).first()

    if request.method == 'GET':
        # Debug logs
        print("DEBUG USER:", user)
        print("DEBUG PROFILE:", profile)

        response_data = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "middle_name": "",
            "email": user.email or "",
            "phoneNumber": "",
            "province": "",
            "city": "", 
            "barangay": "",
            "detailedAddress": "",
            "SecondaryNumber": ""
        }

        if profile:
            response_data.update({
                "middle_name": profile.middleName or "",
                "phoneNumber": profile.phoneNumber or "",
                "SecondaryNumber": profile.SecondaryNumber or "",
                "province": profile.province or "",
                "city": profile.city or "",
                "barangay": profile.barangay or "",
                "detailedAddress": profile.detailedAddress or ""
            })

        return Response(response_data)

    elif request.method == 'PUT':
            try:
                data = request.data
                
                # Extract core fields
                first_name = data.get('first_name', '').strip()
                last_name = data.get('last_name', '').strip()
                email = data.get('email', '').strip()

                # Validate required fields
                if not first_name or not last_name or not email:
                    return Response({"error": "First name, last name, and email are required"}, 
                                status=status.HTTP_400_BAD_REQUEST)

                # Update User model (auth_user)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = email
                user.save()

                # Update or create basicInfo - it already knows the user via user_account
                if profile:
                    # Update all basicInfo fields
                    profile.firstName = first_name
                    profile.lastName = last_name
                    profile.email = email
                    profile.middleName = data.get('middle_name', profile.middleName)
                    profile.phoneNumber = data.get('phoneNumber', profile.phoneNumber)
                    profile.SecondaryNumber = data.get('SecondaryNumber', profile.SecondaryNumber)
                    profile.province = data.get('province', profile.province)
                    profile.city = data.get('city', profile.city)
                    profile.barangay = data.get('barangay', profile.barangay)
                    profile.detailedAddress = data.get('detailedAddress', profile.detailedAddress)
                    profile.save()
                else:
                    # Create new basicInfo - user_account automatically links to current user
                    profile = basicInfo.objects.create(
                        firstName=first_name,
                        lastName=last_name,
                        email=email,
                        middleName=data.get('middle_name', ''),
                        phoneNumber=data.get('phoneNumber', ''),
                        SecondaryNumber=data.get('SecondaryNumber', ''),
                        province=data.get('province', ''),
                        city=data.get('city', ''),
                        barangay=data.get('barangay', ''),
                        detailedAddress=data.get('detailedAddress', ''),
                        user_account=user,  # This links it to the current user
                        source='web',
                        desktop_record='show'
                    )

                return Response({
                    "message": "Profile updated successfully",
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "middle_name": profile.middleName,
                    "phoneNumber": profile.phoneNumber,
                    "SecondaryNumber": profile.SecondaryNumber,
                    "province": profile.province,
                    "city": profile.city,
                    "barangay": profile.barangay,
                    "detailedAddress": profile.detailedAddress
                })

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Add this to your views.py - for desktop app to update users by ID
@api_view(['PUT', 'PATCH'])
def update_user_by_id(request, user_id):
    """Endpoint for desktop app to update user by ID"""
    try:
        user = User.objects.get(id=user_id)
        data = request.data

        print(f"=== DESKTOP UPDATE USER {user_id} ===")
        print(f"Data: {data}")

        # Update user fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        print(f"User {user_id} updated: {user.first_name} {user.last_name}")

        return Response({
            "message": "User updated successfully",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        print(f"ERROR updating user {user_id}: {str(e)}")
        return Response({"error": str(e)}, status=400)

# POST change password (Settings)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def web_reset_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not user.check_password(current_password):
        return Response({'error': 'Incorrect current password'}, status=400)

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)  # Para di ma-logout agad kung gusto mo

    return Response({'message': 'Password changed successfully!'})



# POST contact us message (website)
@api_view(['POST'])
def contact_us_message(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    if not all([name, email, message]):
        return Response({'error': 'All fields are required.'}, status=400)

    try:
        subject = "New Contact Form Message"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        clinic_email = getattr(settings, 'EMAIL_HOST_USER', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost')

        # Send incoming message to clinic (from clinic, reply_to = user)
        email_message = EmailMessage(
            subject=subject,
            body=full_message,
            from_email=clinic_email,
            to=[clinic_email],
            reply_to=[email]
        )
        email_message.send(fail_silently=False)

        # Send Email confirmation sa may user email
        try:
            confirm_subject = "PetMate Animal Clinic — We received your message"
            confirm_body = (
                f"Hi {name},\n\n"
                "Thanks for contacting PetMate Animal Clinic. We received your message and will get back to you shortly.\n\n"
                "Your message:\n"
                f"{message}\n\n"
                "— PetMate Animal Clinic"
            )
            confirmation = EmailMessage(
                subject=confirm_subject,
                body=confirm_body,
                from_email=clinic_email,
                to=[email],
            )
            confirmation.send(fail_silently=True)  # don't fail the whole request if confirmation fails
        except Exception:
            # swallow confirmation errors; clinic already received the message
            pass

        return Response({'message': 'Your message has been received. We will get back to you shortly.'}, status=201)

    except Exception as e:
        return Response({'error': f'Failed to submit message: {str(e)}'}, status=500)


# ---------EMAIL REMINDER---------------

def send_appointment_reminder_email(patient_email, patient_name, pet_name, service_type,
                                    appointment_date, appointment_time, booking_id, reminder_type):
    """Send appointment reminder email"""
    try:
        subject = "🐾 PetMate Animal Clinic - Appointment Reminder"
        from_email = 'petmateanimalclinic@gmail.com'
        to = [patient_email]

        # Render HTML template
        html_content = render_to_string('appointment_reminder.html', {
            'patient_name': patient_name,
            'pet_name': pet_name,
            'service_type': service_type,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'booking_id': booking_id,
            'reminder_type': reminder_type
        })
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return True
    except Exception as e:
        print(f"Failed to send reminder email: {str(e)}")
        return False


def schedule_reminders_for_appointment(appointment):
    """Schedule all reminders for a new appointment"""
    from .models import AppointmentReminder

    # Calculate reminder times - make sure everything is timezone-aware
    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date, appointment.prefTime)
    )

    # Next day reminder (24 hours before)
    next_day_reminder_time = appointment_datetime - timedelta(days=1)

    # Same day reminder (2 hours before)
    same_day_reminder_time = appointment_datetime - timedelta(hours=2)

    # Only schedule if reminder time is in the future
    now = timezone.now()

    if next_day_reminder_time > now:
        AppointmentReminder.objects.create(
            appointment=appointment,
            reminder_type='next_day',
            scheduled_send_time=next_day_reminder_time
        )

    if same_day_reminder_time > now:
        AppointmentReminder.objects.create(
            appointment=appointment,
            reminder_type='same_day',
            scheduled_send_time=same_day_reminder_time
        )

def check_and_send_reminders():
    """Check for pending reminders and send them"""
    from .models import AppointmentReminder

    now = timezone.now()
    pending_reminders = AppointmentReminder.objects.filter(
        sent_at__isnull=True,
        scheduled_send_time__lte=now
    )

    sent_count = 0
    for reminder in pending_reminders:
        if reminder.appointment and reminder.appointment.status not in ['cancelled', 'completed']:
            appointment = reminder.appointment
            success = send_appointment_reminder_email(
                patient_email=appointment.owner.email,
                patient_name=f"{appointment.owner.firstName} {appointment.owner.lastName}",
                pet_name=appointment.pet.petName,
                service_type=appointment.service_name,
                appointment_date=appointment.date.strftime("%B %d, %Y"),
                appointment_time=appointment.prefTime.strftime("%I:%M %p"),
                booking_id=appointment.booking_id,
                reminder_type=reminder.reminder_type
            )

            if success:
                reminder.sent_at = now
                reminder.save()
                sent_count += 1

    return sent_count


def send_immediate_reminder_for_today(appointment):
    """Send immediate reminder for appointments booked for today"""
    now = timezone.now()
    today = now.date()

    # Check if appointment is for today
    if appointment.date == today:
        # Make the appointment datetime timezone-aware
        appointment_datetime = timezone.make_aware(
            datetime.combine(appointment.date, appointment.prefTime)
        )

        # Calculate time difference in hours
        time_diff = (appointment_datetime - now).total_seconds() / 3600

        # Send immediate reminder if appointment is within the next 4 hours
        if 1 <= time_diff <= 4:  # 1-4 hours from now
            patient_email = appointment.owner.email
            patient_name = f"{appointment.owner.firstName} {appointment.owner.lastName}"

            return send_appointment_reminder_email(
                patient_email=patient_email,
                patient_name=patient_name,
                pet_name=appointment.pet.petName,
                service_type=appointment.service_name,
                appointment_date=appointment.date.strftime("%B %d, %Y"),
                appointment_time=appointment.prefTime.strftime("%I:%M %p"),
                booking_id=appointment.booking_id,
                reminder_type='same_day'
            )

    return False


# DESKTOP-ONLY: Reminder monitoring for admin/staff
class ReminderStatusView(APIView):
    def get(self, request):
        """Get reminder system status - Desktop admin only"""
        try:
            # Verify desktop admin user
            admin_user = DesktopUser.objects.get(
                id=request.query_params.get('admin_id'),
                role='admin',
                is_active=True
            )
        except DesktopUser.DoesNotExist:
            return Response({'error': 'Admin access required'}, status=403)

        from datetime import datetime, timedelta

        today = timezone.now().date()
        last_7_days = today - timedelta(days=7)

        # Stats
        sent_today = AppointmentReminder.objects.filter(
            sent_at__date=today
        ).count()

        sent_this_week = AppointmentReminder.objects.filter(
            sent_at__date__gte=last_7_days
        ).count()

        pending_reminders = AppointmentReminder.objects.filter(
            sent_at__isnull=True,
            scheduled_send_time__gte=timezone.now()
        ).count()

        # Recent reminders
        recent_reminders = AppointmentReminder.objects.filter(
            sent_at__date__gte=last_7_days
        ).select_related('appointment', 'appointment__owner', 'appointment__pet').order_by('-sent_at')[:10]

        recent_data = []
        for reminder in recent_reminders:
            if reminder.appointment:
                recent_data.append({
                    'id': reminder.id,
                    'patient_name': f"{reminder.appointment.owner.firstName} {reminder.appointment.owner.lastName}",
                    'pet_name': reminder.appointment.pet.petName,
                    'appointment_date': reminder.appointment.date.strftime("%Y-%m-%d"),
                    'appointment_time': reminder.appointment.prefTime.strftime("%I:%M %p"),
                    'reminder_type': reminder.get_reminder_type_display(),
                    'sent_at': reminder.sent_at.strftime("%Y-%m-%d %I:%M %p") if reminder.sent_at else None,
                })

        return Response({
            'stats': {
                'sent_today': sent_today,
                'sent_this_week': sent_this_week,
                'pending_reminders': pending_reminders,
                'system_status': 'active'
            },
            'recent_reminders': recent_data
        })


# DESKTOP-ONLY: Manual reminder trigger for emergency cases
class ManualReminderView(APIView):
    def post(self, request):
        """Manually send reminder - Desktop admin only for emergency use"""
        try:
            admin_user = DesktopUser.objects.get(
                id=request.data.get('admin_id'),
                role='admin',
                is_active=True
            )
        except DesktopUser.DoesNotExist:
            return Response({'error': 'Admin access required'}, status=403)

        appointment_id = request.data.get('appointment_id')

        try:
            appointment = WalkInAppointment.objects.get(id=appointment_id)

            # Only send if appointment is still valid
            if appointment.status in ['cancelled', 'completed']:
                return Response({
                    'error': 'Cannot send reminder for cancelled/completed appointment'
                }, status=400)

            success = send_appointment_reminder_email(
                patient_email=appointment.owner.email,
                patient_name=f"{appointment.owner.firstName} {appointment.owner.lastName}",
                pet_name=appointment.pet.petName,
                service_type=appointment.service_name,
                appointment_date=appointment.date.strftime("%B %d, %Y"),
                appointment_time=appointment.prefTime.strftime("%I:%M %p"),
                booking_id=appointment.booking_id,
                reminder_type='manual'
            )

            if success:
                # Log this manual reminder
                AppointmentReminder.objects.create(
                    appointment=appointment,
                    reminder_type='manual',
                    scheduled_send_time=timezone.now(),
                    sent_at=timezone.now()
                )
                return Response({'message': 'Manual reminder sent successfully'}, status=200)
            else:
                return Response({'error': 'Failed to send reminder'}, status=500)

        except WalkInAppointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=404)


@api_view(['GET'])
def api_service_counts(request):
    # Count WalkInAppointments by service type name
    data = (
        WalkInAppointment.objects.values('service_type__name')
        .annotate(total=Count('service_type__name'))
        .order_by('service_type__name')
    )

    formatted = {item['service_type__name']: item['total'] for item in data}
    return JsonResponse(formatted)


@api_view(['GET'])
def api_species_counts(request):
    # ✅ Allow optional month from query param (?month=12)
    month = request.GET.get("month")

    if month:
        month = int(month)
    else:
        month = datetime.today().month  # ✅ Default = current month

    # ✅ Monthly filtering (ALL species now respect the selected month)
    cats = Pet.objects.filter(species__icontains="cat", date_added__month=month).count()
    dogs = Pet.objects.filter(species__icontains="dog", date_added__month=month).count()
    others = Pet.objects.filter(date_added__month=month).exclude(
        species__icontains="cat"
    ).exclude(
        species__icontains="dog"
    ).count()

    return Response({
        "month": month,
        "cats": cats,
        "dogs": dogs,
        "others": others
    })


@api_view(["GET"])
def todays_appointments(request):
    today = date.today()
    appointments = WalkInAppointment.objects.filter(
        date=today
    ).exclude(
        status__in=["cancelled", "completed"]
    ).select_related('service_type', 'owner', 'pet')

    result = []
    for a in appointments:
        result.append({
            "owner": str(a.owner),
            "pet_name": str(a.pet.petName),
            "service": a.service_type.name if a.service_type else "Unknown",
            "prefTime": str(a.prefTime)
        })

    return Response(result)

# Add these views to views.py
@api_view(['GET'])
def get_office_hours(request):
    """Get all office hours"""
    try:
        hours = OfficeHours.objects.all().order_by('id')

        # Create default entries if they don't exist
        if hours.count() == 0:
            for day_code, day_name in OfficeHours.DAY_CHOICES:
                default_start = time(8, 0) if day_code not in ['saturday', 'sunday'] else time(9, 0)
                default_end = time(17, 0) if day_code not in ['saturday', 'sunday'] else (
                    time(16, 0) if day_code == 'saturday' else None
                )
                default_status = 'closed' if day_code == 'sunday' else 'open'

                OfficeHours.objects.get_or_create(
                    day=day_code,
                    defaults={
                        'status': default_status,
                        'start_time': default_start,
                        'end_time': default_end
                    }
                )
            hours = OfficeHours.objects.all().order_by('id')

        serializer = OfficeHoursSerializer(hours, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_office_hours(request):
    """Update office hours - for desktop app"""
    data = request.data

    for day_data in data:
        day_name = day_data.get('day')
        try:
            office_hour = OfficeHours.objects.get(day=day_name)

            status = day_data.get('status', 'open')
            office_hour.status = status

            if status == 'open':
                # Parse time from desktop app
                start_time_str = day_data.get('start_time')
                end_time_str = day_data.get('end_time')

                if start_time_str:
                    # Handle different time formats
                    try:
                        # Try HH:MM:SS format
                        office_hour.start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
                    except ValueError:
                        try:
                            # Try HH:MM format
                            office_hour.start_time = datetime.strptime(start_time_str, '%H:%M').time()
                        except ValueError:
                            # Default to 8:00 AM if parsing fails
                            office_hour.start_time = time(8, 0)
                else:
                    office_hour.start_time = None

                if end_time_str:
                    try:
                        # Try HH:MM:SS format
                        office_hour.end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
                    except ValueError:
                        try:
                            # Try HH:MM format
                            office_hour.end_time = datetime.strptime(end_time_str, '%H:%M').time()
                        except ValueError:
                            # Default to 5:00 PM if parsing fails
                            office_hour.end_time = time(17, 0)
                else:
                    office_hour.end_time = None
            else:
                # Clear times for closed/appointment_only
                office_hour.start_time = None
                office_hour.end_time = None

            office_hour.save()

        except OfficeHours.DoesNotExist:
            continue

    return Response({'message': 'Office hours updated successfully'})


class ServiceTypeListCreateView(generics.ListCreateAPIView):
    """List all service types and create new ones"""
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = ServiceType.objects.all()

        # Check if no_pagination parameter is passed (for combobox)
        no_pagination = self.request.query_params.get('no_pagination')
        if no_pagination:
            self.pagination_class = None
            # For combobox, return all active service types
            return queryset.filter(is_active=True).order_by('name')

        # Filter by active status if provided
        is_active = self.request.query_params.get('is_active', '')
        if is_active.lower() == 'true':
            queryset = queryset.filter(is_active=True)
        elif is_active.lower() == 'false':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('-created_at')


class ServiceTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a service type"""
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

    def perform_destroy(self, instance):
        # Soft delete by setting is_active to False
        instance.is_active = False
        instance.save()
# -----------------WALKIN TO NEW ACCOUNT SYNC---------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def check_existing_patient(request):
    """Check if a walk-in patient exists with the given email"""
    email = request.data.get('email', '').strip().lower()

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=400)

    # Check if email already has a web account
    if User.objects.filter(email=email).exists():
        return Response({
            'has_account': True,
            'message': 'An account already exists with this email. Please login instead.'
        })

    # Check for walk-in patient with this email
    patient = basicInfo.objects.filter(
        email=email,
        source='desktop',
        user_account__isnull=True
    ).first()

    if patient:
        # Check if verification was sent recently (last 2 minutes)
        two_minutes_ago = timezone.now() - timedelta(minutes=2)
        recent_verification = EmailVerification.objects.filter(
            email=email,
            patient=patient,
            created_at__gte=two_minutes_ago
        ).first()

        if recent_verification and not recent_verification.verified:
            # Don't resend if sent recently, just return the existing verification
            return Response({
                'has_existing_record': True,
                'patient_id': patient.id,
                'patient_name': f"{patient.firstName} {patient.lastName}",
                'verification_id': recent_verification.id,
                'message': 'Verification code already sent. Check your email.',
                'already_sent': True  # Flag to indicate no new email was sent
            })

        # Generate new OTP
        otp = str(random.randint(100000, 999999))
        verification = EmailVerification.objects.create(
            email=email,
            otp=otp,
            patient=patient,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # Send OTP email
        try:
            subject = "🐾 PetMate Animal Clinic - Verify Your Email"
            html_content = render_to_string('claim_account_email.html', {
                'otp': otp,
                'patient_name': f"{patient.firstName} {patient.lastName}",
                'expiry_minutes': 10
            })
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email='petmateanimalclinic@gmail.com',
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({
                'has_existing_record': True,
                'patient_id': patient.id,
                'patient_name': f"{patient.firstName} {patient.lastName}",
                'verification_id': verification.id,
                'message': 'We found an existing walk-in record. OTP sent to your email.'
            })

        except Exception as e:
            print(f"Error sending email: {e}")
            return Response({
                'error': 'Failed to send verification email'
            }, status=500)

    return Response({
        'has_existing_record': False,
        'message': 'No existing walk-in record found. You can create a new account.'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_and_claim_account(request):
    """Verify OTP and create web account for walk-in patient"""
    data = request.data
    verification_id = data.get('verification_id')
    otp = data.get('otp')
    password = data.get('password')

    if not all([verification_id, otp, password]):
        return Response({'error': 'All fields are required'}, status=400)

    try:
        verification = EmailVerification.objects.get(
            id=verification_id,
            otp=otp,
            verified=False
        )

        # Check if OTP is expired
        if verification.is_expired():
            return Response({'error': 'OTP has expired. Please request a new one.'}, status=400)

        # Check if patient still exists and hasn't been claimed
        patient = verification.patient
        if patient.user_account:
            return Response({'error': 'This record has already been claimed.'}, status=400)

        # Create User account
        User = get_user_model()
        try:
            with transaction.atomic():
                # Create user with email as username
                user = User.objects.create_user(
                    username=verification.email,
                    email=verification.email,
                    password=password
                )
                user.first_name = patient.firstName
                user.last_name = patient.lastName
                user.save()

                # Link patient to user account
                patient.user_account = user
                patient.source = 'web'  # Update source
                patient.desktop_record = 'show'  # Show in both systems
                patient.save()

                # Mark verification as complete
                verification.verified = True
                verification.user_account_created = True
                verification.save()

                # Log the user in
                try:
                    auth_request = request._request if hasattr(request, '_request') else request
                    django_login(auth_request, user)
                except Exception as e:
                    print(f"Login failed but account created: {e}")

                return Response({
                    'success': True,
                    'message': 'Account created successfully! Your walk-in records have been linked.',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    },
                    'patient': {
                        'id': patient.id,
                        'full_name': f"{patient.firstName} {patient.lastName}"
                    }
                })

        except Exception as e:
            return Response({'error': f'Failed to create account: {str(e)}'}, status=500)

    except EmailVerification.DoesNotExist:
        return Response({'error': 'Invalid or expired verification code.'}, status=400)
from rest_framework import generics, status, permissions, viewsets
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import date,datetime,time
from .models import *
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

import random
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User

from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError






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

        # Check if user has staff permissions (desktop or admin)
        is_staff_user = user.is_authenticated and (user.is_staff or user.is_superuser)

        # Base queryset logic
        if user.is_authenticated:
            if is_staff_user:
                # Staff/Desktop: see ALL appointments for management
                queryset = WalkInAppointment.objects.all().order_by('-created_at')
            else:
                # Regular web user: only show their own appointments
                queryset = WalkInAppointment.objects.filter(
                    owner__user_account=user
                ).order_by('created_at')
        else:
            # Unauthenticated request (desktop system) - treat as staff
            queryset = WalkInAppointment.objects.all().order_by('-created_at')

        # Rest of your filtering logic remains the same...
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
                            Q(service_name__icontains=term)
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
            serializer.save(request='pending', status='pending')
        else:
            # Staff/Desktop: auto-approved
            serializer.save(request='accepted')


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

    if not email:
        return Response({'error': 'Email is required.'}, status=400)

    user = None
    user_type = None

    # Check Django User model first (web users)
    try:
        user = User.objects.get(email=email)
        user_type = 'web'
    except User.DoesNotExist:
        # Check DesktopUser model if not found in User model
        try:
            user = DesktopUser.objects.get(email=email, is_active=True)
            user_type = 'desktop'
        except DesktopUser.DoesNotExist:
            return Response({'error': 'No account found with this email.'}, status=404)

    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Store OTP based on user type with correct field
    if user_type == 'web':
        PasswordResetOTP.objects.create(
            web_user=user,  # Use web_user field
            otp=otp,
            user_type=user_type
        )
    else:
        PasswordResetOTP.objects.create(
            desktop_user=user,  # Use desktop_user field
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

    if not all([email, otp, new_password]):
        return Response({'error': 'All fields are required.'}, status=400)

    # Find user and type
    user = None
    user_type = None

    # Check both models
    try:
        user = User.objects.get(email=email)
        user_type = 'web'
    except User.DoesNotExist:
        try:
            user = DesktopUser.objects.get(email=email, is_active=True)
            user_type = 'desktop'
        except DesktopUser.DoesNotExist:
            return Response({'error': 'Invalid email.'}, status=404)

    # Find OTP record with correct field based on user type
    if user_type == 'web':
        otp_record = PasswordResetOTP.objects.filter(
            web_user=user,  # Use web_user field for web users
            otp=otp,
            user_type=user_type
        ).last()
    else:
        otp_record = PasswordResetOTP.objects.filter(
            desktop_user=user,  # Use desktop_user field for desktop users
            otp=otp,
            user_type=user_type
        ).last()

    if not otp_record:
        return Response({'error': 'Invalid OTP.'}, status=400)

    if otp_record.is_expired():
        otp_record.delete()
        return Response({'error': 'OTP expired.'}, status=400)

    # Check if new password is different from current
    if user.check_password(new_password):
        return Response({'error': 'New password must be different from your current password.'}, status=400)

    # Validate password strength
    try:
        validate_password(new_password, user=user)
    except ValidationError as ve:
        return Response({'error': ve.messages}, status=400)

    # Reset password based on user type
    user.set_password(new_password)
    user.save()
    otp_record.delete()

    return Response({'message': 'Password reset successfully.'}, status=200)

# GET user info for profile display (Settings)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # Safely fetch the related basicInfo record
    profile = basicInfo.objects.filter(user_account=user).first()

    # Debug logs (will show in Django console)
    print("DEBUG USER:", user)
    print("DEBUG PROFILE:", profile)

    response_data = {
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "middle_name": "",
        "email": user.email or "",
        "phoneNumber": "",
    }

    if profile:
        response_data["middle_name"] = profile.middleName or ""
        response_data["phoneNumber"] = profile.phoneNumber or ""

    return Response(response_data)



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


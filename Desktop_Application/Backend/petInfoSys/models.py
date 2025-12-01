from datetime import date
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #para sa auth_user

from datetime import timedelta

#-----------------------------------------DESKTOP WEBSITE MODELS------------------------------

class DesktopUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
    ]

    # Required fields
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    # Password field (we'll hash passwords like Django auth does)
    password = models.CharField(max_length=128)  # Same as auth_user

    # Status flags
    force_password_change = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # For staff accounts, track who created them
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'
    )
    temp_password = models.CharField(max_length=128, blank=True, null=True)
    temp_password_created_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.role})"

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

class basicInfo(models.Model):
    SOURCE_CHOICES = [
        ('desktop', 'Desktop System'),
        ('web', 'Website'),
    ]

    DESKTOP_RECORD_CHOICES = [
        ('show', 'Show in Desktop Records'),
        ('hide', 'Hide from Desktop Records'),
    ]

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middleName = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=255)
    SecondaryNumber = models.CharField(max_length=255,null=True, blank=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    detailedAddress = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    # NEW FIELDS - Add these
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='desktop')
    desktop_record = models.CharField(
        max_length=10,
        choices=DESKTOP_RECORD_CHOICES,
        default='show'
    )
    user_account = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_profiles'
    )

    def __str__(self):
        parts = [self.firstName, self.middleName, self.lastName]
        return " ".join(p for p in parts if p)

    def save(self, *args, **kwargs):
        # Auto-set based on source
        if self.source == 'desktop' and not self.pk:
            self.desktop_record = 'show'
        elif self.source == 'web' and not self.pk:
            self.desktop_record = 'hide'
        super().save(*args, **kwargs)

class Pet(models.Model):
    owner = models.ForeignKey(
        "basicInfo",
        on_delete=models.CASCADE,
        related_name="pets"
    )
    petName = models.CharField(max_length=255)
    petColor = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    birthDay = models.DateField(null=True, blank=True)  # optional

    stored_age = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=50)
    remarks = models.CharField(max_length=350, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.petName} (Owner: {self.owner.firstName})"

    @property
    def age(self):
        if self.birthDay:
            today = date.today()
            days = (today - self.birthDay).days

            if days < 7:
                return f"{days} day{'s' if days != 1 else ''} old"
            elif days < 30:
                weeks = days // 7
                return f"{weeks} week{'s' if weeks != 1 else ''} old"
            elif days < 365:
                months = days // 30
                return f"{months} month{'s' if months != 1 else ''} old"
            else:
                years = days // 365
                return f"{years} year{'s' if years != 1 else ''} old"
        return self.stored_age or "Unknown"



class Service(models.Model):
    owner = models.ForeignKey(
        basicInfo,
        on_delete=models.CASCADE,
        related_name='services'
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='services'
    )
    service_type = models.CharField(max_length=255)
    date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # optional
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    def __str__(self):
        return f"Service: {self.service_type} for {self.pet.petName} ({self.date})"

class WalkInAppointment(models.Model):
    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    owner = models.ForeignKey(basicInfo, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField()
    prefTime = models.TimeField()
    status = models.CharField(max_length=20, default='pending')
    service_name = models.CharField(max_length=100, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
    request = models.CharField(max_length=20, default='accepted')

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        super().save(*args, **kwargs)
    
    def generate_booking_id(self):
        import random
        import string
        from datetime import datetime
        
        # Format: BK + YYMMDD + 4 random chars
        date_part = datetime.now().strftime('%y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        booking_id = f"BK{date_part}{random_part}"
        
        # Ensure uniqueness
        while WalkInAppointment.objects.filter(booking_id=booking_id).exists():
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            booking_id = f"BK{date_part}{random_part}"
        
        return booking_id



#--------- FORGOT PASSWORD  MODEL ---------

# Model for Password Reset OTP
class PasswordResetOTP(models.Model):
    # Store both possibilities
    web_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    desktop_user = models.ForeignKey('DesktopUser', on_delete=models.CASCADE, null=True, blank=True)

    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=[('web', 'Web'), ('desktop', 'Desktop')], default='web')

    @property
    def user(self):
        return self.web_user or self.desktop_user

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user} ({self.user_type})"


# -----------------EMAIL REMINDER MODEL------------------
class AppointmentReminder(models.Model):
    REMINDER_TYPES = [
        ('next_day', 'Next Day Reminder'),
        ('same_day', 'Same Day Reminder'),
        ('service_return', 'Service Return Reminder'),
    ]

    appointment = models.ForeignKey(WalkInAppointment, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    scheduled_send_time = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reminder_type} - {self.scheduled_send_time}"

# -----------------DYNAMIC WEB DETAILS------------------
class OfficeHours(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('appointment_only', 'Appointment Only'),
        ('closed', 'Closed'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Office Hours"
        ordering = ['id']

    def __str__(self):
        return f"{self.get_day_display()} - {self.get_status_display()}"


class ServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Service Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().title()
        super().save(*args, **kwargs)
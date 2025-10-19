from datetime import date
import uuid
from django.db import models

from django.contrib.auth.models import User #para sa auth_user

#-----------------------------------------DESKTOP WEBSITE MODELS------------------------------
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


    

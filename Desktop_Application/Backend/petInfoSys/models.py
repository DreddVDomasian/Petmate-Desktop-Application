from datetime import date
import uuid
from django.db import models

from django.contrib.auth.models import User #para sa auth_user

#-----------------------------------------DESKTOP WEBSITE MODELS------------------------------
class basicInfo(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middleName = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    detailedAddress = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    emergencyNumber = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parts = [self.firstName, self.middleName, self.lastName]
        return " ".join(p for p in parts if p)

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

#-----------------------------------------APPOINTMENT WEBSITE MODELS------------------------------

#---------------------------PCLIENTS--------------------------
class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('new', 'New Client'),
        ('returning', 'Returning Client'),
    ]

    # Client Information
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)

    # Address Information
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    detailed_address = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pclients' # custom table name sa database
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        return f"{self.detailed_address}, {self.barangay}, {self.city}, {self.province}"



#---------------------------PPETS--------------------------
class PetWeb(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'Other'),
    ]

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # Foreign Key to Client
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pets')

    # Pet Information
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ppets'  # custom table name sa database
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet_name} ({self.client.full_name})"



#---------------------------PAPPOINTMENTS--------------------------
class AppointmentType(models.Model):
    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    REASON_CHOICES = [
        ('vaccination', 'Vaccination'),
        ('checkup', 'Check-up'),
        ('surgery', 'Surgery'),
        ('consultations', 'Consultations'),
        ('deworming', 'Deworming'),
    ]

    PROVIDER_CHOICES = [
        ('dr_gonzales', 'Dr. Gonzales'),
        ('dr_domasian', 'Dr. Domasian'),
        ('dr_jerusalem', 'Dr. Jerusalem'),
        ('dr_moleno', 'Dr. Moleno'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    # Foreign Keys
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    pet = models.ForeignKey(PetWeb, on_delete=models.CASCADE, related_name='appointments')

    # Appointment Information
    appointment_reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    provider = models.CharField(max_length=100, choices=PROVIDER_CHOICES)
    appointment_datetime = models.CharField(max_length=100)  # Store as string for simplicity
    comments = models.TextField(blank=True, null=True, max_length=400)

    # Status Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        while AppointmentType.objects.filter(booking_id=booking_id).exists():
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            booking_id = f"BK{date_part}{random_part}"
        
        return booking_id

    class Meta:
        db_table = 'pappointment_types' # custom table name sa database
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.full_name} - {self.pet.pet_name} ({self.appointment_reason})"



#---------------------------REACT PETS------------------------


class ReactPet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=50)
    remarks = models.CharField(max_length=350, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
    

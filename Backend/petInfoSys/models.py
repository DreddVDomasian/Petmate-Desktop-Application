from django.db import models

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
        basicInfo,
        on_delete=models.CASCADE,
        related_name='pets'
    )
    petName = models.CharField(max_length=255)
    petColor = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    birthDay = models.DateField(null=True, blank=True)  # optional
    age = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    remarks = models.CharField(max_length=350, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.petName} (Owner: {self.owner.firstName})"

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
    owner = models.ForeignKey(basicInfo, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField()
    prefTime = models.TimeField()
    status = models.CharField(max_length=20, default='pending')
    service_name = models.CharField(max_length=100, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
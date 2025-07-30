from django.db import models

class basicInfo(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    detailedAddress = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    emergencyNumber = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

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
    age = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)

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
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Service: {self.service_type} for {self.pet.petName} ({self.date})"

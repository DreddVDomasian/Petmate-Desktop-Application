from django.core.management.base import BaseCommand
from faker import Faker
import random
from petInfoSys.models import basicInfo, Pet, Service, WalkInAppointment, ServiceType
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--records', type=int, default=1000,
                            help='Number of clients to generate')

    def handle(self, *args, **kwargs):
        num_records = kwargs['records']
        self.stdout.write(f"Generating {num_records} basicInfo records...")

        # Ensure we have service types to choose from
        default_types = ["Vaccination", "Check-up", "Deworming"]
        for t in default_types:
            ServiceType.objects.get_or_create(name=t, defaults={"is_active": True})

        service_types = list(ServiceType.objects.filter(is_active=True))

        owners = []
        for _ in range(num_records):
            owner = basicInfo.objects.create(
                firstName=fake.first_name(),
                lastName=fake.last_name(),
                middleName=fake.first_name() if random.choice([True, False]) else None,
                phoneNumber=fake.phone_number(),
                province=fake.state(),
                city=fake.city(),
                barangay=fake.street_name(),
                detailedAddress=fake.street_address(),
                email=fake.email(),
                SecondaryNumber=fake.phone_number()
            )
            owners.append(owner)

            # Generate 1–2 pets per owner
            for _ in range(random.randint(1, 2)):
                pet = Pet.objects.create(
                    owner=owner,
                    petName=fake.first_name(),
                    petColor=random.choice(["Brown", "Black", "White", "Mixed"]),
                    breed=random.choice(["Poodle", "Labrador", "Bulldog", "Siamese"]),
                    species=random.choice(["Dog", "Cat"]),
                    sex=random.choice(["Male", "Female"]),
                    birthDay=fake.date_of_birth(minimum_age=0, maximum_age=15),
                )

                # Create 1–2 services per pet
                for _ in range(random.randint(1, 2)):
                    chosen_type = random.choice(service_types)

                    return_date = (
                        None
                        if random.choice([True, False])
                        else fake.date_between(start_date="today", end_date="+1y")
                    )

                    Service.objects.create(
                        owner=owner,
                        pet=pet,
                        service_type=chosen_type,  # <-- FIXED
                        date=fake.date_between(start_date="-2y", end_date="today"),
                        return_date=return_date,
                        status=random.choice(["pending", "completed", "overdue"]),
                    )

                # 0–2 walk-in appointments
                for _ in range(random.randint(0, 2)):
                    WalkInAppointment.objects.create(
                        owner=owner,
                        pet=random.choice(owner.pets.all()),
                        date=fake.date_this_year(),
                        prefTime=fake.time(),
                        service_type=chosen_type,
                        status=random.choice(["pending", "completed", "overdue", "cancelled"]),
                        request=random.choice(["pending", "accepted", "declined"]),
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {num_records} owners with pets & appointments!"
        ))

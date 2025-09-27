
from django.core.management.base import BaseCommand
from faker import Faker
import random
from petInfoSys.models import basicInfo, Pet, Service, WalkInAppointment,Client, PetWeb, AppointmentType
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--records', type=int, default=1000, help='Number of clients to generate')

    def handle(self, *args, **kwargs):
        num_records = kwargs['records']
        self.stdout.write(f"Generating {num_records} basicInfo records...")

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
                emergencyNumber=fake.phone_number()
            )
            owners.append(owner)

            # Generate 1-3 pets per owner
            for _ in range(random.randint(1, 3)):
                pet = Pet.objects.create(
                    owner=owner,
                    petName=fake.first_name(),
                    petColor=random.choice(["Brown", "Black", "White", "Mixed"]),
                    breed=random.choice(["Poodle", "Labrador", "Bulldog", "Siamese"]),
                    species=random.choice(["Dog", "Cat"]),
                    sex=random.choice(["Male", "Female"]),
                    birthDay=fake.date_of_birth(minimum_age=0, maximum_age=15),
                )

                # Add 0-2 services
                for _ in range(random.randint(0, 2)):
                    Service.objects.create(
                        owner=owner,
                        pet=pet,
                        service_type=random.choice(["Vaccination", "Check-up", "Deworming"]),
                        date=fake.date_between(start_date="-2y", end_date="today"),
                        status=random.choice(["pending", "completed", "overdue", "cancelled"]),
                    )

            # Add 0-2 walk-in appointments
            for _ in range(random.randint(0, 2)):
                WalkInAppointment.objects.create(
                    owner=owner,
                    pet=random.choice(owner.pets.all()),
                    date=fake.date_this_year(),
                    prefTime=fake.time(),
                    service_name=random.choice(["Consultation", "Surgery"]),
                    status=random.choice(["pending", "completed", "overdue", "cancelled"]),
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_records} owners with pets & appointments!"))


        self.stdout.write(f"\nGenerating {num_records} web Client records...")

        clients = []
        for _ in range(num_records):
            client = Client.objects.create(
                client_type=random.choice(['new', 'returning']),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                emergency_contact=fake.phone_number(),
                province=fake.state(),
                city=fake.city(),
                barangay=fake.street_name(),
                detailed_address=fake.street_address(),
            )
            clients.append(client)

            # Generate 1-3 Web Pets
            for _ in range(random.randint(1, 3)):
                pet_web = PetWeb.objects.create(
                    client=client,
                    pet_name=fake.first_name(),
                    species=random.choice(['dog', 'cat', 'other']),
                    breed=random.choice(["Poodle", "Labrador", "Bulldog", "Siamese"]),
                    color=random.choice(["Brown", "Black", "White", "Mixed"]),
                    sex=random.choice(['male', 'female']),
                )

                # Generate 0-2 Appointments (Pending)
                for _ in range(random.randint(0, 2)):
                    AppointmentType.objects.create(
                        client=client,
                        pet=pet_web,
                        appointment_reason=random.choice([r[0] for r in AppointmentType.REASON_CHOICES]),
                        provider=random.choice([p[0] for p in AppointmentType.PROVIDER_CHOICES]),
                        appointment_datetime=str(fake.date_time_this_month()),
                        comments=fake.sentence(),
                        status=random.choice(["pending", "accepted", "declined"]),
                    )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_records} web clients, pets, and pending appointments!"))

from django.db import migrations


def add_default_services(apps, schema_editor):
    ServiceType = apps.get_model('petInfoSys', 'ServiceType')

    default_services = [
        ('Consultation', 'General veterinary consultation and examination', True),
        ('Wellness Check', 'Comprehensive health assessment and preventive care', True),
        ('Vaccinations', 'Immunization against common diseases', True),
        ('Deworming & Tick and Flea Prevention', 'Parasite control and prevention treatments', True),
        ('Surgery', 'Various surgical procedures', True),
        ('Comprehensive Hematology (CBC)', 'Complete blood count testing', True),
        ('Blood Chemistry', 'Biochemical profile testing', True),
        ('Progesterone Test', 'Hormone level testing', True),
        ('Pregnancy Test (Relaxin)', 'Canine pregnancy detection', True),
        ('Diagnostic Microscopy', 'Microscopic examination of samples', True),
        ('Urinalysis', 'Urine testing and analysis', True),
        ('Antigen/Antibody Rapid Test Kits', 'Rapid diagnostic testing', True),
        ('Wellness Product Supplies', 'Pet wellness products and supplies', True),
        ('Grooming', 'Pet grooming and hygiene services', True),
        ('Dental Care', 'Oral health and dental treatments', True),
        ('Emergency Care', 'Urgent and emergency veterinary services', True),
        ('Check-up', 'Routine health check-up', True),
        ('Consultations', 'Professional veterinary consultations', True),
        ('Tick & Flea Prevention', 'Preventive treatment for parasites', True),
    ]

    for name, description, is_default in default_services:
        ServiceType.objects.update_or_create(
            name=name,
            defaults={
                'description': description,
                'is_default': is_default,
                'is_active': True
            }
        )


def reverse_default_services(apps, schema_editor):
    ServiceType = apps.get_model('petInfoSys', 'ServiceType')
    ServiceType.objects.filter(is_default=True).update(is_default=False)


class Migration(migrations.Migration):
    dependencies = [
        ('petInfoSys', '0036_servicetype'),  # Use your actual migration number
    ]

    operations = [
        migrations.RunPython(add_default_services, reverse_default_services),
    ]
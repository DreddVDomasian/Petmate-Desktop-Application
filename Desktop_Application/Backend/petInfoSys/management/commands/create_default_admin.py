from django.core.management.base import BaseCommand
from petInfoSys.models import DesktopUser


class Command(BaseCommand):
    help = 'Creates the default admin account for desktop system'

    def handle(self, *args, **options):
        if not DesktopUser.objects.filter(role='admin').exists():
            admin = DesktopUser(
                username='admin',
                full_name='System Administrator',
                email='admin@petmate.com',  # Will be changed on first login
                role='admin',
                force_password_change=True
            )
            admin.set_password('admin123')  # Temporary password
            admin.save()

            self.stdout.write(
                self.style.SUCCESS('Default admin account created!')
            )
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
        else:
            self.stdout.write('Admin account already exists.')
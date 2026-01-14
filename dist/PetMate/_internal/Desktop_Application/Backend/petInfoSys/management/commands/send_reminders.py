import os
import django
from django.core.management.base import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from petInfoSys.views import check_and_send_reminders


class Command(BaseCommand):
    help = 'Send scheduled appointment reminders'

    def handle(self, *args, **options):
        self.stdout.write('Checking for pending reminders...')
        sent_count = check_and_send_reminders()
        self.stdout.write(f'Reminder check completed. Sent {sent_count} reminders.')
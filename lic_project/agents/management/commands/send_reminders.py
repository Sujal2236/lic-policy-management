from django.core.management.base import BaseCommand
from agents.reminders import send_email_reminders

class Command(BaseCommand):
    help = 'Send premium due date email reminders'

    def handle(self, *args, **kwargs):
        count = send_email_reminders()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {count} email reminders!')
        )
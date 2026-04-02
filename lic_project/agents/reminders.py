from datetime import date, timedelta
from django.core.mail import send_mail
from .models import PolicyHolder

def send_email_reminders():
    today = date.today()
    target_date = today + timedelta(days=10)

    policies = PolicyHolder.objects.filter(
        next_due_date=target_date,
        email__isnull=False
    ).exclude(email='')

    count = 0
    for policy in policies:
        send_mail(
            subject='LIC Premium Due Reminder',
            message=f"""Dear {policy.holder_name},

This is a reminder that your LIC premium payment is due in 10 days.

Policy Number : {policy.policy_number}
Due Date      : {policy.next_due_date}
Amount        : ₹{policy.total_amount}

Please make your payment on time to avoid policy lapse.

Regards,
LIC Agent Management System""",
            from_email=None,
            recipient_list=[policy.email],
            fail_silently=False,
        )
        count += 1

    return count
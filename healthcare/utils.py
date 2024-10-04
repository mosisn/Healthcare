# utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_email_reminder(appointment):
    """
    Send an email reminder for a scheduled appointment.

    This function constructs an email message with the appointment details
    and sends it to the patient's email address.

    Args:
        appointment (Appointment): The appointment object containing details
            such as appointment time and the associated patient.

    Raises:
        Exception: If the email sending fails, an exception will be raised.
    """
    subject = 'Appointment Reminder'
    message = f'Reminder: You have an appointment scheduled for {appointment.appointment_time}.'
    recipient_list = [appointment.patient.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

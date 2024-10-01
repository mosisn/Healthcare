from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model adds a role field to differentiate between admin, doctor, and patient users.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    @property
    def full_name(self):
        """
        Get the full name of the user.

        Returns:
            str: The full name composed of first and last name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        """
        String representation of the User instance.

        Returns:
            str: The username and role of the user.
        """
        return f"{self.username} ({self.role})"

class Doctor(models.Model):
    """
    Model representing a doctor profile.

    This model contains information about the doctor, including specialization, availability,
    years of experience, and contact details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    availability = models.JSONField(help_text="Store available slots as JSON")
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")
    contact_number = models.CharField(max_length=10, blank=True, help_text="Contact number")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save method to validate specialization and experience years.

        Raises:
            ValidationError: If specialization is empty or experience years are negative.
        """
        if not self.specialization:
            raise ValidationError("Specialization cannot be empty.")
        if self.experience_years < 0:
            raise ValidationError("Experience years cannot be negative.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Doctor instance.

        Returns:
            str: The doctor's username and specialization.
        """
        return f"Dr. {self.user.username} - {self.specialization}"

class Patient(models.Model):
    """
    Model representing a patient profile.

    This model contains information about the patient, including medical history, date of birth,
    and contact details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    email = models.EmailField()
    medical_history = models.TextField(blank=True, help_text="Patient's medical history")
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, help_text="Contact number")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save method to validate date of birth.

        Raises:
            ValidationError: If date of birth is in the future.
        """
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Patient instance.

        Returns:
            str: The patient's username.
        """
        return f"Patient: {self.user.username}"

class Appointment(models.Model):
    """
    Model representing an appointment between a patient and a doctor.

    This model contains details about the appointment, including status and timestamps.
    """
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save method to validate appointment time and user roles.

        Raises:
            ValidationError: If appointment time is in the past or user roles are incorrect.
        """
        if self.appointment_time < timezone.now():
            raise ValidationError("Appointment time cannot be in the past.")
        if self.patient.user.role != 'patient':
            raise ValidationError("The user must be a patient.")
        if self.doctor.user.role != 'doctor':
            raise ValidationError("The user must be a doctor.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Appointment instance.

        Returns:
            str: The appointment details including doctor, patient, and appointment time.
        """
        return f"Appointment: {self.doctor} with {self.patient} on {self.appointment_time}"

class MedicalRecord(models.Model):
    """
    Model representing a medical record for a patient.

    This model contains notes from the doctor regarding the patient's medical history.
    """
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='medical_records')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save method to validate notes.

        Raises:
            ValidationError: If notes are empty.
        """
        if not self.notes:
            raise ValidationError("Notes cannot be empty.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the MedicalRecord instance.

        Returns:
            str: The record details including patient, doctor, and creation timestamp.
        """
        return f"Record for {self.patient} by {self.doctor} on {self.created_at}"

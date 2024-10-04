from rest_framework import serializers
from .models import User, Doctor, Patient, Appointment, MedicalRecord
from django.utils import timezone
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    This serializer handles the serialization and deserialization of User instances, 
    including validation for unique usernames and password strength.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new user instance with a hashed password.

        Args:
            validated_data (dict): The validated data for creating a user.

        Returns:
            User: The created user instance.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, value):
        """
        Validate that the username is unique.

        Args:
            value (str): The username to validate.

        Raises:
            serializers.ValidationError: If the username already exists.

        Returns:
            str: The validated username.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        """
        Validate the strength of the password.

        Args:
            value (str): The password to validate.

        Raises:
            serializers.ValidationError: If the password is less than 8 characters.

        Returns:
            str: The validated password.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.

    This serializer manages the serialization and validation of Doctor instances,
    ensuring that required fields are provided and valid.
    """
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'availability', 'experience_years', 'contact_number', 'created_at', 'modified_at']
        read_only_fields = ['user', 'created_at', 'modified_at']

    def validate_specialization(self, value):
        """
        Validate that the specialization is not empty.

        Args:
            value (str): The specialization to validate.

        Raises:
            serializers.ValidationError: If the specialization is empty.

        Returns:
            str: The validated specialization.
        """
        if not value:
            raise serializers.ValidationError("Specialization cannot be empty.")
        return value

    def validate_experience_years(self, value):
        """
        Validate that the years of experience are non-negative.

        Args:
            value (int): The years of experience to validate.

        Raises:
            serializers.ValidationError: If the years of experience are negative.

        Returns:
            int: The validated years of experience.
        """
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative.")
        return value

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.

    This serializer handles the serialization and validation of Patient instances,
    ensuring that required fields are provided and valid.
    """
    class Meta:
        model = Patient
        fields = ['id', 'user', 'medical_history', 'date_of_birth', 'contact_number', 'created_at', 'modified_at']
        read_only_fields = ['user', 'created_at', 'modified_at']

    def validate_date_of_birth(self, value):
        """
        Validate that the date of birth is not in the future.

        Args:
            value (date): The date of birth to validate.

        Raises:
            serializers.ValidationError: If the date of birth is in the future.

        Returns:
            date: The validated date of birth.
        """
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.

    This serializer manages the serialization and validation of Appointment instances,
    ensuring that appointment times are valid and associated users are of the correct roles.
    """
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_time', 'status', 'created_at', 'modified_at']
        read_only_fields = ['created_at', 'modified_at']

    def validate_appointment_time(self, value):
        """
        Validate that the appointment time is not in the past.

        Args:
            value (datetime): The appointment time to validate.

        Raises:
            serializers.ValidationError: If the appointment time is in the past.

        Returns:
            datetime: The validated appointment time.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Appointment time cannot be in the past.")
        return value

    def validate(self, attrs):
        """
        Validate that the associated patient and doctor have the correct roles.

        Args:
            attrs (dict): The attributes of the appointment.

        Raises:
            serializers.ValidationError: If the patient or doctor role is incorrect.

        Returns:
            dict: The validated attributes.
        """
        if attrs['patient'].user.role != 'patient':
            raise serializers.ValidationError("The user must be a patient.")
        if attrs['doctor'].user.role != 'doctor':
            raise serializers.ValidationError("The user must be a doctor.")
        return attrs

class MedicalRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for MedicalRecord model.

    This serializer handles the serialization and validation of MedicalRecord instances,
    ensuring that notes are provided and valid.
    """
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'notes', 'created_at', 'modified_at']
        read_only_fields = ['created_at', 'modified_at']

    def validate_notes(self, value):
        """
        Validate that the notes are not empty.

        Args:
            value (str): The notes to validate.

        Raises:
            serializers.ValidationError: If the notes are empty.

        Returns:
            str: The validated notes.
        """
        if not value:
            raise serializers.ValidationError("Notes cannot be empty.")
        return value

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the serialization and validation of user registration data,
    ensuring that the password is securely set.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        """
        Create a new user instance with a hashed password.

        Args:
            validated_data (dict): The validated data for creating a user.

        Returns:
            User: The created user instance.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer handles the validation of login credentials and authenticates the user.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the user credentials for login.

        Args:
            attrs (dict): The login credentials.

        Raises:
            serializers.ValidationError: If the credentials are invalid.

        Returns:
            User: The authenticated user instance.
        """
        user = authenticate(**attrs)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        return user


class AppointmentReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for appointment reminders.

    This serializer handles the validation and serialization of appointment
    details required for sending reminders to patients.
    """

    class Meta:
        model = Appointment
        fields = ['id', 'appointment_time', 'patient']

    def validate(self, attrs):
        """
        Validate the appointment data.

        Ensures that the appointment time is in the future.

        Args:
            attrs (dict): The incoming appointment data.

        Raises:
            serializers.ValidationError: If the appointment time is not in the future.
        
        Returns:
            dict: The validated appointment data.
        """
        if attrs['appointment_time'] <= timezone.now():
            raise serializers.ValidationError("Appointment time must be in the future.")
        
        return attrs
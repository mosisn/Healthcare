from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException

from .models import Doctor, Patient, Appointment, MedicalRecord
from .permissions import IsAdminOrReadOnly, IsDoctorOrReadOnly, IsPatientOrReadOnly
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, MedicalRecordSerializer, RegisterSerializer, LoginSerializer, AppointmentReminderSerializer
from .utils import send_email_reminder  

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view handles the creation of a new user account. Upon successful registration,
    a token is generated for the user to facilitate authentication in subsequent requests.
    """
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    API view for user login.

    This view authenticates a user and retrieves an authentication token that can be used
    for subsequent requests. The token is returned in the response upon successful login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating doctor profiles.

    Only admin users can create new doctor profiles. All users can view the list of doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific doctor profile.

    Only admin users can modify or delete doctor profiles. All users can view the doctor details.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]


class PatientListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating patient profiles.

    Patients can create their profiles and view the list of patients.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminOrReadOnly]


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific patient profile.

    Patients can modify their own profiles, while admin users can manage all patient profiles.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsPatientOrReadOnly, IsAdminOrReadOnly]


class DoctorAvailabilityView(generics.UpdateAPIView):
    """
    API view for doctors to manage their availability and appointment slots.

    Only authenticated doctors can update their availability information.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]


class PatientMedicalHistoryView(generics.RetrieveAPIView):
    """
    API view for patients to view their medical history.

    Only authenticated patients can access their own medical history.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOrReadOnly]


class AvailableDoctorsView(generics.ListCreateAPIView):
    """
    API view for patients to view available doctors and book appointments.

    Only authenticated patients can view the list of available doctors and create appointments.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorAppointmentScheduleView(generics.ListUpdateAPIView):
    """
    API view for doctors to view and manage their appointment schedule.

    Only authenticated doctors can view and update their appointment schedules.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]



class AppointmentReminderView(generics.CreateAPIView):
    """
    API view for sending appointment reminders via email.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentReminderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        appointment = serializer.save()
        try:
            send_email_reminder(appointment)
        except Exception as e:
            raise APIException(f"Failed to send email reminder: {str(e)}")

        return Response({"message": "Email reminder sent successfully."}, status=status.HTTP_201_CREATED)


class MedicalRecordListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating patient medical records.

    Only authenticated doctors can create medical records for patients.
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]


class MedicalRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting patient medical records.

    Only authenticated doctors can manage medical records.
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

class DoctorProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update a doctor's profile.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class PatientProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update a patient's profile.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

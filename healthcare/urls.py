from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    DoctorListCreateView,
    DoctorRetrieveUpdateDestroyView,
    PatientListCreateView,
    PatientRetrieveUpdateDestroyView,
    DoctorProfileView,
    PatientProfileView,
    AppointmentReminderView,
    MedicalRecordListCreateView,
    MedicalRecordRetrieveUpdateDestroyView,
    AvailableDoctorsView,
    DoctorAppointmentScheduleView,
    PatientMedicalHistoryView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('doctors/', DoctorListCreateView.as_view(), name='doctor_list_create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor_detail'),
    path('patients/', PatientListCreateView.as_view(), name='patient_list_create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient_detail'),
    path('doctors/<int:pk>/profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('patients/<int:pk>/profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('appointments/reminder/', AppointmentReminderView.as_view(), name='appointment_reminder'),
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_record_list_create'),
    path('medical-records/<int:pk>/', MedicalRecordRetrieveUpdateDestroyView.as_view(), name='medical_record_detail'),
    path('available-doctors/', AvailableDoctorsView.as_view(), name='available_doctors'),
    path('doctors/appointments/', DoctorAppointmentScheduleView.as_view(), name='doctor_appointment_schedule'),
    path('patients/medical-history/', PatientMedicalHistoryView.as_view(), name='patient_medical_history'),
]

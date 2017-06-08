from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='user:user_login')
def doctor_appointment(request, patient, doctor, caregiver):
    if request.user.user_type == 'CG':
        if patient_diagnosed_before(patient):
            doctor = get_appropriate_doctor(patient)
            if doctor is not None:
                create_appointment(patient,doctor,caregiver)
            else:
                doctor = find_free_doctor()
                create_appointment(patient,doctor,caregiver)
        else:
            doctor = find_free_doctor()
            create_appointment(patient, doctor, caregiver)
    else:
        return HttpResponse("<h1>Not authorized for this operation</h1>")


def patient_diagnosed_before(patient):
    patient_appointment_list = patient.patientappointment_set.all()
    if len(patient_appointment_list) > 0:
        return True
    return False


def get_appropriate_doctor(patient):
    patient_appointment_history_list = patient.patient_appointment.all()
    selected_doctor = None
    for appointment in patient_appointment_history_list:
        doctor = appointment.doctor
        if doctor.doctorappointment.appointments <= 10:
            selected_doctor = doctor
            return selected_doctor
    return selected_doctor


def find_free_doctor():
    doctor_list = DoctorAppointment.objects.filter(appointments__lte=10)
    return doctor_list[0]


def create_appointment(patient,doctor,care_giver):
    appointment = PatientAppointment(patient=patient,doctor=doctor,care_giver=care_giver)
    appointment.save()
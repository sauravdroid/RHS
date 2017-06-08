from .models import *

max_limit = 10


def doctor_appointment(patient, caregiver):
    if no_active_appointment(patient):
        if patient_diagnosed_before(patient):
            doctor = get_appropriate_doctor(patient)
            if doctor is not None:
                create_appointment(patient, doctor, caregiver)
            else:
                doctor = find_free_doctor()
                create_appointment(patient, doctor, caregiver)
        else:
            doctor = find_free_doctor()
            create_appointment(patient, doctor, caregiver)
        return True
    else:
        return False


def patient_diagnosed_before(patient):
    patient_appointment_list = patient.patient_appointment.all()
    if len(patient_appointment_list) > 0:
        return True
    return False


def no_active_appointment(patient):
    patient_appointment_list = patient.patient_appointment.all()
    for appointment in patient_appointment_list:
        if not appointment.appointment_status:
            return False
    return True


def get_appropriate_doctor(patient):
    patient_appointment_history_list = patient.patient_appointment.all()
    selected_doctor = None
    for appointment in patient_appointment_history_list:
        doctor = appointment.doctor
        if doctor.doctorappointment.appointments <= max_limit:
            selected_doctor = doctor
            return selected_doctor
    return selected_doctor


def find_free_doctor():
    doctor_list = DoctorAppointment.objects.filter(appointments__lte=max_limit)
    return doctor_list[0].doctor


def create_appointment(patient, doctor, care_giver):
    appointment = PatientAppointment(patient=patient, doctor=doctor, care_giver=care_giver)
    appointment_doctor = DoctorAppointment.objects.get(doctor=doctor)
    appointment_doctor.appointments += 1
    appointment_doctor.save()
    appointment.save()

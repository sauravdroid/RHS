from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Snippets)
admin.site.register(CustomUser)
admin.site.register(PatientDetail)
admin.site.register(PatientHistory)
admin.site.register(CurrentPatientStatus)
admin.site.register(PatientDiagnosis)
admin.site.register(PatientMedication)
admin.site.register(PatientMedicalStatus)
admin.site.register(PatientAppointment)
admin.site.register(DoctorAppointment)
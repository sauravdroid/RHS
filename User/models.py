from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, user_type, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, user_type, password=None):
        user = self.create_user(email=email, username=username, first_name=first_name, last_name=last_name,
                                user_type=user_type, password=password)
        user.is_admin = True
        user.save(using=self.db)
        return user


class CustomUser(AbstractBaseUser):
    user_types = (('CG', 'CG'), ('P', 'P'), ('DC', 'DC'))
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)
    user_type = models.CharField(max_length=50, choices=user_types)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name', 'user_type']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.username

    def get_email(self):
        return self.email

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Snippets(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    title = models.CharField(max_length=200)
    body = models.TextField()
    language = models.CharField(max_length=100)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class PatientDetail(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    uhid = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    occupation = models.CharField(max_length=255)
    address = models.TextField()
    locality = models.CharField(max_length=255)

    def __str__(self):
        return self.patient.get_full_name()


class PatientHistory(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    present_history = models.TextField(max_length=4096)
    past_history = models.TextField(max_length=4096)
    family_history = models.TextField(max_length=4096)
    menstural_obstetric_history = models.TextField(max_length=4096)
    immunization_history = models.TextField(max_length=4096)
    allergic_history = models.TextField(max_length=4096)
    socio_eco_status = models.TextField(max_length=255)


class CurrentPatientStatus(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    care_provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    insurance_status = models.CharField(max_length=9)
    insurance_id = models.CharField(max_length=25)
    organ_donor_status = models.BooleanField(default=False)
    episode_type = models.CharField(max_length=14)
    episode_number = models.IntegerField(max_length=4)
    encounter_type = models.CharField(max_length=14)
    encounter_no = models.IntegerField(max_length=4)
    encounter_date_time = models.DateTimeField()
    reason_for_visit = models.TextField(max_length=4096)
    visit_date = models.DateField(default=timezone.now())


class PatientMedicalStatus(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    care_provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    vitals_systolic_BP = models.IntegerField(max_length=3)
    vitals_diastolic_BP = models.IntegerField(max_length=3)
    pulse_rate = models.DecimalField(max_digits=4, decimal_places=2)
    temperature = models.IntegerField(max_length=3)
    temperature_source = models.CharField(max_length=6)
    respiration_rate = models.IntegerField(max_length=3)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    blood_group = models.CharField(max_length=3)
    clinical_exam_observation = models.TextField(max_length=4096)
    investigation_result = models.TextField(max_length=4096)
    date = models.DateField(default=timezone.now())


class PatientDiagnosis(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    diagnosis_type = models.CharField(max_length=11)
    diagnosis_code_name = models.CharField(max_length=500)
    diagnosis_code = models.CharField(max_length=500)
    diagnosis_description = models.TextField(max_length=4096)
    treatment_plan_investigations = models.TextField(max_length=4096)
    treatment_plan_medication = models.TextField(max_length=4096)
    treatment_plan_procedure = models.TextField(max_length=4096)
    treatment_plan_referral = models.TextField(max_length=4096)
    other_treatment_plan_type = models.TextField(max_length=10)
    other_treatment_plan_details = models.TextField(max_length=4096)
    current_clinical_status = models.TextField(max_length=255)
    date = models.DateTimeField(default=timezone.now())


class PatientMedication(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    medication_name = models.CharField(max_length=500)
    durg_code = models.CharField(max_length=500)
    strength = models.CharField(max_length=500)
    dose = models.CharField(max_length=500)
    route = models.CharField(max_length=500)
    frequency = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now())


class PatientAppointment(models.Model):
    patient = models.ForeignKey(CustomUser, related_name='patient_appointment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, related_name='doctor_appointment', on_delete=models.CASCADE)
    care_giver = models.ForeignKey(CustomUser, related_name='care_giver_appointment', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now())
    appointment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.get_full_name() + '-->' + self.doctor.get_full_name()


class DoctorAppointment(models.Model):
    doctor = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    appointments = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)

    def __str__(self):
        return self.doctor.get_full_name() + ' ' + str(self.appointments)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_doctor_appointment(sender, instance=None, created=False, **kwargs):
    if created:
        doctor_appointment = DoctorAppointment(doctor=instance)
        doctor_appointment.save()

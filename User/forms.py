from django import forms
from .models import *


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'user_type', 'password']


class AddPatientForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password']


class AddPatientDetailForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        exclude = ['patient']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))


class PatientHistoryForm(forms.ModelForm):
    class Meta:
        model = PatientHistory
        exclude = ['patient']


class CurrentPatientStatusForm(forms.ModelForm):
    class Meta:
        model = CurrentPatientStatus
        exclude = ['patient', 'care_provider', 'visit_date']


class PatientMedicalStatusForm(forms.ModelForm):
    class Meta:
        model = PatientMedicalStatus
        exclude = ['patient', 'care_provider', 'date']


class PatientDiagnosisForm(forms.ModelForm):
    class Meta:
        model = PatientDiagnosis
        exclude = ['patient', 'doctor', 'date']


class PatientMedicationForm(forms.ModelForm):
    class Meta:
        model = PatientMedication
        exclude = ['patient', 'doctor', 'date']

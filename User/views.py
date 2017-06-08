from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from .permissions import BlackListPermission
from .serializers import SnippetSerializer, CustomUserSerializer


# Create your views here.


class SnippetList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, BlackListPermission)

    def get(self, request, format=None):
        snippets = Snippets.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Snippets.objects.get(pk=pk)
        except Snippets.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        serializer = SnippetSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistration(APIView):
    @staticmethod
    def post(request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data['username']
            user = CustomUser.objects.get(username=username)
            token = Token.objects.get(user=user)
            return Response({'success': True, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"success": True, "token": token.key, "user_type": user.user_type},
                            status=status.HTTP_200_OK)
        else:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)


@login_required(login_url='user:user_login')
def user_registration(request):
    if check_superuser(request):
        if request.method == 'GET':
            form = UserRegistrationForm()
            return render(request, 'User/user-registration.html', {'form': form})
        elif request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                return HttpResponse("Successfully Registered")

        else:
            return HttpResponse("Request type not supported")
    return HttpResponse("Not permitted to view this page")


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('user:user_profile')
        form = LoginForm()
        return render(request, 'User/user-login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    url = request.GET.get('next')
                    return redirect('user:user_registration')
                else:
                    return redirect('user:user_profile')
            else:
                return HttpResponse("Wrong Username or password")


@login_required(login_url='user:user_login')
def user_profile(request):
    if request.method == 'GET':
        if request.user.user_type == 'CG':
            return render(request, 'User/Profile/caregiver-profile.html')
        elif request.user.user_type == 'DC':
            return render(request, 'User/Profile/doctor-profile.html')
        elif request.user.user_type == 'AD':
            return render(request, 'User/Profile/admin-profile.html')
    elif request.method == 'POST':
        if request.user.user_type == 'CG':
            try:
                patient = CustomUser.objects.get(username=request.POST.get('username'))
                if patient.user_type == 'P':
                    return render(request, 'User/Profile/caregiver-profile.html', {'patient': patient})
                else:
                    return render(request, 'User/Profile/caregiver-profile.html',
                                  {'error': 'No matching Patient Exist'})
            except CustomUser.DoesNotExist:
                return render(request, 'User/Profile/caregiver-profile.html', {'error': 'No matching Patient Exist'})


def user_logout(request):
    logout(request)
    return redirect('user:user_login')


@login_required(login_url='user:user_login')
def add_patient(request):
    if request.method == 'GET':
        form = AddPatientForm()
        return render(request, 'User/Profile/add-patient.html', {'form': form})
    elif request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user_type = 'P'
            patient.save()
            request.session['patient_username'] = form.cleaned_data['username']
            return redirect('user:add_patient_detail')
        else:
            return HttpResponse('Invalid Form')


@login_required(login_url='user:user_login')
def add_patient_detail(request):
    username = request.session.get('patient_username', None)
    if username is not None:
        if request.method == 'GET':
            form = AddPatientDetailForm()
            return render(request, 'User/Profile/add-patient-detail.html', {'form': form})
        elif request.method == 'POST':
            form = AddPatientDetailForm(request.POST)
            if form.is_valid():
                patient_form = form.save(commit=False)
                patient = CustomUser.objects.get(username=username)
                patient_form.patient = patient
                patient_form.save()
                return HttpResponse("Successfully Added Patient")
            else:
                return HttpResponse("Invalid Form")

    else:
        return HttpResponse("Please add a patient first")


@login_required(login_url='user:user_login')
def patient_profile(request, username):
    patient = CustomUser.objects.get(username=username)
    try:
        current_patient_status = patient.currentpatientstatus
    except CurrentPatientStatus.DoesNotExist:
        current_patient_status = None
    patient_medical_status_list = patient.patientmedicalstatus_set.all()
    if len(patient_medical_status_list) > 0:
        patient_medical_status = patient_medical_status_list[0]
    else:
        patient_medical_status = None
    patient_diagnosis_list = patient.patientdiagnosis_set.all()
    if len(patient_diagnosis_list) > 0:
        patient_diagnosis = patient_diagnosis_list[0]
    else:
        patient_diagnosis = None

    return render(request, 'User/Profile/patient-profile.html',
                  {'user': request.user, 'patient': patient, 'current_patient_status': current_patient_status,
                   'patient_medical_status': patient_medical_status,
                   'patient_diagnosis': patient_diagnosis})


@login_required(login_url='user:user_login')
def add_current_patient_status(request, username):
    if request.method == 'GET':
        form = CurrentPatientStatusForm()
        return render(request, 'User/Profile/add-patient-status.html', {'form': form, 'username': username})
    elif request.method == 'POST':
        patient = CustomUser.objects.get(username=username)
        form = CurrentPatientStatusForm(request.POST)
        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.patient = patient
            patient_form.care_provider = request.user
            patient_form.save()
            return HttpResponse("Done")
        else:
            return HttpResponse("Invalid Form")


@login_required(login_url='user:user_login')
def add_patient_medical_status(request, username):
    if request.method == 'GET':
        form = PatientMedicalStatusForm()
        return render(request, 'User/Profile/add-patient-status.html', {'form': form, 'username': username})
    elif request.method == 'POST':
        patient = CustomUser.objects.get(username=username)
        form = PatientMedicalStatusForm(request.POST)
        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.patient = patient
            patient_form.care_provider = request.user
            patient_form.save()
            return HttpResponse("Done")
        else:
            return HttpResponse("Invalid Form")


def check_superuser(req):
    superuser = False
    if req.user.is_authenticated and req.user.is_admin:
        superuser = True
    return superuser

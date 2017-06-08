from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'user'

urlpatterns = [
    url(r'^all/$', views.SnippetList.as_view(), name='snippet_list'),
    url(r'^snippet/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet_detail'),
    url(r'^register/$', views.user_registration, name='user_registration'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^add/patient/$', views.add_patient, name='add_patient'),
    url(r'^add/patient/detail/$', views.add_patient_detail, name='add_patient_detail'),
    url(r'^patient/(?P<username>[\w.@\-]+)/$', views.patient_profile, name='patient_profile'),
    url(r'^add/patient/current_status/(?P<username>[\w.@\-]+)/$', views.add_current_patient_status,
        name='add_patient_current_status'),
    url(r'^add/patient/medical_status/(?P<username>[\w.@\-]+)/$', views.add_patient_medical_status,
        name='add_patient_medical_status'),
    url(r'^add/patient/appointment/(?P<username>[\w.@\-]+)/$', views.appointment,
        name='appointment'),
]
urlpatterns = format_suffix_patterns(urlpatterns)

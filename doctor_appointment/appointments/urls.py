from django.contrib import admin
from django.urls import path

from appointments.views import *

urlpatterns = [
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('patients/', PatientList.as_view(), name='patient-list'),
    path('appointments/', AppointmentList.as_view(), name='patient-list'),
    path('appointments/<int:id>/', AppointmentDetail.as_view(), name='appointmentdetail-list')
]
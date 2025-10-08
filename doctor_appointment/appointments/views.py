from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from appointments.models import *
from appointments.serializers import *
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppointmentList(APIView):
    def get(self, request):
        appointment = Appointment.objects.all()
        serializers = AppointmentSerializer(appointment, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentDetail(APIView):
    def get(self, request, id):
        appointment = Appointment.objects.get(id=id)
        serializers = AppointmentSerializer(appointment)
        return Response(serializers.data)

    def put(self, request, id):
        appointment = Appointment.objects.get(id=id)
        serializers = AppointmentSerializer(appointment, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)

    def delete(self, request, id):
        appointment = Appointment.objects.get(id=id)
        appointment.delete()

        return Response(status=204)

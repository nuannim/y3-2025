from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from .models import *
from datetime import date
import datetime

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'date',
            'at_time',
            'details'
        ]

    def validate(self, value):
        # date = data.get('date')
        at_time = value.get('at_time')
        if value.get('date') < date.today():
            raise serializers.ValidationError("appointment date must be in the future")
        if value.get('date') == date.today() and at_time < datetime.datetime.now().time():
            raise serializers.ValidationError("appopopoeko[waefko time date must be in the future")
        return value


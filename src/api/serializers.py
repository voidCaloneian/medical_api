from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Patient.
    """
    class Meta:
        model = Patient
        fields = ['id', 'date_of_birth', 'diagnoses', 'created_at']
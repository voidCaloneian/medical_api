from django.db import models
from django.conf import settings


class Doctor(models.Model):
    """
    Модель для хранения информации о врачах
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Doctor: {self.user.username}'

class Patient(models.Model):
    """
    Модель для хранения информации о пациентах
    """
    id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField()
    diagnoses = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Patient {self.id}'

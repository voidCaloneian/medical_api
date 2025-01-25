from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Doctor, Patient
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **options):
        # Создаем тестового врача
        if User.objects.filter(username='test@doctor.com').exists():
            self.stdout.write(self.style.WARNING('Данные для тестов уже созданы'))
            return
        
        user = User.objects.create_user(
            username='test@doctor.com',
            email='test@doctor.com',
            password='test123'
        )
        doctor = Doctor.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS(f'Created doctor: {user.username}'))

        # Создаем тестовых пациентов
        test_patients = [
            {
                'date_of_birth': date(1990, 1, 15),
                'diagnoses': {
                    'primary': 'Гипертония',
                    'secondary': 'Диабет'
                }
            },
            {
                'date_of_birth': date(1985, 5, 20),
                'diagnoses': {
                    'primary': 'Астма',
                    'secondary': 'Бронхит'
                }
            },
            {
                'date_of_birth': date(1995, 12, 3),
                'diagnoses': {
                    'primary': 'Мигрень',
                    'secondary': 'Остеохондроз'
                }
            }
        ]

        for patient_data in test_patients:
            patient = Patient.objects.create(**patient_data)
            self.stdout.write(self.style.SUCCESS(f'Создан пациент: {patient.id} c диагнозами {patient.diagnoses}'))

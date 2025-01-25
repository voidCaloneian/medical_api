from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .models import Doctor, Patient

class MedicalAPITests(TestCase):
    """
    Тестовый класс для проверки API медицинской системы.
    Тестирует аутентификацию, авторизацию и работу с данными пациентов.
    """

    def setUp(self):
        """
        Подготовка тестовых данных:
        - Создание тестового клиента API
        - Создание тестового пользователя-врача
        - Создание тестового пациента
        """
        self.client = APIClient()
        self.doctor_user = User.objects.create_user(
            username='DoctorIvanLimarev@gmail.com',
            password='11pobeda11'
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user)
        self.patient = Patient.objects.create(
            date_of_birth='2000-01-01',
            diagnoses=['Гипертрофия мышц'],
            created_at='2025-01-01',  # Будущая дата для тестовых целей
        )

    def get_tokens_for_user(self, user):
        """
        Генерация JWT токенов для пользователя.
        
        Args:
            user: Экземпляр пользователя для генерации токенов
            
        Returns:
            dict: Словарь, содержащий refresh и access токены
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_login(self):
        """Проверка успешного входа с валидными учетными данными врача."""
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'DoctorIvanLimarev@gmail.com',
            'password': '11pobeda11'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_get_patients_authorized(self):
        """Проверка получения списка пациентов авторизованным врачом."""
        tokens = self.get_tokens_for_user(self.doctor_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])
        url = reverse('patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_patients_unauthorized(self):
        """Проверка запрета доступа к списку пациентов без авторизации."""
        url = reverse('patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        
    def test_get_patients_as_non_doctor(self):
        """Проверка запрета доступа к списку пациентов для не-врача."""
        regular_user = User.objects.create_user(
            username='regularUser@gmail.com',
            password='444nepremennobudetzanami444'
        )
        tokens = self.get_tokens_for_user(regular_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])
        url = reverse('patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Доступ запрещен')

    def test_patient_serialization(self):
        """Проверка корректности сериализации данных пациента."""
        tokens = self.get_tokens_for_user(self.doctor_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])
        url = reverse('patients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        patient_data = response.data[0]
        # Проверка соответствия полей пациента
        self.assertEqual(patient_data['id'], self.patient.id)
        self.assertEqual(patient_data['date_of_birth'], '2000-01-01')
        self.assertEqual(patient_data['diagnoses'], ['Гипертрофия мышц'])

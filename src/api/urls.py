from django.urls import path
from .views import LoginView, PatientListView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Путь для аутентификации
    path('patients/', PatientListView.as_view(), name='patients'),  # Путь для получения списка пациентов
]

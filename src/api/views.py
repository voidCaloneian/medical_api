from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Patient
from .serializers import PatientSerializer


class LoginView(TokenObtainPairView):
    pass  # Используем стандартное представление SimpleJWT

class PatientListView(APIView):
    """
    Представление для получения списка пациентов.
    Доступ разрешен только аутентифицированным пользователям с ролью врача.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Получение списка пациентов.
        """
        if hasattr(request.user, 'doctor'):  # Является ли пользователь врачом
            patients = Patient.objects.all()
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data)
        else:  # Пользователь не врач
            return Response({'detail': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

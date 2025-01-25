from django.urls import path, include


urlpatterns = [
    path('api/', include('api.urls')),  #  Подключение URL-ов приложения api
]

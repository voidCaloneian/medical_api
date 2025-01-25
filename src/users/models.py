from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Меняем модель пользователя на свою кастомную, так как
    юзернейм встроенной модели нам не нужен, используем email
    """
    username = models.EmailField('Email', unique=True, null=False, blank=False)
    email = models.EmailField('Email address', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели пользователя с email в качестве уникального идентификатора.
    """

    def create_user(self, email, first_name, last_name, password=None):
        """
        Создание обычного пользователя.
        """
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Создание суперпользователя.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Пользовательская модель пользователя, использующая email вместо username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

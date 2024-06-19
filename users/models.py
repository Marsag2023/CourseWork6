from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите адрес электронной почты')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE,
                               help_text='Загрузите свой аватар')
    phone = PhoneNumberField(verbose_name='Телефон', help_text='Введите номер телефона', **NULLABLE)
    tg_name = models.CharField(max_length=50, verbose_name='Имя в Telegram',
                               **NULLABLE, help_text='Введите имя в Telegram')
    country = CountryField(verbose_name='Страна', **NULLABLE, help_text='Выберите страну')

    token = models.CharField(max_length=50, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'change_status', 'Can change user status'
            )
        ]

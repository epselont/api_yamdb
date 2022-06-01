from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель пользователя с выбором его роли.'''
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True,
    )

    @property
    def is_moderator(self):
        '''Пользователь в статусе модератора'''
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        '''Пользователь в статусе администратора'''
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

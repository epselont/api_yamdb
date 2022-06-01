from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Адрес категории',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )
    year = models.IntegerField('Год создания')
    description = models.TextField('Описание')

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        'Адрес жанра',
        unique=True
    )

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name='genre',
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория'
    )

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=100)


def validate_even(value):
    if value not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        raise ValidationError(
            (f'Оценка должна быть от 1 до 10. Ваша {value}'),
            params={'value': value},
        )


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(default=1, validators=[validate_even])
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']


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


class Titles(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200
    )
    year = models.IntegerField('Год создания', null=True)
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genres, through='Genre_title')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Категория',
    )

    def __str__(self):
        return f'{self.title.name} {self.genre.name}'

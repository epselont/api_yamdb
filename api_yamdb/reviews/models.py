from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_even(value):
    if value not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        raise ValidationError(
            (f'Оценка должна быть от 1 до 10. Ваша {value}'),
            params={'value': value},
        )


class User(AbstractUser):
    """Модель пользователя с выбором его роли."""
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
        """Пользователь в статусе модератора."""
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Пользователь в статусе администратора."""
        return self.role == self.ADMIN

    # Свойство сообщает какое поле используется для входа в систему.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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


class Title(models.Model):
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
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                       name='unique review')]


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


class Genre_title(models.Model):
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Категория',
    )

    def __str__(self):
        return f'{self.title.name} {self.genre.name}'

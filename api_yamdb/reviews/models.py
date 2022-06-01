from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError


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

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    # title = models.ForeignKey(
    #     'Titles',
    #     on_delete=models.CASCADE,
    #     related_name='titles',
    #     verbose_name='Произведение',
    # )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор отзыва',
    )


class Comments(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

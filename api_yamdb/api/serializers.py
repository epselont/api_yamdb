from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import (Categories, Comment, Genre_title, Genres, Review,
                            Titles)

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre_title
        fields = ('__all__')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)

    class Meta:
        model = Titles
        fields = ('__all__')

    def validate_year(self, value):
        year = datetime.now().year
        if not (value > year):
            raise serializers.ValidationError(
                'Это произведение не опубликованно, проверьте дату!'
            )
        return value

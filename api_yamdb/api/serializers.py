from reviews.models import Categories, Genres, Genre_title, Titles
from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('__all__')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('__all__')


class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre_title
        fields = ('__all__')


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = ('__all__')

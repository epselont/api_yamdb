from reviews.models import Categories, Genres, Genre_title, Titles
from rest_framework import serializers
from datetime import datetime
# from rest_framework.validators import UniqueTogetherValidator


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

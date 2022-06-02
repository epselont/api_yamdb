from django.shortcuts import get_object_or_404
from reviews.models import Categories, Genres, Genre_title, Titles
from rest_framework import viewsets
from .serializers import CategoriesSerializer, GenresSerializer, GenreTitleSerializer, TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class GenreTitleViewSet(viewsets.ModelViewSet):
    queryset = Genre_title.objects.all()
    serializer_class = GenreTitleSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

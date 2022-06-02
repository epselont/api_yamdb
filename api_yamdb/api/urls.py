from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, GenreTitleViewSet, TitlesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

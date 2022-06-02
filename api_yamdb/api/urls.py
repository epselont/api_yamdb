from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, GenreTitleViewSet, TitlesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genre', GenresViewSet)
router.register('title', TitlesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

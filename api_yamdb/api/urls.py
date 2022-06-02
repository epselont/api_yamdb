from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet, get_token,
                    registration)

router = DefaultRouter()

router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    views.CommentViewSet, basename='comment')
router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    views.ReviewViewSet, basename='review')
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token')
]

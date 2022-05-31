from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    views.CommentViewSet, basename='comment')

router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    views.ReviewViewSet, basename='review')

app_name = 'api'


urlpatterns = [
    path('v1/', include(router.urls)),
]

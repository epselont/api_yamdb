from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import registration, get_token, UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet,)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token')
]

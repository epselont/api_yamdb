from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Права администратора на управление всем контентом проекта."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """Права администратора, модератора, автора на управление контентом."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        """Права на изменение контента администратором, модераторм, автором."""
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

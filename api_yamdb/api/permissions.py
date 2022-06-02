from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOnly(BasePermission):
    """Права администратора на управление всем контентом проекта."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Права администратора и права чтения всеми пользователями."""

    message = 'Требуются права администратора.'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """Права на изменение контента администратором,
    модератором, автором и права чтения всеми пользователями."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    message = 'Изменение доступно автору, модератору или администратору.'

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

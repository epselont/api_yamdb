from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied


class OnlyAuthor:
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет доступа на удаление/изменение этого ресурса.")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет доступа на удаление/изменение этого ресурса.")
        instance.delete()


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass

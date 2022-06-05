from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import (Categories, Genres, Review, Titles,
                            User)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from .filters import TitleFilter
from .mixins import OnlyAuthor
from .permissions import IsAdminOnly, IsAdminOrReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, GenreTitleSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitlesSerializer, TitlesCreateSerializer, TokenSerializer,
                          UserEditSerializer, UsersSerializer)


class CatGenMixin(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass


class ReviewViewSet(OnlyAuthor, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        titles = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        reviews = titles.reviews.all()
        return reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get("title_id"))


class CommentViewSet(OnlyAuthor, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review, pk=self.kwargs.get("review_id"), title=title)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get("title_id"),
            review_id=self.kwargs.get("review_id")
        )


class CategoriesViewSet(CatGenMixin):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CatGenMixin):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter
    filterset_fields = ('category', 'name', 'genre', 'year')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    ordering_fields = ('genre',)
    ordering = ('slug',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlesCreateSerializer
        return TitlesSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Регистрация нового пользователя."""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb',
        message=f'Ваш код: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Получение JWT-токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOnly,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def user_profile(self, request):
        """Получение и редактирование пользователем своих данных."""
        user = request.user
        if request.method == "GET":
            serializer = UserEditSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserEditSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

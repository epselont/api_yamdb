from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from reviews.models import Title, Review, Comment
from .mixins import OnlyAuthor
from .serializers import ReviewSerializer, CommentSerializer

User = get_user_model()


class ReviewViewSet(OnlyAuthor, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        titles = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        reviews = titles.reviews.all()
        return reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get("title_id"))


class CommentViewSet(OnlyAuthor, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        titles = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        comments = titles.reviews.comments.all()
        return comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get("title_id"),
            review_id=self.kwargs.get("review_id")
        )

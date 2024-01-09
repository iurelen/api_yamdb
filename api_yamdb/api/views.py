import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (AdminSuperuserChangeOrAnyReadOnly,
                          OwnerModeratorChange)
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitlePostSerializer,
                          TitleGetSerializer)

User = get_user_model()


class NoPutMethodMixin:
    """Mixin for disabling the HTTP PUT Method."""

    def update(self, request, *args, **kwargs):
        logging.warning(f"""
            perm: {self.get_permissions()[0].has_permission(request, self)}
            obj: {self.get_permissions()[0].has_object_permission(request, self, self.get_object())}
        """)
        if not kwargs.get('partial', False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class GenreAndCategoryModelViewSet(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   mixins.ListModelMixin,
                                   GenericViewSet,):
    """
    A viewset for Genre and Category ViewSets.

    Added `create()`,`destroy()` and `list()` actions.
    Adding `lookup_field` for slug fild,
    search for name field and permissions.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (AdminSuperuserChangeOrAnyReadOnly,)


class CategoryViewSet(GenreAndCategoryModelViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer


class CommentViewSet(NoPutMethodMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-pub_date')
    serializer_class = CommentSerializer
    permission_classes = (OwnerModeratorChange,)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return super().get_queryset().filter(review=review_id)

    def perform_create(self, serializer):
        user = self.request.user
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(review=review, author=user)


class GenreViewSet(GenreAndCategoryModelViewSet):
    queryset = Genre.objects.order_by('name')
    serializer_class = GenreSerializer


class ReviewViewSet(NoPutMethodMixin, viewsets.ModelViewSet):
    queryset = Review.objects.order_by('-pub_date')
    serializer_class = ReviewSerializer
    permission_classes = (OwnerModeratorChange,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return super().get_queryset().filter(title=title_id)

    def perform_create(self, serializer):
        user = self.request.user
        score = self._check_score(self.request)
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title, author=user, score=score)

    def _check_score(self, request):
        """Check that the score is between 1 and MAX_SCORE or None."""
        message_error = (f'Invalid score value. Score must be an '
                         f'integer between 0 and {settings.MAX_SCORE}')
        score = request.data.get('score', None)
        try:
            if not score or int(score) in range(1, settings.MAX_SCORE + 1):
                return score
            raise ValueError
        except ValueError:
            raise ValidationError(message_error)


class TitleViewSet(NoPutMethodMixin, viewsets.ModelViewSet):
    queryset = Title.objects.order_by('name')
    serializer_class = TitlePostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminSuperuserChangeOrAnyReadOnly,)

    def get_serializer_class(self, *args, **kwargs):
        """Turn serializer class for safe methods."""
        if self.request.method in SAFE_METHODS:
            return TitleGetSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Title.objects.order_by('name').annotate(
            rating=Avg('review__score')
        )
        return queryset
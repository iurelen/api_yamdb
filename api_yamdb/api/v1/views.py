from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Review, Title

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
    serializer_class = CommentSerializer
    permission_classes = (OwnerModeratorChange,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.order_by('-pub_date')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(review=review, author=self.request.user)


class GenreViewSet(GenreAndCategoryModelViewSet):
    queryset = Genre.objects.order_by('name')
    serializer_class = GenreSerializer


class ReviewViewSet(NoPutMethodMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerModeratorChange,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id).order_by('-pub_date')

    def perform_create(self, serializer):
        user = self.request.user
        score = self.request.data.get('score')
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title, author=user, score=score)


class TitleViewSet(NoPutMethodMixin, viewsets.ModelViewSet):
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

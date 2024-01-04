from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.exceptions import ParseError
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
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-pub_date')
    serializer_class = CommentSerializer
    permission_classes = (
        (OwnerModeratorChange | AdminSuperuserChangeOrAnyReadOnly),)
    # permission_classes = (AllowAny,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return super().get_queryset().filter(review=review_id)

    def create(self, request, *args, **kwargs):
        user = request.user
        review = get_object_or_404(Review, pk=kwargs.get('review_id'))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review=review, author=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class GenreViewSet(GenreAndCategoryModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-pub_date')
    serializer_class = ReviewSerializer
    permission_classes = (
        (OwnerModeratorChange | AdminSuperuserChangeOrAnyReadOnly),
    )

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return super().get_queryset().filter(title=title_id)

    def create(self, request, *args, **kwargs):
        score = self._check_score(request)
        user = request.user
        title = get_object_or_404(Title, pk=kwargs.get('title_id'))

        if not self.get_queryset().filter(title=title, author=user).exists():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(title=title, author=user, score=score)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            message_error = serializer.errors
        else:
            message_error = "Already have a review from you"
        return Response(
            data=message_error,
            status=status.HTTP_400_BAD_REQUEST
        )

    def _check_score(self, request):
        message_error = f'Invalid score value. Score must be an ' \
                        f'integer between 0 and {settings.MAX_SCORE}'
        score = request.data.get('score', None)
        try:
            if not score or int(score) in range(1, settings.MAX_SCORE + 1):
                return score
            raise ValueError(message_error)
        except ValueError:
            raise ParseError(message_error)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitlePostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminSuperuserChangeOrAnyReadOnly,)

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return TitleGetSerializer
        return self.serializer_class

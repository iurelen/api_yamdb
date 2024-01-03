from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Comment, Genre, Review, Title

from .permissions import (CustomPermissions,
                          AdminSuperuserChangeOrAnyReadOnly)
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleSerializer)

class GenreAndCategoryModelViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet,):
    """
    A viewset that provides default `create()`, `destroy()` and `list()` actions.
    Adding `lookup_field` for slug fild, searh for name field and permissions.
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (AdminSuperuserChangeOrAnyReadOnly,)


class CategoryViewSet(GenreAndCategoryModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CustomPermissions,)


class GenreViewSet(GenreAndCategoryModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (CustomPermissions,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(title=kwargs.get('title_id'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        title = Title.objects.get(pk=kwargs.get('title_id'))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(title=title, author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (AdminSuperuserChangeOrAnyReadOnly,)
    # permission_classes = (AllowAny,)

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TitleSerializerMetaMixin:

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('rating',)


class ValidateSlugMixin:
    """Slug validation mixin."""

    def validate_slug(self, value):
        if not value.isidentifier():
            raise serializers.ValidationError()
        return value


class CategorySerializer(serializers.ModelSerializer,
                         ValidateSlugMixin):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer,
                      ValidateSlugMixin):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    score = serializers.IntegerField(
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'author', 'pub_date', 'title')


class TitlePostSerializer(serializers.ModelSerializer,
                          TitleSerializerMetaMixin):
    """TitleSerializer for NO Safe methods."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'The name field must not exceed 256 characters.'
            )
        return value


class TitleGetSerializer(serializers.ModelSerializer,
                         TitleSerializerMetaMixin):
    """TitleSerializer for Safe methods."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True
    )
    rating = serializers.IntegerField()

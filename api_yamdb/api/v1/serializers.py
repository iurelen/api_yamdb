from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TitleSerializerMetaMixin:

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('rating',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'author', 'pub_date', 'review')


class GenreSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        author = validated_data.get('author')
        title = validated_data.get('title')
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Already have the review from you')

        return super().create(validated_data)

    def validate_score(self, value):
        """Check that the score is between 1 and MAX_SCORE or None."""
        if 1 < value < settings.MAX_SCORE + 1:
            return value
        raise serializers.ValidationError(
            'Invalid score value. Score must be an '
            f'integer between 0 and {settings.MAX_SCORE}'
        )


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

    def validate_year(self, value):
        current_year = timezone.now().year

        if value > current_year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего года.'
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

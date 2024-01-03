from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class ValidateSlugMixin:
    """Slug valudation mixin."""
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
    author = serializers.StringRelatedField(),
    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'author', 'pub_date', 'title')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(
        default=None
    )
    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category'
        )
        model = Title

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        category_data = validated_data.pop('category')

        title = Title.objects.create(**validated_data)

        title.genre.set(Genre.objects.filter(slug__in=genre_data))
        title.category = Category.objects.get(slug=category_data)
        title.save()

        return title

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError('The name field must not exceed 256 characters.')
        return value
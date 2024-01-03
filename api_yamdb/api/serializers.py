from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def validate_slug(self, value):
        if not value.isidentifier():
            return serializers.ValidationError()
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(),
    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'author', 'pub_date', 'title')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

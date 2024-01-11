from django.contrib import admin
from django.db.models import Avg

from .models import Category, Genre, Review, Title, Comment, GenreTitle

@admin.register(Category, Genre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreInline(admin.TabularInline):
    model = GenreTitle
    extra = 1

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'rating',
                    'description',
                    'year',
                    'category',
                    'display_genres')
    list_editable = ('category',)

    @admin.display(description='Жанры')
    def display_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())
    inlines = (GenreInline,)

    @admin.display(description='Рейтинг')
    def rating(self, obj):
        rating = Review.objects.filter(
            title=obj
        ).aggregate(rating=Avg('score'))['rating']
        if rating:
            rating = "{:.2f}".format(rating)
        return rating

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'score', 'author', 'pub_date',)

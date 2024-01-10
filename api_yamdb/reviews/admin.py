from django.contrib import admin
from django.db.models import Avg

from .models import Category, Genre, Review, Title, Comment, GenreTitle


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'rating',
                    'description',
                    'year',
                    'category',
                    'display_genres')

    def display_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())
    inlines = (GenreInline,)

    def rating(self, obj):
        rating = Review.objects.filter(
            title=obj
        ).aggregate(rating=Avg('score'))['rating']
        if rating:
            rating = "{:.2f}".format(rating)
        return rating

    display_genres.short_description = 'Жанры'
    rating.short_description = 'Рейтинг'

    list_editable = ('category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'score', 'author', 'pub_date',)


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)

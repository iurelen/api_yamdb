from django.contrib import admin

from .models import CustomUser
from reviews.models import Comment, Review


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'amount_review',
                    'amount_comments',
                    'role',)

    def amount_review(self, obj):
        return Review.objects.filter(author=obj).count()

    def amount_comments(self, obj):
        return Comment.objects.filter(author=obj).count()

    amount_review.short_description = 'Всего обзоров'
    amount_comments.short_description = 'Всего комментариев'

    list_editable = ('role',)


admin.site.register(CustomUser, UserAdmin)

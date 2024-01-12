from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser
from reviews.models import Comment, Review


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'amount_review',
                    'amount_comments',
                    'role',)
    list_editable = ('role',)

    @admin.display(description='Всего обзоров')
    def amount_review(self, obj):
        return Review.objects.filter(author=obj).count()

    @admin.display(description='Всего комментариев')
    def amount_comments(self, obj):
        return Comment.objects.filter(author=obj).count()


admin.site.unregister(Group)

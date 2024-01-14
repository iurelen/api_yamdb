from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'amount_review',
                    'amount_comments',
                    'role',
                    'is_superuser',)
    list_editable = ('role',)

    @admin.display(description='Всего обзоров')
    def amount_review(self, obj):
        return obj.reviews.count()

    @admin.display(description='Всего комментариев')
    def amount_comments(self, obj):
        return obj.comments.count()


admin.site.unregister(Group)

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Почта', unique=True, max_length=254)
    username = models.SlugField('Логин', unique=True, max_length=150)
    role = models.CharField(
        'Пользовательская роль',
        max_length=32,
        choices=Role.choices,
        default=Role.USER
    )
    bio = models.TextField('О себе')
    confirmation_code = models.IntegerField('Код подтверждения', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email',),
                name='unique_pair_username_email'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'
        default_related_name = 'author'

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class CustomUser(AbstractUser):
    role = models.CharField(
        'Пользовательская роль',
        max_length=32,
        choices=ROLE_CHOICE,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    confirmation_code = models.IntegerField('Код подтверждения', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_pair_username_email'
            )
        ]

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICE = (
    ('admin', 'Admin'),
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('superuser', 'Superuser'),
)


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=32,
        choices=ROLE_CHOICE,
    )
    bio = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.username

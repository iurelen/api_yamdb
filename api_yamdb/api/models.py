from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=64)

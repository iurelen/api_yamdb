from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AddNameStrMixin(models.Model):
    """Added field name and magic method __str__."""

    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class AddNameStrSlugMixin(AddNameStrMixin):
    """Added field slug."""

    slug = models.CharField(
        max_length=64,
        unique=True
    )

    class Meta:
        abstract = True


class DefaultFieldMixin(models.Model):
    """Added fields test,author, pub_date."""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.TimeField(
        auto_created=True,
    )

    class Meta:
        abstract = True


class Category(AddNameStrSlugMixin):
    class Meta:
        verbose_name = 'category'


class Genre(AddNameStrSlugMixin):

    class Meta:
        verbose_name = 'genre'


class Title(AddNameStrMixin):
    year = models.PositiveIntegerField()
    description = models.TextField()
    categories = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING
    )
    genre = models.ManyToManyField(
        Genre,
    )
    rating = models.IntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'title'


class Review(DefaultFieldMixin):
    score = models.PositiveIntegerField(
        default=0,

    )

    class Meta:
        verbose_name = 'review'


class Comment(DefaultFieldMixin):

    class Meta:
        verbose_name = 'comments'

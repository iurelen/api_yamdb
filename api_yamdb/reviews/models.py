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
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.slug}'


class DefaultFieldMixin(models.Model):
    """Added fields test,author, pub_date."""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
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
    description = models.TextField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    rating = models.IntegerField(
        default=0,
        null=True
    )

    class Meta:
        verbose_name = 'title'


class Review(DefaultFieldMixin):
    score = models.PositiveIntegerField(
        default=0,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'review'


class Comment(DefaultFieldMixin):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'comments'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

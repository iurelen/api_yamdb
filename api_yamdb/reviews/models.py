from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint, Avg

User = get_user_model()


class AddNameStrMixin(models.Model):
    """Added field name and magic method __str__."""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_LENGTH_FOR_NAME,

    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class AddNameStrSlugMixin(AddNameStrMixin):
    """Added field slug."""

    slug = models.CharField(
        'Идентификатор',
        max_length=settings.MAX_LENGTH_FOR_SLUG,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.slug}'


class DefaultFieldMixin(models.Model):
    """Added fields test,author, pub_date."""

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(AddNameStrSlugMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        default_related_name = 'category'


class Genre(AddNameStrSlugMixin):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'
        default_related_name = 'genre'


class Review(DefaultFieldMixin):
    score = models.PositiveIntegerField(
        'Оценка',
        default=0,
        null=True,
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            UniqueConstraint(fields=('author', 'title'),
                             name='author_title_unique'),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'review'


class Title(AddNameStrMixin):
    year = models.PositiveIntegerField('Год выхода')
    description = models.TextField(
        'Описание',
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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'
        default_related_name = 'title'

    @property
    def rating(self):
        rating = Review.objects.filter(title=self).aggregate(
            avg_value=Avg('score')
        )
        return rating.get('avg_value', None)


class Comment(DefaultFieldMixin):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

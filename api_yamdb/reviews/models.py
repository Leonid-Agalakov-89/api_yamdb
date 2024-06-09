from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (LENGTH_OF_CATEGORY_NAME,
                               LENGTH_OF_CATEGORY_SLUG,
                               LENGTH_OF_TITLE_NAME)
from reviews.validators import validate_year


User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    name = models.CharField(
        unique=True,
        max_length=LENGTH_OF_CATEGORY_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=LENGTH_OF_CATEGORY_SLUG,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'категории'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'жанры'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        max_length=LENGTH_OF_TITLE_NAME,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            validate_year
        ],
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'произведения'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class ReviewCommentBaseModel(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Напишите, что-нибудь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        abstract = True


class Review(ReviewCommentBaseModel):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name="Оценка",
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'title',
                    'author',
                ),
                name='unique_review',
            )
        ]

    def __str__(self):
        return f'{self.title}, {self.author}'


class Comment(ReviewCommentBaseModel):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

from django.db import models

from lazychoices import LazyChoiceField, LazyChoiceModelMixin


class Book(LazyChoiceModelMixin, models.Model):
    CATEGORY_CHOICES = [('fiction', 'Fiction'), ('non-fiction', 'Non-Fiction'), ('other', 'Other')]
    GENRE_CHOICES = [
        ('Fiction', [('crime', 'Crime'), ('horror', 'Horror')]),
        ('Non-Fiction', [('biography', 'Biography'), ('reference', 'Reference')]),
    ]

    title = models.CharField(max_length=50)
    category = LazyChoiceField(null=False)
    genre = LazyChoiceField(null=True)


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

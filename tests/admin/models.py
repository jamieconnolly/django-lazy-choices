from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from lazy_choices import LazyChoiceField, LazyChoiceModelMixin


@python_2_unicode_compatible
class Book(LazyChoiceModelMixin, models.Model):
    CATEGORY_CHOICES = [('fiction', 'Fiction'), ('non-fiction', 'Non-Fiction'), ('other', 'Other')]
    GENRE_CHOICES = [
        ('Fiction', [('crime', 'Crime'), ('horror', 'Horror')]),
        ('Non-Fiction', [('biography', 'Biography'), ('reference', 'Reference')]),
    ]

    title = models.CharField(max_length=50)
    category = LazyChoiceField(null=False)
    genre = LazyChoiceField(null=True)

    def __str__(self):
        return self.get_genre_display()

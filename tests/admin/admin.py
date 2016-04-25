from django.contrib.admin import ModelAdmin

from lazychoices.admin import LazyChoicesFieldListFilter


class BookAdmin(ModelAdmin):
    list_filter = [
        ('category', LazyChoicesFieldListFilter),
        ('genre', LazyChoicesFieldListFilter),
    ]
    ordering = ['-id']

from django.contrib.admin import ModelAdmin

from lazy_choices.admin import LazyChoicesFieldListFilter


class BookAdmin(ModelAdmin):
    list_filter = [
        ('category', LazyChoicesFieldListFilter),
        ('genre', LazyChoicesFieldListFilter)
    ]
    ordering = ['-id']

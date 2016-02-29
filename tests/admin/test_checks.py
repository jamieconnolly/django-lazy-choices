from django.contrib import admin
from django.core import checks
from django.test import TestCase

from lazychoices.admin import LazyChoiceInlineModelAdminMixin

from .models import Book, Chapter


class LazyChoiceInlineModelAdminChecksTests(TestCase):
    def test_lazy_model(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, admin.options.InlineModelAdmin):
            lazy_model = Book
            model = Chapter

        errors = InlineModelAdmin(Book, admin.site).check()
        self.assertEqual(errors, [])

    def test_missing_lazy_model(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, admin.options.InlineModelAdmin):
            model = Chapter

        errors = InlineModelAdmin(Book, admin.site).check()
        expected = [
            checks.Error(
                "'tests.admin.test_checks.InlineModelAdmin' must have a 'lazy_model' attribute.",
                hint=None,
                obj=InlineModelAdmin,
                id='lazychoices.E101',
            )
        ]
        self.assertEqual(errors, expected)

    def test_invalid_lazy_model(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, admin.options.InlineModelAdmin):
            lazy_model = Chapter
            model = Chapter

        errors = InlineModelAdmin(Book, admin.site).check()
        expected = [
            checks.Error(
                "The value of 'lazy_model' must inherit from 'LazyChoiceModelMixin'.",
                hint=None,
                obj=InlineModelAdmin,
                id='lazychoices.E102',
            )
        ]
        self.assertEqual(errors, expected)

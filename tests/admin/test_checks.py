from django.contrib.admin.options import InlineModelAdmin as BaseInlineModelAdmin
from django.core import checks
from django.test import TestCase

from lazychoices.admin import LazyChoiceInlineModelAdminMixin

from ..compat import run_model_admin_check
from .models import Book, Chapter


class LazyChoiceInlineModelAdminChecksTests(TestCase):
    def test_lazy_model(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, BaseInlineModelAdmin):
            lazy_model = Book
            model = Chapter

        errors = run_model_admin_check(InlineModelAdmin, Book)
        self.assertEqual(errors, [])

    def test_missing_lazy_model(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, BaseInlineModelAdmin):
            model = Chapter

        errors = run_model_admin_check(InlineModelAdmin, Book)
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
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, BaseInlineModelAdmin):
            lazy_model = Chapter
            model = Chapter

        errors = run_model_admin_check(InlineModelAdmin, Book)
        expected = [
            checks.Error(
                "The value of 'lazy_model' must inherit from 'LazyChoiceModelMixin'.",
                hint=None,
                obj=InlineModelAdmin,
                id='lazychoices.E102',
            )
        ]
        self.assertEqual(errors, expected)

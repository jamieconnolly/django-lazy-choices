from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from lazychoices.admin import LazyChoiceInlineModelAdminMixin

from .models import Book, Chapter


class LazyChoiceInlineModelAdminMixinTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_formset(self):
        class InlineModelAdmin(LazyChoiceInlineModelAdminMixin, admin.options.InlineModelAdmin):
            lazy_model = Book
            model = Chapter

        inline = InlineModelAdmin(Book, admin.site)
        request = self.request_factory.get('/')
        request.user = User.objects.create_user('example', 'example@example.com', 'password')

        formset = inline.get_formset(request)
        self.assertEqual(formset.lazy_model, Book)

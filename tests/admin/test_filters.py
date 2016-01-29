from django.contrib.admin import site
from django.contrib.admin.views.main import ChangeList
from django.test import RequestFactory, TestCase
from django.utils.encoding import force_text

from .admin import BookAdmin
from .models import Book


class LazyChoicesFieldListFilterTests(TestCase):
    def setUp(self):
        self.modeladmin = BookAdmin(Book, site)
        self.request_factory = RequestFactory()

        self.crime_book1 = Book.objects.create(
            title='Hercule Poirot',
            category='fiction', genre='crime'
        )
        self.crime_book2 = Book.objects.create(
            title='Sherlock Holmes',
            category='fiction', genre='crime'
        )
        self.horror_book = Book.objects.create(
            title='The Shining',
            category='fiction', genre='horror'
        )
        self.biography_book = Book.objects.create(
            title='A Child Called It',
            category='non-fiction', genre='biography'
        )
        self.reference_book = Book.objects.create(
            title='Encyclopedia Britannica',
            category='non-fiction', genre='reference'
        )
        self.unwritten_book = Book.objects.create(
            title='The Unwritten Book',
            category='other', genre=None
        )

    def get_changelist(self, request, model, modeladmin):
        return ChangeList(
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
        )

    # test that all is shown (and is the default)
    def test_something_all(self):
        request = self.request_factory.get('/', {})
        changelist = self.get_changelist(request, Book, self.modeladmin)

        # Make sure the correct queryset is returned
        queryset = changelist.get_queryset(request)
        self.assertEqual(list(queryset), list(Book.objects.all().order_by('-id')))

        # Make sure the correct choice is selected
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'category')
        choices = list(filterspec.choices(changelist))
        self.assertEqual(len(choices), 4)

        self.assertEqual(choices[0]['display'], 'All')
        self.assertEqual(choices[0]['selected'], True)
        self.assertEqual(choices[0]['query_string'], '?')

    # test that None is shown
    def test_something_null(self):
        request = self.request_factory.get('/', {'genre__isnull': 'True'})
        changelist = self.get_changelist(request, Book, self.modeladmin)

        # Make sure the correct queryset is returned
        queryset = changelist.get_queryset(request)
        self.assertEqual(list(queryset), [self.unwritten_book])

        # Make sure the last choice is None and is selected
        filterspec = changelist.get_filters(request)[0][1]
        self.assertEqual(force_text(filterspec.title), 'genre')
        choices = list(filterspec.choices(changelist))
        self.assertEqual(len(choices), 6)

        self.assertEqual(choices[-1]['display'], '-')
        self.assertEqual(choices[-1]['selected'], True)
        self.assertEqual(choices[-1]['query_string'], '?genre__isnull=True')

    def test_something_exact(self):
        request = self.request_factory.get('/', {'genre__exact': 'crime'})
        changelist = self.get_changelist(request, Book, self.modeladmin)

        # Make sure the correct choice is selected
        filterspec = changelist.get_filters(request)[0][1]
        self.assertEqual(force_text(filterspec.title), 'genre')
        choices = list(filterspec.choices(changelist))
        self.assertEqual(choices[1]['display'], 'Crime')
        self.assertEqual(choices[1]['selected'], True)
        self.assertEqual(choices[1]['query_string'], '?genre__exact=crime')

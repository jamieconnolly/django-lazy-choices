from django.test import TestCase

from lazy_choices.utils import flatten_choices


class UtilTests(TestCase):
    def test_flatten_choices(self):
        choices1 = [('foo', 'Foo'), ('bar', 'Bar')]
        choices2 = [(1, [('foo', 'Foo')]), (2, [('bar', 'Bar')])]

        expected = [('foo', 'Foo'), ('bar', 'Bar')]
        self.assertEqual(flatten_choices(choices1), expected)
        self.assertEqual(flatten_choices(choices2), expected)

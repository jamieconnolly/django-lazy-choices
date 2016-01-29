from django.db import models

from lazy_choices.models import LazyChoiceField, LazyChoiceModelMixin

from ..base import IsolatedModelsTestCase


class LazyChoiceModelMixinTests(IsolatedModelsTestCase):
    def test_display(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [
                (1, [('foo', 'Foo')]),
                ('bar', 'Bar'),
            ]
            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        m1, m2 = Model(field='foo'), Model(field='bar')
        p1, p2 = Proxy(field='baz'), Proxy(field='qux')

        self.assertEqual(m1.get_field_display(), 'Foo')
        self.assertEqual(m2.get_field_display(), 'Bar')
        self.assertEqual(p1.get_field_display(), 'Baz')
        self.assertEqual(p2.get_field_display(), 'Qux')

        # If the value for the field doesn't correspond to a valid choice,
        # the value itself is provided as a display value.
        m1.field = p1.field = ''
        self.assertEqual(m1.get_field_display(), '')
        self.assertEqual(p1.get_field_display(), '')

        m1.field = p1.field = 'invalid'
        self.assertEqual(m1.get_field_display(), 'invalid')
        self.assertEqual(p1.get_field_display(), 'invalid')

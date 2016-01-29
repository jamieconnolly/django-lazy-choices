from django.db import models

from lazy_choices.db.models import LazyChoiceField, LazyChoiceModelMixin

from ... import IsolatedModelsTestCase


class LazyChoiceModelMixinTests(IsolatedModelsTestCase):
    def test_display(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        m1 = Model(field='foo')
        m2 = Model(field='bar')
        p1 = Proxy(field='baz')
        p2 = Proxy(field='qux')

        self.assertEqual(m1.field, 'foo')
        self.assertEqual(m2.field, 'bar')
        self.assertEqual(p1.field, 'baz')
        self.assertEqual(p2.field, 'qux')

        self.assertEqual(m1.get_field_display(), 'Foo')
        self.assertEqual(m2.get_field_display(), 'Bar')
        self.assertEqual(p1.get_field_display(), 'Baz')
        self.assertEqual(p2.get_field_display(), 'Qux')

        # If the value for the field doesn't correspond to a valid choice,
        # the value itself is provided as a display value.
        m1.field = ''
        p1.field = ''
        self.assertEqual(m1.get_field_display(), '')
        self.assertEqual(p1.get_field_display(), '')

        m1.field = 'invalid'
        p1.field = 'invalid'
        self.assertEqual(m1.get_field_display(), 'invalid')
        self.assertEqual(p1.get_field_display(), 'invalid')

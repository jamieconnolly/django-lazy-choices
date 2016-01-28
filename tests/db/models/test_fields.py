from django.core import checks, exceptions
from django.db import models

from lazy_choices.db.models import LazyChoiceField, LazyChoiceModelMixin

from . import IsolatedModelsTestCase


class LazyChoiceFieldTests(IsolatedModelsTestCase):
    def test_valid_field(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        errors = field.check()
        expected = []
        self.assertEqual(errors, expected)

    def test_missing_choices(self):
        class Model(LazyChoiceModelMixin, models.Model):
            field = LazyChoiceField()

        class Proxy(Model):
            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        errors = field.check()
        expected = []
        self.assertEqual(errors, expected)

    def test_non_iterable_choices(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = 'bad'

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = 'also-bad'

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        errors = field.check()
        expected = [
            checks.Error(
                "'FIELD_CHOICES' must be an iterable (e.g., a list or tuple).",
                hint=None,
                obj=Model,
                id='lazy_choices.E001',
            ),
            checks.Error(
                "'FIELD_CHOICES' must be an iterable (e.g., a list or tuple).",
                hint=None,
                obj=Proxy,
                id='lazy_choices.E001',
            ),
        ]
        self.assertEqual(errors, expected)

    def test_choices_containing_non_pairs(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [(1, 2, 3), (1, 2, 3)]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [(4, 5, 6), (4, 5, 6)]

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        errors = field.check()
        expected = [
            checks.Error(
                "'FIELD_CHOICES' must be an iterable containing (actual value, human readable name) tuples.",
                hint=None,
                obj=Model,
                id='lazy_choices.E002',
            ),
            checks.Error(
                "'FIELD_CHOICES' must be an iterable containing (actual value, human readable name) tuples.",
                hint=None,
                obj=Proxy,
                id='lazy_choices.E002',
            ),
        ]
        self.assertEqual(errors, expected)

    def test_non_subclassed_model(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        errors = field.check()
        expected = [
            checks.Error(
                "The model must inherit from 'LazyChoiceModelMixin'.",
                hint=None,
                obj=Model,
                id='lazy_choices.E003',
            )
        ]
        self.assertEqual(errors, expected)

    def test_raises_error_on_empty_string(self):
        class Model(LazyChoiceModelMixin, models.Model):
            field = LazyChoiceField()

        with self.assertRaisesMessage(exceptions.ValidationError, "'This field cannot be blank.'"):
            Model._meta.get_field('field').clean('', None)

    def test_cleans_empty_string_when_blank_true(self):
        class Model(LazyChoiceModelMixin, models.Model):
            field = LazyChoiceField(blank=True)

        self.assertEqual('', Model._meta.get_field('field').clean('', None))

    def test_raises_error_on_empty_input(self):
        class Model(LazyChoiceModelMixin, models.Model):
            field = LazyChoiceField(null=False)

        with self.assertRaisesMessage(exceptions.ValidationError, "'This field cannot be null.'"):
            Model._meta.get_field('field').clean(None, None)

    def test_cleans_valid_choice(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        self.assertEqual('foo', field.clean('foo', Model()))
        self.assertEqual('baz', field.clean('baz', Proxy()))

    def test_cleans_valid_choice_with_optgroup(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [(1, [('foo', 'Foo')]), (2, [('bar', 'Bar')])]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [(3, [('baz', 'Baz')]), (4, [('qux', 'Qux')])]

            class Meta:
                proxy = True

        field = Model._meta.get_field('field')
        self.assertEqual('foo', field.clean('foo', Model()))
        self.assertEqual('baz', field.clean('baz', Proxy()))

    def test_raises_error_on_invalid_choice(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

            class Meta:
                proxy = True

        with self.assertRaisesMessage(exceptions.ValidationError, "Value 'baz' is not a valid choice."):
            Model._meta.get_field('field').clean('baz', Model())

        with self.assertRaisesMessage(exceptions.ValidationError, "Value 'foo' is not a valid choice."):
            Model._meta.get_field('field').clean('foo', Proxy())

    def test_raises_error_on_invalid_choice_with_optgroup(self):
        class Model(LazyChoiceModelMixin, models.Model):
            FIELD_CHOICES = [(1, [('foo', 'Foo')]), (2, [('bar', 'Bar')])]

            field = LazyChoiceField()

        class Proxy(Model):
            FIELD_CHOICES = [(3, [('baz', 'Baz')]), (4, [('qux', 'Qux')])]

            class Meta:
                proxy = True

        with self.assertRaisesMessage(exceptions.ValidationError, "Value 'baz' is not a valid choice."):
            Model._meta.get_field('field').clean('baz', Model())

        with self.assertRaisesMessage(exceptions.ValidationError, "Value 'foo' is not a valid choice."):
            Model._meta.get_field('field').clean('foo', Proxy())

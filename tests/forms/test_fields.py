import copy

from django.core.exceptions import ValidationError
from django.db import models

from lazy_choices.forms.fields import LazyChoiceField

from .base import IsolatedModelsTestCase


class LazyChoiceFieldTests(IsolatedModelsTestCase):
    def test_deepcopy(self):
        class Model(models.Model):
            pass

        f1 = LazyChoiceField(choices_name='FIELD_CHOICES', model=Model)
        f2 = copy.deepcopy(f1)
        self.assertIsNot(f1, f2)
        self.assertEqual(f1.choices, f2.choices)
        self.assertIsNot(f1.choices, f2.choices)
        self.assertEqual(f1.model, f2.model)
        self.assertIs(f1.model, f2.model)

    def test_required(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES')

        self.assertRaisesMessage(ValidationError, "'This field is required.'", f.clean, '')
        self.assertRaisesMessage(ValidationError, "'This field is required.'", f.clean, None)
        self.assertEqual('foo', f.clean('foo'))
        self.assertRaisesMessage(
            ValidationError, "'Select a valid choice. abcd is not one of the available choices.'",
            f.clean, 'abcd'
        )

    def test_not_required(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES', required=False)

        self.assertEqual('', f.clean(''))
        self.assertEqual('', f.clean(None))
        self.assertEqual('foo', f.clean('foo'))
        self.assertRaisesMessage(
            ValidationError, "'Select a valid choice. abcd is not one of the available choices.'",
            f.clean, 'abcd'
        )

    def test_with_optgroup(self):
        class Model(models.Model):
            FIELD_CHOICES = [
                (1, [('foo', 'Foo'), ('bar', 'Bar')]),
                (2, [('baz', 'Baz'), ('qux', 'Qux')]),
                ('other', 'Other'),
            ]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES')
        self.assertEqual('foo', f.clean('foo'))
        self.assertEqual('baz', f.clean('baz'))
        self.assertEqual('other', f.clean('other'))
        self.assertRaisesMessage(
            ValidationError, "'Select a valid choice. invalid is not one of the available choices.'",
            f.clean, 'invalid'
        )

    def test_change_model_after_init(self):
        class ModelA(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        class ModelB(models.Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

        f = LazyChoiceField(model=ModelA, choices_name='FIELD_CHOICES')
        f.model = ModelB

        self.assertEqual('baz', f.clean('baz'))
        self.assertRaisesMessage(
            ValidationError,
            "Select a valid choice. foo is not one of the available choices.",
            f.clean,
            'foo'
        )

    def test_choices_with_field_required(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES')
        self.assertEqual([('', '---------'), ('foo', 'Foo'), ('bar', 'Bar')], f.choices)

    def test_choices_with_field_required_and_initial_value(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES', initial='foo')
        self.assertEqual([('foo', 'Foo'), ('bar', 'Bar')], f.choices)

    def test_choices_with_field_not_required(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES', required=False)
        self.assertEqual([('', '---------'), ('foo', 'Foo'), ('bar', 'Bar')], f.choices)

    def test_choices_with_field_not_required_and_initial_value(self):
        class Model(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        f = LazyChoiceField(model=Model, choices_name='FIELD_CHOICES', initial='foo', required=False)
        self.assertEqual([('', '---------'), ('foo', 'Foo'), ('bar', 'Bar')], f.choices)

    def test_set_model_changes_choices(self):
        class ModelA(models.Model):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        class ModelB(models.Model):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

        f = LazyChoiceField(model=ModelA, choices_name='FIELD_CHOICES')
        self.assertEqual([('', '---------'), ('foo', 'Foo'), ('bar', 'Bar')], f.choices)

        f.model = ModelB
        self.assertEqual([('', '---------'), ('baz', 'Baz'), ('qux', 'Qux')], f.choices)

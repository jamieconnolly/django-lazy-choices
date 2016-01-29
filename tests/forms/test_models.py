from django.db import models
from django.forms.fields import CharField

from lazy_choices import LazyChoiceField, LazyChoiceModelMixin
from lazy_choices.forms import LazyChoiceModelForm

from ..base import IsolatedModelsTestCase


class AbstractModel(LazyChoiceModelMixin, models.Model):
    field = LazyChoiceField()

    class Meta:
        abstract = True


class LazyChoiceModelFormTests(IsolatedModelsTestCase):
    def test_replace_model(self):
        class ModelA(AbstractModel):
            FIELD_CHOICES = [('foo', 'Foo'), ('bar', 'Bar')]

        class ModelB(AbstractModel):
            FIELD_CHOICES = [('baz', 'Baz'), ('qux', 'Qux')]

        class ModelForm(LazyChoiceModelForm):
            custom = CharField()

            class Meta:
                fields = '__all__'
                model = ModelA

        form = ModelForm(instance=ModelB())
        formfield = form.fields['field']
        self.assertEqual(formfield.choices, [('', '---------'), ('baz', 'Baz'), ('qux', 'Qux')])
        self.assertEqual(formfield.model, ModelB)

from django.db import models
from django.forms import CharField, inlineformset_factory

from lazychoices import LazyChoiceField, LazyChoiceModelMixin
from lazychoices.forms import LazyChoiceInlineFormSet, LazyChoiceModelForm

from .base import IsolatedModelsTestCase
from .models import Poem, Poet


class AbstractModel(LazyChoiceModelMixin, models.Model):
    field = LazyChoiceField()

    class Meta:
        abstract = True


class LazyChoiceInlineFormSetTests(IsolatedModelsTestCase):
    def test_construct_form(self):
        poet = Poet.objects.create(name='test')
        poet.poem_set.create(name='test poem')

        FormSet = inlineformset_factory(Poet, Poem, fields='__all__', formset=LazyChoiceInlineFormSet, extra=0)
        formset = FormSet(None, instance=poet)
        formset.lazy_model = Poem

        self.assertEqual(len(formset.forms), 1)
        self.assertTrue(hasattr(formset.forms[0], 'lazy_model'))
        self.assertEqual(formset.forms[0].lazy_model, Poem)

    def test_empty_form(self):
        FormSet = inlineformset_factory(Poet, Poem, fields='__all__', formset=LazyChoiceInlineFormSet, extra=0)
        formset = FormSet()
        formset.lazy_model = Poem

        self.assertTrue(hasattr(formset.empty_form, 'lazy_model'))
        self.assertEqual(formset.empty_form.lazy_model, Poem)


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
        self.assertEqual(form.lazy_model, ModelB)
        self.assertEqual(formfield.choices, [('', '---------'), ('baz', 'Baz'), ('qux', 'Qux')])
        self.assertEqual(formfield.model, ModelB)

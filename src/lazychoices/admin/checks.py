from django.contrib.admin.checks import InlineModelAdminChecks
from django.core import checks

from lazychoices.models import LazyChoiceModelMixin


class LazyChoiceInlineModelAdminChecks(InlineModelAdminChecks):
    def check(self, inline_obj, **kwargs):
        errors = super(LazyChoiceInlineModelAdminChecks, self).check(inline_obj)
        errors.extend(self._check_lazy_model(inline_obj))
        return errors

    def _check_lazy_model(self, obj):
        label = '.'.join([obj.__class__.__module__, obj.__class__.__name__])

        if not hasattr(obj, 'lazy_model'):
            return [
                checks.Error(
                    "'{0}' must have a 'lazy_model' attribute.".format(label),
                    hint=None,
                    obj=obj.__class__,
                    id='lazychoices.E101',
                )
            ]
        elif not issubclass(obj.lazy_model, LazyChoiceModelMixin):
            return [
                checks.Error(
                    "The value of '{option}' must inherit from '{parent}'.".format(
                        option='lazy_model', parent='LazyChoiceModelMixin'
                    ),
                    hint=None,
                    obj=obj.__class__,
                    id='lazychoices.E102',
                )
            ]
        else:
            return []

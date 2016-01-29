from django.apps import apps
from django.test import TestCase


class IsolatedModelsTestCase(TestCase):
    def setUp(self):
        # The unmanaged models need to be removed after the test in order to
        # prevent bad interactions with the flush operation in other tests.
        self._old_models = apps.app_configs['models'].models.copy()

    def tearDown(self):
        apps.app_configs['models'].models = self._old_models
        apps.all_models['models'] = self._old_models
        apps.clear_cache()

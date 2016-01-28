#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

DEFAULT_SETTINGS = dict(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
    },
    SECRET_KEY='notasecret',
)


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    test_runner = DiscoverRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()

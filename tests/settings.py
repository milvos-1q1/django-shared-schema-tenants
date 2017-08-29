# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "lq54#hsg57uikn$*=dk+4t$(zg*2k6!^5+8opzp^lsgyp$s-rj"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "rest_framework",

    "shared_schema_tenants.apps.SharedSchemaTenantsConfig",
    "exampleproject.exampleapp",
]

SITE_ID = 1


def is_url(context, value, original_value):
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError
    from django.utils.text import ugettext_lazy as _
    validate_url = URLValidator()
    try:
        validate_url(value)
    except ValidationError as e:
        raise ValidationError(_('This field must be a valid url'))
    return value

SHARED_SCHEMA_TENANTS = {
    "DEFAULT_TENANT_EXTRA_DATA_FIELDS": {
        'logo': {
            'type': 'string',
            'default': None,
            'validators': [is_url],
        },
        'number_of_employees': {
            'type': 'number',
            'default': 0,
        },
        'is_non_profit': {
            'type': 'boolean',
            'default': False,
        },
    },
    "DEFAULT_TENANT_SETTINGS_FIELDS": {
        'notify_users_by_email': {
            'type': 'boolean',
            'default': True
        },
    },
}

if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'shared_schema_tenants.middleware.TenantMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'shared_schema_tenants.middleware.TenantMiddleware',
    )

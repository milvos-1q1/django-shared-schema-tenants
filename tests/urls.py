# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from shared_schema_tenants.urls import urlpatterns as shared_schema_tenants_urls

urlpatterns = [
    url(r'^', include(shared_schema_tenants_urls, namespace='shared_schema_tenants')),
]

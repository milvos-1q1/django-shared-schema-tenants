# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ArticleViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=views.ArticleViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='details'
    ),
    url(
        regex=r'^tags/$',
        view=views.TagViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='list'
    ),
    url(
        regex=r'^tags/(?P<pk>\d+)/$',
        view=views.TagViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='details'
    ),
]

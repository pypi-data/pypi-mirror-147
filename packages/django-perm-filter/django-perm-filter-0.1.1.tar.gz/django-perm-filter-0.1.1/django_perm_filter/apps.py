# -*- coding: utf-8
from django.apps import AppConfig


class DjangoPermFilterConfig(AppConfig):
    name = 'django_perm_filter'
    verbose_name = 'Django Perm Filter'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from . import init  # noqa

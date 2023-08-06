import logging

from django.conf import settings
from django.contrib import admin
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def filter_perms(qs):
    """Taken directly from patch_admin_perms.py"""
    qs = qs.exclude(content_type__app_label__in=settings.PERM_FILTER["HIDE_APPS"])
    for perm in settings.PERM_FILTER["HIDE_PERMS"]:
        app, model = perm.split(".")
        qs = qs.exclude(content_type__app_label=app, codename=model)
    return qs


def unregister_models():
    if hasattr(settings, "PERM_FILTER"):
        for m in settings.PERM_FILTER["UNREGISTER_MODELS"]:
            try:
                model = import_string(m)
                admin.site.unregister(model)
            except (ModuleNotFoundError, RuntimeError) as e:
                logger.warning(
                    str(e)
                    + " Ensure the module is installed and/or added to INSTALLED_APPS if need be."
                )  # noqa

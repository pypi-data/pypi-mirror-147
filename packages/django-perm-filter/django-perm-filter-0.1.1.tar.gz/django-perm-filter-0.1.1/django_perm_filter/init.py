"""
Hide permissions and/or models in the Django admin which are irrelevant.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from .mixins import PermissionFilterMixin
from .utils import unregister_models

User = get_user_model()


class MyGroupAdmin(PermissionFilterMixin, GroupAdmin):
    pass


class MyUserAdmin(PermissionFilterMixin, UserAdmin):
    pass


# Override default registered Admin for User and Group
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
admin.site.register(Group, MyGroupAdmin)


unregister_models()

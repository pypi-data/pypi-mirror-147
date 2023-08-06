
# Django Perm Filter
A simple app that can be included in Django projects which hides app specific permissions from any type of User.  Easily add entire apps, specific permissions or models and it will take care of the rest.  Non-destructive (Does **not** delete permissions).

Typically we have **no reason**, in any Django project, to expose the following permissions for Users or Groups:

| App          | Model        | Permission                              |
|--------------|--------------|-----------------------------------------|
| admin        | log entry    | Can view/add/change/delete log entry    |
| auth         | permission   | Can view/add/change/delete permission   |
| contenttypes | content type | Can view/add/change/delete content type |
| sessions     | session      | Can view/add/change/delete session      |


## Features
- Hide all permissions for an App
- Hide permissions using app and codename (more granular)
- Hide models from the Django Admin

## Quickstart

Install Django Perm Filter::

```bash
pip install django-perm-filter
```

Add it to your `INSTALLED_APPS` at the bottom:

```python
INSTALLED_APPS = (
    ...
    'django_perm_filter',
)
```

In your `settings.py` add a entry for `PERM_FILTER`:
```
PERM_FILTER = {
    "HIDE_APPS": [
        # Django built-in apps
        "admin",
        "contenttypes",
        "sessions",
        "sites",
        # Other apps you wish to hide
    ],
    "HIDE_PERMS": [
        # Django built-in auth permissions
        "auth.view_permission",
        "auth.add_permission",
        "auth.change_permission",
        "auth.delete_permission",
        # Other app.codename perms you wish to hide
    ],
    "UNREGISTER_MODELS": [
        "django.contrib.sites.models.Site",
    ],
}
```

## Optional
By default Django Perms Filter will do the following when the app is ready. However, feel free to override to extend your own built-in Django Group or User Model Admins.
```
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from django_perm_filter import PermissionFilterMixin
from django_perm_filter import unregister_models

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
```

## Running Tests

Does the code actually work?

```bash
source <YOURVIRTUALENV>/bin/activate
(myenv) $ pip install tox
(myenv) $ tox
```

## Development commands

```bash
pip install -r requirements_dev.txt
invoke -l
```

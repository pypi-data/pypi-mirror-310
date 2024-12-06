from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# Register your models here.
from baykeshop.site.admin import site as bayke_site


@admin.register(User, site=bayke_site)
class BaykeUserAdmin(UserAdmin):
    pass


@admin.register(Group, site=bayke_site)
class BaykeGroupAdmin(GroupAdmin):
    pass

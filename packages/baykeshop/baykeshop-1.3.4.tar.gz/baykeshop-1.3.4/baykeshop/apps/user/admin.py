from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# Register your models here.
from baykeshop.site.admin import site as bayke_site
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = _('扩展信息')
    verbose_name_plural = _('扩展信息')


@admin.register(User, site=bayke_site)
class BaykeUserAdmin(UserAdmin):
    list_display = ('username', 'avatar', 'email', 'is_staff', 'date_joined', 'last_login')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    inlines = (UserProfileInline,)

    @admin.display(description=_('头像'))
    def avatar(self, obj):
        try:
            obj.profile
            return obj.profile.avatar.url
        except UserProfile.DoesNotExist:
            return ''
        


@admin.register(Group, site=bayke_site)
class BaykeGroupAdmin(GroupAdmin):
    pass

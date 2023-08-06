from django.contrib import admin, messages
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportMixin

from .models import Partner, PartnerAddress, PartnerContact
from .resources import PartnerResource
from .settings import partners_settings


class PartnerAddressInline(admin.StackedInline):
    model = PartnerAddress
    extra = 0
    autocomplete_fields = ["country"]


class PartnerContactInline(admin.TabularInline):
    model = PartnerContact
    extra = 0


class PartnerAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = PartnerResource
    list_display = ["inner_id", "partner_name", "user", "is_active", "is_verified"]
    search_fields = ["inner_id", "name"]
    date_hierarchy = "created_at"
    list_filter = ["partner_type", "is_active", "is_verified", "is_customer", "is_supplier"]
    inlines = [PartnerContactInline, PartnerAddressInline]
    actions = [
        "activate_partner",
        "verify_partner",
        "deactivate_partner",
        "deverify_partner",
    ]

    def has_view_permission(self, request, obj=None):
        return True

    def has_activate_permission(self, request, obj=None):
        return request.user.has_perms("activate_partner")

    def has_verify_permission(self, request, obj=None):
        return request.user.has_perms("verify_partner")

    def partner_name(self, obj):
        return Truncator(str(obj)).chars(60)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perms("change_partner_user"):
            return ["user"]
        return super().get_readonly_fields(request, obj)

    @admin.action(permissions=["activate"], description=_("Activate Partner"))
    def activate_partner(self, request, queryset):
        count = queryset.count()
        queryset.update(is_active=True)
        for obj in queryset.all():
            obj.activate()
        msg = _("Activate %s partner") % count
        messages.success(request, msg)

    @admin.action(permissions=["activate"], description=_("Deactivate Partner"))
    def deactivate_partner(self, request, queryset):
        count = queryset.count()
        for obj in queryset.all():
            obj.deactivate()
        msg = _("Deactivate %s partners") % count
        messages.success(request, msg)

    @admin.action(permissions=["verify"], description=_("Verify Partner"))
    def verify_partner(self, request, queryset):
        try:
            count = queryset.count()
            for obj in queryset.all():
                obj.verify()
            msg = _("Verify %s partner") % count
            messages.success(request, msg)
        except Exception as err:
            messages.error(request, err)

    @admin.action(permissions=["verify"], description=_("Deverify Partner"))
    def deverify_partner(self, request, queryset):
        count = queryset.count()
        for obj in queryset.all():
            obj.deverify()
        msg = _("Deverify %s partner") % count
        messages.success(request, msg)


admin.site.register(Partner, partners_settings.PARTNER_ADMIN)

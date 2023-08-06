from django.apps import AppConfig as BaseAppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class SimpelPartnersConfig(BaseAppConfig):
    icon = "account-box-outline"
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpel_partners"
    label = "simpel_partners"
    verbose_name = _("Partners")

    def ready(self):
        post_migrate.connect(init_app, sender=self)
        return super().ready()


def init_app(**kwargs):
    pass

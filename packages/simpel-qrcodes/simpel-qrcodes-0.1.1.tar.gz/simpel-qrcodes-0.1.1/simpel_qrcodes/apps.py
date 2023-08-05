from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class SimpelQrcodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "simpel_qrcodes"
    label = "simpel_qrcodes"
    icon = "qrcode-scan"
    verbose_name = _("QRCodes")

    def ready(self):
        post_migrate.connect(init_app, sender=self)


def init_app(sender, **kwargs):
    pass

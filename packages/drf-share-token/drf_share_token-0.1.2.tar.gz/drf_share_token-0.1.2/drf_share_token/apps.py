from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "drf_share_token"
    verbose_name = _("DRF Share token")

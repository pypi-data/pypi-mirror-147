from datetime import timedelta
from django.conf import settings

from rest_framework.settings import APISettings

SHARE_TOKEN_SETTINGS = getattr(settings, "SHARE_TOKEN", None)

DEFAULTS = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
}

config = APISettings(SHARE_TOKEN_SETTINGS, DEFAULTS)

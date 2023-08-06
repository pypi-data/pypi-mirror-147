from typing import TypedDict

from django.db import models
from jwt import encode as jwt_encode, decode as jwt_decode
from .settings import config


class ShareTokenPayload(TypedDict):
    resource: str
    id: int


def encode(instance: models.Model) -> str:
    meta = instance._meta

    return jwt_encode({
        'resource': f"{meta.app_label}:{meta.model_name}",
        'id': instance.id
    }, config.SIGNING_KEY, algorithm=config.ALGORITHM)


def decode(token: str) -> ShareTokenPayload:
    return jwt_decode(token, config.SIGNING_KEY, algorithms=(config.ALGORITHM,))

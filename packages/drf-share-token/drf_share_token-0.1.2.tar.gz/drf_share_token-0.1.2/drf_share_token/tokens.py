from typing import TypedDict, List, Optional

from django.db import models
from jwt import encode as jwt_encode, decode as jwt_decode
from .settings import config


class ShareTokenPayload(TypedDict):
    resource: str
    id: int
    actions: List[int]


def encode(instance: models.Model, actions: Optional[List[str]] = ['retrieve',]) -> str:
    meta = instance._meta
    payload = {
        'resource': f"{meta.app_label}:{meta.model_name}",
        'id': instance.id
    }

    if actions:
        payload['actions'] = actions
    return jwt_encode(payload, config.SIGNING_KEY, algorithm=config.ALGORITHM)


def decode(token: str) -> ShareTokenPayload:
    return jwt_decode(token, config.SIGNING_KEY, algorithms=(config.ALGORITHM,))

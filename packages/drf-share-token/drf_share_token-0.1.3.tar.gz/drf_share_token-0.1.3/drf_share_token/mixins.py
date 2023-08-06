from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from requests.models import PreparedRequest

from drf_share_token.tokens import encode


class ShareTokenMixin:
    share_token_actions = ('retrieve',)

    @action(detail=True, methods=('GET',))
    def share(self, request, *args, **kwargs):

        instance = self.get_object()
        token = encode(instance, actions=self.share_token_actions)
        return Response(data={
            "token": token,
            "link": self.get_token_link(instance, token),
        })

    def get_token_link(self, instance: models.Model, token: str) -> str:
        return self.reverse_action("detail", (instance.id,))
        # url = self.reverse_action("detail", (instance.id,))
        # params = {'token': token}
        #
        # req = PreparedRequest()
        # req.prepare_url(url, params)
        #
        # return req.url

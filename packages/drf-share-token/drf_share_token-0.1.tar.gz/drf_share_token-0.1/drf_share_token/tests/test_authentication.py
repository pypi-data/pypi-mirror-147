import json

from django.test import TestCase, override_settings

from django.urls import include, path
from rest_framework import permissions, status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import GenericViewSet
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase
from rest_framework.test import RequestsClient

from drf_share_token.mixins import ShareTokenMixin
from drf_share_token.permissions import HasValidShareToken
from drf_share_token.settings import config
from drf_share_token.tests.models import FakeModel
from drf_share_token.tests.serializer import FakeModelSerializer
from drf_share_token.tokens import encode

factory = APIRequestFactory()


class FakeModelViewset(GenericViewSet, RetrieveModelMixin, ShareTokenMixin):
    queryset = FakeModel.objects.all()
    permission_classes = (permissions.IsAuthenticated, HasValidShareToken)
    serializer_class = FakeModelSerializer


router = SimpleRouter()
router.register(r'fake-model', FakeModelViewset)



@override_settings(REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'drf_share_token.authentication.ShareTokenAuthentication',
    ]
})
class ShareTokenAuthenticationTestCase(URLPatternsTestCase):
    urlpatterns = [
        path('api/', include(router.urls)),
    ]
    databases = ('default',)

    def test_valid_token_authentication(self):
        config.SIGNING_KEY = "oewrhfopwhfopenfw"
        instance = FakeModel.objects.create(id=999)
        token = encode(instance)

        client = RequestsClient()
        client.headers.update({'Authorization': f'Token {token}'})
        response = client.get(f'http://testserver/api/fake-model/{instance.id}/')

        self.assertEqual(response.status_code, 200)
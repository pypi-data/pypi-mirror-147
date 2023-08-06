import json

from django.test import TestCase, override_settings

from django.urls import include, path
from rest_framework import permissions, status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import GenericViewSet
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase

from drf_share_token.mixins import ShareTokenMixin
from drf_share_token.tests.models import FakeModel

factory = APIRequestFactory()


class FakeModelViewset(GenericViewSet, RetrieveModelMixin, ShareTokenMixin):
    queryset = FakeModel.objects.all()
    permission_classes = (permissions.AllowAny,)


router = SimpleRouter()
router.register(r'fake-model', FakeModelViewset)


class ShareTokenTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include(router.urls)),
    ]

    def test_get_token_path(self):
        view = FakeModelViewset()
        view.basename = router.get_default_basename(FakeModelViewset)
        view.request = None

        self.assertEqual('/api/fake-model/1/share/', view.reverse_action('share', [1]))

    def test_retrieve_token(self) -> None:
        instance = FakeModel.objects.create()

        response = self.client.get(f'/api/fake-model/{instance.id}/share/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual('str', payload['token'])
        self.assertEqual(f'http://testserver/api/fake-model/{instance.id}/', payload['link'])


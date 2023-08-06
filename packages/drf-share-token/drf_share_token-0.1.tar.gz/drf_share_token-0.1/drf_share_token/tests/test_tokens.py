from django.test import TestCase

from drf_share_token.settings import config
from drf_share_token.tests.models import FakeModel
from drf_share_token.tokens import encode


class DefaultTokenTestCase(TestCase):

    fake_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZXNzb3VyY2UiOiJ0ZXN0czpmYWtlbW9kZWwiLCJpZCI6OTk5fQ.xfzbSQdTDnekkHUmNewOjjOMhjoyXOGKcrOsyLIMfVU"

    def test_encode_token(self):
        config.SIGNING_KEY = "abcdefghijklmnopqrstuvwxyz"
        instance = FakeModel(id=999)

        self.assertEqual(self.fake_token, encode(instance))

    def test_encode_token_wrong_signing_key(self):
        config.SIGNING_KEY = "123456"
        instance = FakeModel(id=999)

        self.assertNotEqual(self.fake_token, encode(instance))


from rest_framework import serializers

from drf_share_token.tests.models import FakeModel


class FakeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FakeModel
        fields = ('id',)
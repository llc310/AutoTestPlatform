from rest_framework import serializers

from case_api.models import Case, Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = "__all__"


class CaseAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"

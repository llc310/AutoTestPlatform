from rest_framework import serializers

from case_api.models import CaseAPI, Endpoint, CaseAPIInfo


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = "__all__"


class CaseAPIInfoSerializer(serializers.ModelSerializer):
    endpoint = EndpointSerializer()

    class Meta:
        model = CaseAPIInfo
        fields = "__all__"


class CaseAPISerializer(serializers.ModelSerializer):
    caseapiinfo = CaseAPIInfoSerializer(many=True)

    class Meta:
        model = CaseAPI
        fields = "__all__"

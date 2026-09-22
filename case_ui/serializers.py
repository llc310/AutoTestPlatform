from rest_framework import serializers

from case_ui.models import CaseUI, CaseUIInfo, Element


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class CaseUIInfoSerializer(serializers.ModelSerializer):
    element = ElementSerializer(many=True)

    class Meta:
        model = CaseUIInfo
        fields = "__all__"


class CaseUISerializer(serializers.ModelSerializer):
    caseuiinfo = CaseUIInfoSerializer(many=True)

    class Meta:
        model = CaseUI
        fields = "__all__"

from rest_framework import serializers

from case_ui.models import CaseUI, Element


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class StepSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=32)
    keyword = serializers.CharField(max_length=32)
    args = serializers.ListField()


class CaseUISerializer(serializers.ModelSerializer):
    step = StepSerializer(many=True)

    class Meta:
        model = CaseUI
        fields = "__all__"

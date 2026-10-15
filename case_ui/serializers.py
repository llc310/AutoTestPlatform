from rest_framework import serializers

from case_ui.models import CaseUI, CaseUIInfo, Element, Step


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"


class CaseUIInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseUIInfo
        fields = "__all__"


class CaseUISerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseUI
        fields = "__all__"

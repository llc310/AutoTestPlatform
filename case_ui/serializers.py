from rest_framework import serializers

from case_ui.models import CaseUI, CaseUIInfo, Element, Step


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):
    element = ElementSerializer(many=True)

    class Meta:
        model = Step
        fields = "__all__"


class CaseUIInfoSerializer(serializers.ModelSerializer):
    step = StepSerializer(many=True)
    class Meta:
        model = CaseUIInfo
        fields = "__all__"


class CaseUISerializer(serializers.ModelSerializer):
    step_count = serializers.SerializerMethodField()

    class Meta:
        model = CaseUI
        fields = "__all__"

    def get_step_count(self,obj):
        return obj.get_step_count()



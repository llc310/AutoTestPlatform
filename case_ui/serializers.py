from rest_framework import serializers

from case_ui.models import CaseUI, Element, KeyWord, Action


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class CaseUISerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUI
        fields = "__all__"

    def validate(self, attrs):
        super().validate(attrs)
        action_list:list = attrs.get("action_list",[])
        length = -1
        for action in action_list:
            if "parametrize" in action:
                for _,param_value in action["parametrize"].items():
                    if length == -1:
                        length = len(param_value)
                        continue
                    elif length != len(param_value):
                        raise serializers.ValidationError("每个parametrize参数长度不一致")
        return attrs
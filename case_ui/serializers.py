from rest_framework import serializers

from case_ui.models import CaseUI, Element, KeyWord, Action, CaseUIAction


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


    def validate(self, attrs):
        super().validate(attrs)
        parametrize_dict:dict = attrs.get("parametrize",{})
        length = -1
        for value in parametrize_dict.values():
            if length == -1:
                length = len(value)
                continue
            elif length != len(value):
                raise serializers.ValidationError("每个parametrize参数长度不一致")
        return attrs


class CaseUISerializer(serializers.ModelSerializer):
    action_id = ActionSerializer(many=True,read_only=True)
    class Meta:
        model = CaseUI
        fields = "__all__"


class CaseUIActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUIAction
        fields = "__all__"
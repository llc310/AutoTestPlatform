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


class CaseUISerializer(serializers.ModelSerializer):
    action_id = ActionSerializer(many=True,read_only=True)
    class Meta:
        model = CaseUI
        fields = "__all__"


class CaseUIActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUIAction
        fields = "__all__"
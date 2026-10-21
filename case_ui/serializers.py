from rest_framework import serializers

from case_ui.models import CaseUI, Element, KeyWord, Allure, Parametrize, Validate, Action, Step, CaseUIStep


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = "__all__"


class AllureSerializer(serializers.ModelSerializer):
    class Meat:
        model = Allure
        fields = "__all__"


class ParametrizeSerializer(serializers.ModelSerializer):
    class Meat:
        model = Parametrize
        fields = "__all__"


class ValidateSerializer(serializers.ModelSerializer):
    class Meat:
        model = Validate
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):


    class Meat:
        model = Action
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):
    class Meat:
        model = Step
        fields = "__all__"


class CaseUISerializer(serializers.ModelSerializer):
    class Meat:
        model = CaseUI
        fields = "__all__"


class CaseUIStepSerializer(serializers.ModelSerializer):
    class Meat:
        model = CaseUIStep
        fields = "__all__"
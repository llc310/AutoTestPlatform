from rest_framework import serializers

from case_ui.models import CaseUI, Element, KeyWord, Allure, Parametrize, Validate, Action, Step, CaseUIAction


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = "__all__"


class AllureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allure
        fields = "__all__"


class ParametrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametrize
        fields = "__all__"

    def validate(self, attrs):
        param_value = attrs["param_value"]
        if isinstance(param_value,list) and isinstance(param_value[0],(int,str)):
            return attrs
        else:
            raise serializers.ValidationError("param_value类型错误")

class ValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validate
        fields = "__all__"

    def validate(self, attrs):
        validate_params = attrs["validate_params"]
        if isinstance(validate_params,list) and isinstance(validate_params[0],(int,str)):
            return attrs
        else:
            raise serializers.ValidationError("validate_params类型错误")

class StepSerializer(serializers.ModelSerializer):
    keyword_id = KeyWordSerializer()
    class Meta:
        model = Step
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    allure_id = AllureSerializer(read_only=True)
    parametrize_id = ParametrizeSerializer(read_only=True)
    validate_id = ValidateSerializer(read_only=True)
    step_id = StepSerializer(many=True,read_only=True)

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
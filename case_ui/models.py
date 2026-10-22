import yaml
from django.db import models

from project.models import Project


# Create your models here.
class Element(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="元素名称", max_length=32)
    by = models.CharField(verbose_name="定位方式",max_length=32)
    path = models.CharField(verbose_name="定位路径")

    project_id = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )


class KeyWord(models.Model):
    objects: models.QuerySet

    keyword_name = models.CharField(verbose_name="关键字名",max_length=64)
    description = models.CharField(verbose_name="操作描述",max_length=64)


class Allure(models.Model):
    objects: models.QuerySet

    feature = models.CharField(verbose_name="所属模块",max_length=64,default="")
    story = models.CharField(verbose_name="功能名",max_length=64,default="")
    title = models.CharField(verbose_name="用例标题",max_length=64,default="")
    description = models.CharField(verbose_name="用例描述",max_length=64,default="")


class Parametrize(models.Model):
    objects: models.QuerySet

    param_key = models.CharField(verbose_name="参数化键名",max_length=64)
    param_value = models.JSONField(verbose_name="参数化键值")


class Validate(models.Model):
    objects: models.QuerySet

    class ValidateType(models.TextChoices):
        EQUALS = "equals"
        CONTAINS = "contains"
        DB_EQUALS = "db_equals"
        DB_CONTAINS = "db_contains"

    validate_type = models.CharField(verbose_name="断言类型",choices=ValidateType.choices)
    validate_params = models.JSONField(verbose_name="断言参数")


class Action(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="操作名",max_length=64)
    sort = models.PositiveIntegerField(verbose_name="执行顺序")

    project_id = models.ForeignKey(
        verbose_name="项目id",
        to=Project,
        on_delete=models.CASCADE
    )
    allure_id = models.OneToOneField(
        verbose_name="allure参数id",
        to=Allure,
        on_delete=models.CASCADE
    )
    parametrize_id = models.OneToOneField(
        verbose_name="parametrize参数id",
        to=Parametrize,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    validate_id = models.OneToOneField(
        verbose_name="validate参数id",
        to=Validate,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["sort"]


class Step(models.Model):
    objects: models.QuerySet

    action = models.CharField(verbose_name="操作", max_length=64)
    params = models.JSONField(verbose_name="参数值", blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name="执行顺序")

    keyword_id = models.ForeignKey(
        verbose_name="关键字id",
        to=KeyWord,
        null=True,
        on_delete=models.SET_NULL,
    )
    element_id = models.ForeignKey(
        verbose_name="页面元素id",
        to=Element,
        null=True,
        on_delete=models.SET_NULL,
    )
    action_id = models.ForeignKey(
        verbose_name="测试步骤id",
        to=Action,
        related_name="step_id",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["order"]


class CaseUI(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="UI测试用例名称",max_length=64)

    project_id = models.ForeignKey(verbose_name="项目id", to=Project, on_delete=models.CASCADE)
    action_id = models.ManyToManyField(
        verbose_name="操作id",
        to=Action,
        through="CaseUIAction",
        through_fields=("caseui_id","action_id")
    )

    class Meta:
        ordering = ["id"]

    def to_yaml(self, yaml_path):
        from case_ui.serializers import CaseUISerializer

        serializer = CaseUISerializer(self)
        data = serializer.data

        case = []
        for caseuiinfo in data["caseuiinfo"]:
            caseinfo = {}
            if caseuiinfo["allure"]:
                for key, value in caseuiinfo["allure"].items():
                    if value:
                        caseinfo[key] = value
            step_list = []
            for step in caseuiinfo["step"]:
                locator = Element.objects.get(id=step["locator"]).locator
                step["locator"] = [locator["by"], locator["value"]]
                step_list.append(step)
            caseinfo["step"] = step_list
            if caseuiinfo["parametrize"]:
                caseinfo.update({"parametrize": caseuiinfo["parametrize"]})
            if caseuiinfo["validate"]:
                caseinfo.update({"validate": caseuiinfo["validate"]})
            case.append(caseinfo)

        with open(file=yaml_path, mode="w", encoding="utf-8") as f:
            yaml.safe_dump(case, f, allow_unicode=True, sort_keys=False)


class CaseUIAction(models.Model):
    sort = models.PositiveIntegerField(verbose_name="执行顺序")

    caseui_id = models.ForeignKey(verbose_name="UI测试用例id",to=CaseUI,on_delete=models.CASCADE)
    action_id = models.ForeignKey(verbose_name="测试步骤id",to=Action,on_delete=models.CASCADE)

    class Meta:
        ordering = ["caseui_id","sort"]
        unique_together = ["caseui_id","sort"]
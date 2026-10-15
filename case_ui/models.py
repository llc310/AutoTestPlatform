import yaml
from django.db import models

from project.models import Project


# Create your models here.
class Element(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="元素名称", max_length=32)
    by = models.CharField(verbose_name="定位方式",max_length=32)
    locator = models.CharField(verbose_name="定位路径")
    project = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )


class Step(models.Model):
    objects: models.QuerySet

    element = models.ManyToManyField(verbose_name="页面元素id",to=Element)

    order = models.PositiveBigIntegerField(verbose_name="页面操作执行顺序")
    action = models.CharField(verbose_name="页面操作名称",max_length=64)
    keyword = models.CharField(verbose_name="页面操作关键字",max_length=64)
    args = models.JSONField(verbose_name="函数参数",blank=True,default=list)

    class Meta:
        ordering = ["order"]


class CaseUIInfo(models.Model):
    objects: models.QuerySet

    step = models.ManyToManyField(verbose_name="操作顺序",to=Step)

    name = models.CharField(verbose_name="ui测试步骤名称", max_length=32)
    allure = models.JSONField(verbose_name="allure参数", blank=True, null=True)
    parametrize = models.JSONField(verbose_name="参数化参数", blank=True, null=True)
    validate = models.JSONField(verbose_name="断言参数", blank=True, null=True)


class CaseUI(models.Model):
    objects: models.QuerySet

    project = models.ForeignKey(
        verbose_name="项目id",
        to=Project,
        on_delete=models.CASCADE,
        related_name="case_ui",
    )
    caseuiinfo = models.ManyToManyField(verbose_name="ui测试用例id", to=CaseUIInfo)

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

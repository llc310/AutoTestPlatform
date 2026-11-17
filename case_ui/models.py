import copy

import yaml
from django.db import models

from project.models import Project


# Create your models here.
class Element(models.Model):
    objects: models.QuerySet

    class ByValue(models.TextChoices):
        ID = "id", "id"
        XPATH = "xpath", "xpath"
        LINK_TEXT = "link text", "link text"
        PARTIAL_LINK_TEXT = "partial link text", "partial link text"
        NAME = "name", "name"
        TAG_NAME = "tag name", "tag name"
        CLASS_NAME = "class name", "class name"
        CSS_SELECTOR = "css selector", "css selector"

    name = models.CharField(verbose_name="元素名称", max_length=32)
    by = models.CharField(verbose_name="定位方式",max_length=32,choices=ByValue,default=ByValue.XPATH)
    path = models.CharField(verbose_name="定位路径")

    project_id = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["id"]


class KeyWord(models.Model):
    objects: models.QuerySet

    keyword_name = models.CharField(verbose_name="关键字名",max_length=64)
    description = models.CharField(verbose_name="操作描述",max_length=64)

    class Meta:
        ordering = ["id"]


class Action(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="操作名",max_length=64)
    allure = models.JSONField(verbose_name="allure参数")
    step = models.JSONField(verbose_name="页面操作步骤")
    parametrize = models.JSONField(verbose_name="参数化参数",blank=True)
    validate = models.JSONField(verbose_name="断言参数",blank=True)

    project_id = models.ForeignKey(
        verbose_name="项目id",
        to=Project,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["id"]



class CaseUI(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="UI测试用例名称",max_length=64)

    project_id = models.ForeignKey(verbose_name="项目id", to=Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]

    # 将数据库中的用例信息转化为YAML测试文件
    def to_yaml(self, yaml_path):
        from case_ui.models import CaseUIAction
        case = []

        caseuiactions = CaseUIAction.objects.filter(caseui_id=self.id).select_related("action_id").order_by("sort")
        actions = [caseuiaction.action_id for caseuiaction in caseuiactions]
        for action in actions:
            # 获取allure参数
            action_dict = {}
            action_dict.update(action.allure)
            # 获取step
            action_dict.update({"step": []})
            for step in action.step:
                step_dict = {}
                step_dict.update({"action": step["action"]})
                step_dict.update({"keyword": KeyWord.objects.get(id=step["keyword_id"]).keyword_name})
                if "element_id" in step:
                    element = Element.objects.get(id=step["element_id"])
                    step_dict.update({"locator": [element.by,element.path]})
                if "args" in step:
                    step_dict.update({"args": step["args"]})
                action_dict["step"].append(step_dict)
            # 获取parametrize
            if action.parametrize:
                action_dict.update({"parametrize": action.parametrize})
            # 获取validate
            if action.validate:
                validate_dict = copy.deepcopy(action.validate)
                for _,type in validate_dict.items():
                    for result_assert in type:
                        actual_result:dict = result_assert["actual_result"]
                        # 获取keyword
                        keyword = KeyWord.objects.get(id=actual_result.pop("keyword_id")).keyword_name
                        actual_result.update({"keyword": keyword})
                        # 获取locator
                        if "element_id" in actual_result:
                            element = Element.objects.get(id=actual_result.pop("element_id"))
                            actual_result.update({"locator": [element.by, element.path]})
                action_dict.update({"validate": validate_dict})

            case.append(action_dict)

        # 将数据写入YAML文件
        with open(file=yaml_path,encoding="utf-8",mode="w") as f:
            yaml.safe_dump(data=case,stream=f,allow_unicode=True,sort_keys=False)


class CaseUIAction(models.Model):
    objects: models.QuerySet

    sort = models.PositiveIntegerField(verbose_name="执行顺序")

    caseui_id = models.ForeignKey(verbose_name="UI测试用例id",to=CaseUI,on_delete=models.CASCADE)
    action_id = models.ForeignKey(verbose_name="测试步骤id",to=Action,on_delete=models.CASCADE)

    class Meta:
        ordering = ["caseui_id","sort"]
        unique_together = ["caseui_id","sort"]
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

    action_list = models.JSONField(verbose_name="测试步骤")

    project_id = models.ForeignKey(verbose_name="项目id", to=Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]

    # 将数据库中的用例信息转化为YAML测试文件
    def to_yaml(self, yaml_path):
        # 将数据写入YAML文件
        with open(file=yaml_path,encoding="utf-8",mode="w") as f:
            yaml.safe_dump(data=self.action_list,stream=f,allow_unicode=True,sort_keys=False)

from django.db import models

from project.models import Project


# Create your models here.
class Element(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="元素名称", max_length=32)
    locator = models.JSONField(verbose_name="定位")
    project = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )


class Case(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="ui测试用例名称", max_length=32)
    project = models.ForeignKey(
        verbose_name="项目id",
        to=Project,
        on_delete=models.CASCADE,
        related_name="case_ui",
    )
    allure = models.JSONField(verbose_name="allure参数", blank=True, null=True)
    step = models.JSONField(verbose_name="用例步骤", blank=True, null=True)
    parametrize = models.JSONField(verbose_name="参数化参数", blank=True, null=True)
    validate = models.JSONField(verbose_name="断言参数", blank=True, null=True)

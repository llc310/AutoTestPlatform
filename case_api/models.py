from django.db import models

from project.models import Project


# Create your models here.
class Endpoint(models.Model):
    name = models.CharField(verbose_name="接口名称", max_length=32)
    project = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )
    method = models.CharField(verbose_name="请求方法", max_length=8)
    url = models.CharField(verbose_name="网址", max_length=255)
    params = models.JSONField(
        verbose_name="查询字符串", max_length=10240, blank=True, null=True
    )
    data = models.JSONField(
        verbose_name="表单参数", max_length=10240, blank=True, null=True
    )
    json = models.JSONField(
        verbose_name="JSON参数", max_length=10240, blank=True, null=True
    )
    cookies = models.JSONField(
        verbose_name="COOKIE信息", max_length=10240, blank=True, null=True
    )
    headers = models.JSONField(
        verbose_name="请求头", max_length=10240, blank=True, null=True
    )


class Case(models.Model):
    name = models.CharField(verbose_name="接口测试用例名称", max_length=32)
    project = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )
    endpoint = models.ForeignKey(
        verbose_name="接口id", to=Endpoint, on_delete=models.CASCADE
    )
    allure = models.JSONField(verbose_name="allure参数", blank=True, null=True)
    api_args = models.JSONField(verbose_name="接口用例参数", blank=True, null=True)
    extract = models.JSONField(verbose_name="提取参数", blank=True, null=True)
    parametrize = models.JSONField(verbose_name="参数化参数", blank=True, null=True)
    validate = models.JSONField(verbose_name="断言参数", blank=True, null=True)

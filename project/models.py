from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet


# Create your models here.
class Project(models.Model):
    objects: QuerySet

    name = models.CharField(verbose_name="项目名称", max_length=32)
    description = models.CharField(
        verbose_name="项目简介", max_length=128, default="测试项目"
    )
    base_url = models.CharField(verbose_name="项目网址", default="")
    user_list = models.ManyToManyField(
        verbose_name="项目成员", to=User, blank=True, related_name="project_users"
    )
    project_leader = models.ForeignKey(
        verbose_name="项目管理人", to=User, null=True, on_delete=models.SET_NULL
    )


class Config(models.Model):
    objects: QuerySet

    project = models.ForeignKey(
        verbose_name="项目", to=Project, on_delete=models.CASCADE
    )
    conftest = models.TextField(verbose_name="pytest项目配置文件", default="")

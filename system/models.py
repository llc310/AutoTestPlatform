from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Department(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="部门名称", max_length=32)
    leader = models.ForeignKey(
        verbose_name="部门领导",
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )

    description = models.CharField(
        verbose_name="部门描述", max_length=128, default="公司部门"
    )


class Position(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="职位名称", max_length=32)
    is_leader = models.BooleanField(verbose_name="是否负责人", default=False)


class Role(models.Model):
    objects: models.QuerySet

    user = models.ForeignKey(verbose_name="用户", to=User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        verbose_name="部门", to=Department, on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        verbose_name="职位", to=Position, on_delete=models.CASCADE
    )

from pathlib import Path

import time
from django.db import models

from case_api.models import CaseAPI as CaseAPI
from case_ui.models import CaseUI
from project.models import Project
from suite.tasks import pool, run_api_case


# Create your models here.
class Suite(models.Model):
    objects: models.QuerySet

    project = models.ForeignKey(verbose_name="项目id", to=Project, on_delete=models.CASCADE)
    case_ui_list = models.ManyToManyField(verbose_name="UI测试用例id", to=CaseUI)
    case_api_list = models.ManyToManyField(verbose_name="接口测试用例id", to=CaseAPI)

    name = models.CharField(verbose_name="套件名称", max_length=32)
    description = models.CharField(verbose_name="套件名称", blank=True, max_length=32)

    def case_ui_count(self):
        return self.case_ui_list.all().count()

    def case_api_count(self):
        return self.case_api_list.all().count()

    def run(self):
        # 创建工作目录
        path = Path("upload_yaml") / f"project_{self.project.id}" / f"suite_{self.id}"

        # 创建存放测试用例的目录
        api_path = path / "api"
        api_path.mkdir(parents=True, exist_ok=True)
        ui_path = path / "ui"
        ui_path.mkdir(parents=True, exist_ok=True)

        # 创建并执行测试用例yaml文件
        if self.case_api_list:
            for case_api in self.case_api_list.all():
                yaml_path = api_path / f"test_api_{case_api.id}.yaml"
                case_api.to_yaml(yaml_path)
                run_result = RunResult.objects.create(
                    suite = self.id,
                    path = yaml_path
                )
                pool.submit(run_api_case,yaml_path,run_result.id)


class RunResult(models.Model):
    objects: models.QuerySet

    class RunStatus(models.IntegerChoices):
        Init = 0, "初始化"
        Running = 1, "正在执行"
        Reporting = 2, "正在输出报告"
        Done = 3, "执行完毕"
        Reporting_Done = 4, "报告输出完毕"
        Error = -1, "执行出错"

    suite = models.ForeignKey(verbose_name="测试套件id", to=Suite, on_delete=models.CASCADE)

    path = models.CharField(verbose_name="用例路径", max_length=256)
    is_pass = models.BooleanField(verbose_name="是否通过", default=False)
    status = models.IntegerField(verbose_name="用例状态", choices=RunStatus, default=RunStatus.Init)

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_datetime = models.DateTimeField(verbose_name="更新时间", auto_now=True)

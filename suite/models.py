
from pathlib import Path


import pytest
from django.db import models
from django_q.models import Schedule

from django_q.tasks import schedule

from case_api.models import CaseAPI as CaseAPI
from case_ui.models import CaseUI
from project.models import Project
from suite.tasks import merge_all_report_log, pool, run_api_case, run_ui_case


# Create your models here.
class Suite(models.Model):
    objects: models.QuerySet

    schedule = models.ForeignKey(to=Schedule,null=True,on_delete=models.SET_NULL)

    class RunType(models.TextChoices):
        ONCE = "O"
        CRON = "C"

    project = models.ForeignKey(
        verbose_name="项目id", to=Project, on_delete=models.CASCADE
    )
    case_ui_list = models.ManyToManyField(
        verbose_name="UI测试用例id", to=CaseUI, blank=True
    )
    case_api_list = models.ManyToManyField(
        verbose_name="接口测试用例id", to=CaseAPI, blank=True
    )

    name = models.CharField(verbose_name="套件名称", max_length=32)
    description = models.CharField(verbose_name="套件名称", blank=True, max_length=32)
    run_type = models.CharField(verbose_name="运行模式",choices=RunType,default=RunType.ONCE)
    cron = models.CharField(verbose_name="运行表达式",max_length=32,blank=True)

    def case_ui_count(self):
        return self.case_ui_list.all().count()

    def case_api_count(self):
        return self.case_api_list.all().count()

    def save(self,*args,**kwargs) -> None:

        if self.run_type == self.RunType.CRON:
            Schedule.objects.filter(name=f"cron_套件{self.id}").delete()  # 删旧防重复
            schedule(
                "suite.tasks.run_by_cron",
                self.id,  # 位置参数 = 套件 id
                name=f"cron_套件{self.id}",  # 固定 name，配合上面去重
                schedule_type=Schedule.CRON,  # "C"
                cron=self.cron,  # "*/2 * * * *"
                repeats=-1,  # 无限
            )
        else:
            if self.schedule:
                self.schedule.delete()
        return super().save(*args, **kwargs)
    def run(self):
        # 创建工作目录
        path = Path("upload_yaml") / f"project_{self.project.id}" / f"suite_{self.id}"

        run_result = RunResult.objects.create(suite=self, path=path)
        # 创建存放测试用例的目录
        api_path = path / "api"
        api_path.mkdir(parents=True, exist_ok=True)
        ui_path = path / "ui"
        ui_path.mkdir(parents=True, exist_ok=True)

        # 创建并执行测试用例yaml文件
        futures = []
        run_type = []
        if self.case_api_list.exists():
            for case_api in self.case_api_list.all():
                yaml_path = api_path / f"test_api_{case_api.id}.yaml"
                case_api.to_yaml(yaml_path)
            futures.append(pool.submit(run_api_case, api_path, run_result.id, "api"))
            run_type.append("api")

        if self.case_ui_list.exists():
            for case_ui in self.case_ui_list.all():
                yaml_path = ui_path / f"test_ui_{case_ui.id}.yaml"
                case_ui.to_yaml(yaml_path)
            futures.append(pool.submit(run_ui_case, ui_path, run_result.id, "ui"))
            run_type.append("ui")

        results = [future.result(timeout=900) for future in futures]
        is_pass = all(res_code == pytest.ExitCode.OK for res_code in results)

        # 合并测试结果
        run_result.status = RunResult.RunStatus.Reporting
        run_result.is_pass = is_pass
        run_result.save(update_fields=["status","is_pass"])
        merge_all_report_log(path, run_type)
        run_result.status = RunResult.RunStatus.Reporting_Done
        run_result.save(update_fields=["status"])


class RunResult(models.Model):
    objects: models.QuerySet

    class RunStatus(models.IntegerChoices):
        Init = 0, "初始化"
        Running = 1, "正在执行"
        Reporting = 2, "正在输出报告"
        Done = 3, "执行完毕"
        Reporting_Done = 4, "报告输出完毕"
        Error = -1, "执行出错"

    suite = models.ForeignKey(
        verbose_name="测试套件id", to=Suite, on_delete=models.CASCADE
    )

    path = models.CharField(verbose_name="用例路径", max_length=256)
    is_pass = models.BooleanField(verbose_name="是否通过", default=False)
    status = models.IntegerField(
        verbose_name="用例状态", choices=RunStatus, default=RunStatus.Init
    )

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_datetime = models.DateTimeField(verbose_name="更新时间", auto_now=True)

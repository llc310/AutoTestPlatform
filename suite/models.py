

from django.db import models

from case_api.models import Case as CaseAPI
from case_ui.models import Case as CaseUI
from project.models import Project


# Create your models here.
class Suite(models.Model):
    objects: models.QuerySet

    name = models.CharField(verbose_name="套件名称",max_length=32)
    project = models.ForeignKey(verbose_name="项目id",to=Project,on_delete=models.CASCADE)
    description = models.CharField(verbose_name="套件名称",blank=True,max_length=32)

    case_ui_list = models.ManyToManyField(verbose_name="UI测试用例id",to=CaseUI)
    case_api_list = models.ManyToManyField(verbose_name="接口测试用例id",to=CaseAPI)

    def case_ui_count(self):
        return self.case_ui_list.all().count()

    def case_api_count(self):
        return self.case_api_list.all().count()

    def run(self):
        ...

class RunResult(models.Model):
    objects: models.QuerySet

    class RunStatus(models.IntegerChoices):
        Init = 0, "初始化"
        Ready = 1, "准备开始"
        Running = 2,"正在执行"
        Reporting = 3,"正在输出报告"
        Done = 4, "执行完毕"
        Error = -1, "执行出错"

    suite = models.ForeignKey(verbose_name="测试套件id",to=Suite,on_delete=models.CASCADE)

    path = models.CharField(verbose_name="用例路径",max_length=256)
    is_pass = models.BooleanField(verbose_name="是否通过",default=False)
    status = models.IntegerField(verbose_name="用例状态",choices=RunStatus)

    create_datetime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_datetime = models.DateTimeField(verbose_name="更新时间",auto_now=True)

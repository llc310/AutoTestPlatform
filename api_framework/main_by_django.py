import os
import shutil
import subprocess

import pytest
import sys

import time

request_id = sys.argv[-1]
sys.argv = sys.argv[:-2]
sys.path.append(r"E:\Pycharm-WorkSpace\AutoTest01")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoTest01.settings")
from django import setup

setup()
from case.models import RunResult

res_code = pytest.main()
result: RunResult = RunResult.objects.get(id=request_id)

if res_code == pytest.ExitCode.OK:
    result.status = RunResult.RunStatus.Done
    result.is_pass = True
    result.save()
    print("测试用例执行结束")
else:
    result.status = RunResult.RunStatus.Error
    result.save()
    print("测试用例执行失败")

res_code = subprocess.run(
    "allure generate ./temps -o ./report --clean", shell=True, check=True
)

if res_code == pytest.ExitCode.OK:
    result.status = RunResult.RunStatus.Reporting
    result.save()
    print("测试用例报告生成成功")

shutil.move(
    "log/frame.log",
    "log/frame_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".log",
)

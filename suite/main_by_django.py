import os
import shutil
import subprocess

import pytest
import sys

import time

id = sys.argv[-1]
sys.argv = sys.argv[:-2]

sys.path.append(r"E:\Pycharm-WorkSpace\AutoTestPlatform")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoTestPlatform.settings")
from django import setup
setup()

from suite.models import RunResult
run_result = RunResult.objects.get(id=id)
run_result.status = RunResult.RunStatus.Running
run_result.save()

res_code = pytest.main()

if res_code == pytest.ExitCode.OK:
    run_result.status = RunResult.RunStatus.Done
    run_result.is_pass = True
    run_result.save()
    print("测试用例执行结束")
else:
    run_result.status = RunResult.RunStatus.Error
    run_result.save()
    print("测试用例执行失败")

run_result.status = RunResult.RunStatus.Reporting
run_result.save()
run_return = subprocess.run(
    "allure generate ./temps -o ./report --clean", shell=True, check=True
)

if run_return.returncode:
    run_result.status = RunResult.RunStatus.Reporting_Done
    run_result.save()
    print("测试用例报告生成成功")
else:
    run_result.status = RunResult.RunStatus.Error
    run_result.save()
    print("测试用例报告生成失败")

shutil.move(
    "log/frame.log",
    "log/frame_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".log",
)

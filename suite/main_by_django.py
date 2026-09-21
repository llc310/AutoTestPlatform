import os
import shutil
import subprocess
from pathlib import Path

import pytest
import sys

import time



type = sys.argv[-1]
sys.argv = sys.argv[:-2]

id = sys.argv[-1]
sys.argv = sys.argv[:-2]

sys.path.append(r"E:\Pycharm-WorkSpace\AutoTestPlatform")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoTestPlatform.settings")
from django import setup

setup()

allure_dir = Path.cwd().parent / f"temps_{type}"
allure_dir.mkdir(parents=True, exist_ok=True)
log_dir = Path.cwd().parent / "log"
log_dir.mkdir(parents=True,exist_ok=True)
log_file = log_dir / f"frame_{type}.log"

from suite.models import RunResult

run_result = RunResult.objects.get(id=id)
run_result.status = RunResult.RunStatus.Running
run_result.save()

res_code = pytest.main([
    "--alluredir", allure_dir,
     "--log-file", log_file,
     "--log-file-level", "INFO",
    *sys.argv
])

if res_code == pytest.ExitCode.OK:
    run_result.status = RunResult.RunStatus.Done
    run_result.is_pass = True
    run_result.save()
    print("测试用例执行结束")
else:
    run_result.status = RunResult.RunStatus.Error
    run_result.save()
    print("测试用例执行失败")

import os
import shutil
import sys
from pathlib import Path

import pytest

type = sys.argv[-1]
sys.argv = sys.argv[:-2]

id = sys.argv[-1]
sys.argv = sys.argv[:-2]

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoTestPlatform.settings")
from django import setup

setup()

allure_dir = Path.cwd().parent / f"temps_{type}"
if allure_dir.exists():
    shutil.rmtree(allure_dir)
allure_dir.mkdir(parents=True, exist_ok=True)
log_dir = Path.cwd().parent / "log"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"frame_{type}.log"

from suite.models import RunResult

run_result = RunResult.objects.get(id=id)
run_result.status = RunResult.RunStatus.Running
run_result.save(update_fields=["status"])

res_code = pytest.main(
    [
        "--alluredir",
        str(allure_dir),
        "--log-file",
        str(log_file),
        "--log-file-level",
        "INFO",
        sys.argv[-1],
    ]
)

sys.exit(res_code)
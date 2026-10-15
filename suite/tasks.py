import os
import shutil
import subprocess
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

from AutoTestPlatform import settings

pool = ThreadPoolExecutor(max_workers=3)


def run_case(path, id, type,base_url):
    if type == "api":
        print(f"创建进程执行接口框架:{time.time()}")
        case_path = f"{settings.BASE_DIR}/api_framework/testcases/test_all_case.py"
    elif type == "ui":
        print(f"创建进程执行UI框架:{time.time()}")
        case_path = f"{settings.BASE_DIR}/selenium_framework/testcases/test_all_case.py"
    else:
        return 3
    run_path = f"{settings.BASE_DIR}/suite/main_by_django.py"
    env = {**os.environ,
           "BASE_URL": base_url,
           "RESULT_ID": str(id),
           "RUN_TYPE": type
           }
    p = subprocess.run(
        [sys.executable, run_path, case_path],
        env = env,
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(p.stdout.decode("gbk", errors="replace"))
    print(p.stderr.decode("gbk", errors="replace"))
    return p.returncode


def merge_all_report_log(result_path, run_type=("api", "ui")):
    temps_dirs = [str(result_path / "temps_api"), str(result_path / "temps_ui")]
    report_dir = result_path / "report"
    subprocess.run(
        ["allure", "generate", *temps_dirs, "-o", report_dir, "--clean"],
        check=True,
        shell=True,
    )

    log_dir = result_path / "log"
    log_file = result_path / "frame.log"
    with open(file=log_file, mode="w", encoding="utf-8") as f:
        for type in run_type:
            part = log_dir / f"frame_{type}.log"
            f.write(f"\n========== {type} log ==========\n")
            if part.exists():
                f.write(part.read_text(encoding="utf-8", errors="replace"))


def clean_file(result_path: Path):
    yaml_dir = result_path / "yaml"
    yaml_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("api", "ui"):
        dir = result_path / sub
        for yaml_file in dir.glob("test*.yaml"):
            shutil.move(yaml_file, yaml_dir / yaml_file.name)

    for item in result_path.iterdir():
        if item.name in ("report", "yaml", "frame.log"):
            continue
        if item.is_dir():
            shutil.rmtree(item, True)
        else:
            item.unlink(True)


def create_artifacts(result_id, result_path):
    path = settings.BASE_DIR / "zip" / f"result_{result_id}"
    try:
        path.mkdir(parents=True, exist_ok=True)
        zip_path = shutil.make_archive(
            f"{path}/artifacts_result_{result_id}", "zip", result_path
        )
        shutil.move(zip_path, result_path / "artifacts.zip")
    finally:
        shutil.rmtree(path, True)


def run_by_cron(id):
    from suite.models import Suite

    suite = Suite.objects.get(id=id)
    suite.run()

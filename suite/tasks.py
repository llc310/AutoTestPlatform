import subprocess
import sys
import time
from concurrent.futures.process import ProcessPoolExecutor


from AutoTestPlatform import settings


pool = ProcessPoolExecutor(max_workers=3)


def run_api_case(path, id, type):
    print(f"创建进程执行接口框架:{time.time()}")
    run_path = f"{settings.BASE_DIR}/suite/main_by_django.py"
    case_path = f"{settings.BASE_DIR}/api_framework/testcases/test_all_case.py"
    p = subprocess.run(
        [sys.executable, run_path, case_path, "result_id", str(id), "type", type],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(p.stdout.decode("gbk", errors="replace"))
    print(p.stderr.decode("gbk", errors="replace"))
    return p.returncode


def run_ui_case(path, id, type):
    print(f"创建进程执行UI框架:{time.time()}")
    run_path = f"{settings.BASE_DIR}/suite/main_by_django.py"
    case_path = f"{settings.BASE_DIR}/selenium_framework/testcases/test_all_case.py"
    p = subprocess.run(
        [sys.executable, run_path, case_path, "result_id", str(id), "type", type],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(p.stdout.decode("gbk", errors="replace"))
    print(p.stderr.decode("gbk", errors="replace"))
    return p.returncode


def merge_all_report_log(path, run_type=("api", "ui")):
    temps_dirs = [str(path / "temps_api"), str(path / "temps_ui")]
    report_dir = path / "report"
    subprocess.run(
        ["allure", "generate", *temps_dirs, "-o", report_dir, "--clean"],
        check=True,
        shell=True,
    )

    log_dir = path / "log"
    log_file = (
        path / f"log/frame_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.log"
    )
    with open(file=log_file, mode="w", encoding="utf-8") as f:
        for type in run_type:
            part = log_dir / f"frame_{type}.log"
            f.write(f"\n========== {type} log ==========\n")
            if part.exists():
                f.write(part.read_text(encoding="utf-8", errors="replace"))


def run_by_cron(id):
    from suite.models import Suite
    suite = Suite.objects.get(id=id)
    suite.run()
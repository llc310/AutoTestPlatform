import subprocess
import sys
from concurrent.futures.process import ProcessPoolExecutor

import time

pool = ProcessPoolExecutor(max_workers=3)

def run_api_case(path,id):
    print(f"创建进程执行接口框架:{time.time()}")
    run_path = "suite/main_by_django.py"
    case_path = "api_framework/testcases/test_all_case.py"
    p = subprocess.run([sys.executable, run_path, case_path, case_path, "result_id", str(id)],
                       cwd=path.parent.parent,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    try:
        print(p.stdout.decode("gbk", errors="replace"))
        print(p.stderr.decode("gbk", errors="replace"))
    except UnicodeDecodeError:
        print(p.stdout.decode("gbk", errors="replace"))
        print(p.stderr.decode("gbk", errors="replace"))
import shutil
import subprocess
import time

import pytest

# 程序主入口
if __name__ == "__main__":
    pytest.main(["--alluredir", "./temps", "--clean-alluredir"])
    subprocess.run(
        "allure generate ./temps -o ./report --clean", shell=True, check=True
    )
    shutil.move(
        "log/frame.log",
        "log/frame_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".log",
    )

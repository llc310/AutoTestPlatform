import pytest
import settings
from commons.db_util import DBUtil
from commons.driver_manager import DriverManager


# 清理日志
@pytest.fixture(scope="class", autouse=True)
def clear_log():
    log_list = list(settings.LOG_DIR.glob("*.log"))
    while len(log_list) > settings.LOG_FILE_MAX_NUM:
        if log_list[0].name == "frame.log":
            log_list.pop(1)
            log_list[1].unlink(missing_ok=True)
        else:
            log_list.pop(0)
            log_list[0].unlink(missing_ok=True)


# 获取浏览器驱动对象
@pytest.fixture(scope="function")
def get_webdriver():
    driver_manger = DriverManager()
    driver = driver_manger.driver
    driver.get(settings.BASE_URL)
    yield driver
    driver_manger.quit_driver()


# 创建data文件夹
@pytest.fixture(scope="class", autouse=True)
def create_data_dir():
    settings.TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)


db = 21313
# # 数据库操作
# @pytest.fixture(scope="session",autouse=True)
# def get_db():
#     yield
#     db.close()

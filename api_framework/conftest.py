import pytest
import settings
from commons.db_util import DBUtil
from commons.request_util import RequestUtil
from commons.yaml_util import YamlUtil


# 创建关联参数文件
@pytest.fixture(scope="session", autouse=True)
def create_extract_file():
    YamlUtil.clean_yaml(settings.EXTRACT_FILE)


# 清理日志
@pytest.fixture(scope="session", autouse=True)
def clear_log():
    log_list = list(settings.LOG_DIR.glob("*.log"))
    while len(log_list) > settings.LOG_FILE_MAX_NUM:
        if log_list[0].name == "frame.log":
            log_list.pop(1)
            log_list[1].unlink(missing_ok=True)
        else:
            log_list.pop(0)
            log_list[0].unlink(missing_ok=True)


# 让每个用例使用不同的session
@pytest.fixture(scope="function")
def get_request_util():
    yield RequestUtil()


db = DBUtil()


# 数据库操作
@pytest.fixture(scope="session", autouse=True)
def get_db():
    yield
    db.close()

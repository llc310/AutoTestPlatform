from pathlib import Path

# 项目配置信息文件
# 项目基础路径
BASE_DIR = Path(__file__).parent
# 测试用例文件夹路径：跟随当前工作目录（cwd = 传入的用例文件夹）
TEST_CASE_DIR = Path.cwd()
# 运行测试用例文件（可选，目录下没有该文件时自动运行全部用例）
RUN_CASE_FILE = TEST_CASE_DIR / "run_case.yaml"
# 关联参数文件路径：每进程独立
EXTRACT_FILE = Path.cwd() / "extract.yaml"
# LOG文件夹路径：每进程独立
LOG_DIR = Path.cwd().parent / "log"
# LOG文件最多记录数
LOG_FILE_MAX_NUM = 4

# 项目网址路径
BASE_URL = "http://127.0.0.1:8888"

# 项目数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "3526823227llc"
DB_DATABASE = "vue_api_server"

# Allure报告信息
ALLURE_EPIC = "博客项目"

if __name__ == "__main__":
    print(BASE_DIR)
    print(Path("login/test_login_success.yaml").stem)

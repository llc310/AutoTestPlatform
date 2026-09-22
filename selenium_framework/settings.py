from pathlib import Path

# 项目前台网址
BASE_URL = "https://uc-uat.ahsjs.com/dologin.htm"
# 项目基础路径
BASE_DIR = Path(__file__).parent
# 测试数据路径
TEST_DATA_DIR = Path.cwd() / "data"
# Cookie信息文件路径
COOKIE_DIR = TEST_DATA_DIR / "cookies.yaml"
# 文件测试数据路径
TEST_CASE_DIR = Path.cwd()
# 运行测试用例文件
RUN_CASE_FILE = TEST_CASE_DIR / "run_case.yaml"

# 浏览器类型
BROWSER_TYPE = "CHROME"

# 浏览器程序路径
BROWSER_PATH = BASE_DIR / "driverobjects"

# 浏览器隐式等待时间
IMPLICITLY_WAIT_TIME = 10

# 浏览器显示等待时间
EXPLICIT_WAIT_TIME = 2

# 测试账号密码
PASSWORD = "123456a"

# LOG文件夹路径
LOG_DIR = BASE_DIR / "log"
# LOG文件最多记录数
LOG_FILE_MAX_NUM = 4

# 项目数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "3526823227llc"
DB_DATABASE = "vue_api_server"

# Allure报告信息
ALLURE_EPIC = "博客项目"

# 超级鹰接口信息
CHAOJIYING_USERNAME = "20260823yhchaej6"
CHAOJIYING_PASSWORD = "3526823227llc"
CHAOJIYING_ID = "983412"
CHAOJIYING_CODETYPE = 1902

if __name__ == "__main__":
    print(TEST_DATA_DIR)

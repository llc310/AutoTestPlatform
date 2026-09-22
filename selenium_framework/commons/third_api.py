# 调用其他软件的接口
import logging

import requests
from settings import (BASE_DIR, CHAOJIYING_CODETYPE, CHAOJIYING_ID,
                      CHAOJIYING_PASSWORD, CHAOJIYING_USERNAME)

from selenium_framework.settings import TEST_DATA_DIR


# 超级鹰验证码识别接口
def get_img_code():
    url = "https://upload.chaojiying.net/Upload/Processing.php"
    data = {
        "user": CHAOJIYING_USERNAME,
        "pass": CHAOJIYING_PASSWORD,
        "softid": CHAOJIYING_ID,
        "codetype": CHAOJIYING_CODETYPE,
    }
    files = {"userfile": open(file=TEST_DATA_DIR / "verify.png", mode="rb")}
    response = requests.post(url=url, data=data, files=files)
    json_data = response.json()
    if json_data["err_no"] == 0:
        return json_data["pic_str"]
    else:
        logging.error("识别验证码失败")

import json
import logging

import requests
import settings


# 发送接口请求的工具类
class RequestUtil:
    def __init__(self):
        self.session = requests.session()

    def send_all_requests(self, case):
        request_data = dict(case.requests)
        request_data["url"] = settings.BASE_URL + request_data["url"]
        logging.info(
            "请求数据\n%s",
            json.dumps(request_data, indent=4, ensure_ascii=False, default=str),
        )
        response = self.session.request(**request_data)
        try:
            logging.info(
                "响应数据\n%s",
                json.dumps(response.json(), indent=4, ensure_ascii=False, default=str),
            )
        except ValueError:
            logging.info("响应数据\n%s", response.text)
        # logging.info(f"请求数据为:{str(request_data)}")
        # try:
        #     logging.info(f"响应数据为:{response.json()}")
        # except ValueError:
        #     logging.info(f"响应数据为:{response.text}")
        return response

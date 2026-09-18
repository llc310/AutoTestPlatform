import logging
import re
from copy import deepcopy

from commons.yaml_util import YamlUtil
from jsonpath import jsonpath


class ExtractUtil:
    @classmethod
    def load_extract_params(cls, response, extract_list):
        copy_response = deepcopy(response)
        try:
            copy_response.json = copy_response.json()
        except ValueError:
            copy_response.json = {"msg": "这个响应没有json数据"}
        params = {}
        for param in extract_list:
            key, value = cls.__get_param(copy_response, **param)
            if value:
                params[key] = value
                logging.info(f"提取接口关联参数{key}:{value}")
        YamlUtil.write_extract_params(params)

    @classmethod
    def __get_param(cls, response, key, attr, expr):
        if attr == "json":
            result = jsonpath(response.json, expr)
            if result:
                value = result[0]
            else:
                value = None
        else:
            value = re.findall(expr, getattr(response, attr))
        return key, value

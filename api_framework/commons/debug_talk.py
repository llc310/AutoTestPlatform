import random

import settings
from commons.yaml_util import YamlUtil


# 测试用例使用函数类
class DebugTalk:
    @classmethod
    def random_int(cls, start=0, end=100):
        return random.randint(start, end)

    @classmethod
    def random_str_int(cls, start=0, end=100):
        return "'" + str(random.randint(start, end)) + "'"

    @classmethod
    def random_str(cls, k=10):
        return "".join(
            random.choices("abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=k)
        )

    @classmethod
    def read_extract(cls, key):
        params = YamlUtil.read_yaml(settings.EXTRACT_FILE)
        return params[key]

    @classmethod
    def read_extract_str(cls, key):
        params = YamlUtil.read_yaml(settings.EXTRACT_FILE)
        return "'" + str(params[key]) + "'"

    @classmethod
    def write_extract(cls, key, value):
        YamlUtil.write_extract_params({key: value})


if __name__ == "__main__":
    print(DebugTalk.random_int(end=10))
    print(DebugTalk.read_extract("msg"))

import random

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
    def write_extract(cls, key, value):
        YamlUtil.write_extract_params({key: value})


if __name__ == "__main__":
    print(DebugTalk.random_int(end=10))

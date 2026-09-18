import settings
import yaml


# 操作YAML文件的工具类
class YamlUtil:
    @classmethod
    def read_yaml(cls, yaml_path):
        try:
            with open(file=yaml_path, mode="r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}

    @classmethod
    def write_yaml(cls, yaml_path, data):
        with open(file=yaml_path, mode="w+", encoding="utf-8") as f:
            yaml.safe_dump(data, f)

    @classmethod
    def clean_yaml(cls, yaml_path):
        with open(file=yaml_path, mode="w", encoding="utf-8"):
            return

    @classmethod
    def write_extract_params(cls, params_dict):
        old_params_dict = cls.read_yaml(settings.EXTRACT_FILE)
        old_params_dict.update(params_dict)
        cls.write_yaml(settings.EXTRACT_FILE, old_params_dict)


if __name__ == "__main__":
    data1 = {"token": "123124214", "msg": "fasfdadsfaf"}
    YamlUtil.write_yaml(settings.EXTRACT_FILE, data1)
    print(YamlUtil.read_yaml(settings.EXTRACT_FILE))

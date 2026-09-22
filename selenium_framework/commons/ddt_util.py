import re
from copy import deepcopy

import settings
import yaml
from commons.debug_talk import DebugTalk
from commons.yaml_util import YamlUtil

# 实现数据驱动测试的工具文件


# 读取测试用例
def load_case(yaml_path):
    return load_parametrize(yaml_path)


# 读取参数化
def load_parametrize(yaml_path):
    case_list = YamlUtil.read_yaml(yaml_path)
    if len(case_list) == 1:
        if "parametrize" in case_list[0].keys():
            return parametrize_single_case(case_list[0])
        else:
            return single_case(case_list)
    else:
        if any("parametrize" in case for case in case_list):
            return parametrize_business_case(case_list)
        else:
            return business_case(case_list)


# 读取函数
def load_function(case: dict):
    return hot_load(case)


# 加载调用函数
def hot_load(case):
    expr = r"\$\{(.*?)\((.*?)\)\}"
    case_str: str = yaml.safe_dump(case, allow_unicode=True)
    params = re.findall(expr, case_str)
    for param in params:
        old_value = "${" + param[0] + "(" + param[1] + ")}"
        function = getattr(DebugTalk, param[0])
        if param[1] == "":
            new_value = function()
        else:
            arguments = param[1].split(",")
            for index in range(len(arguments)):
                argument = arguments[index]
                pattern = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)$")
                if pattern.fullmatch(argument):
                    if argument.isdigit():
                        arguments[index] = int(argument)
                    else:
                        arguments[index] = float(argument)
            new_value = function(*arguments)
        case_str = case_str.replace(old_value, str(new_value))
        # if isinstance(new_value,str) and new_value.isdigit():
        #     case_str = case_str.replace(old_value,"'" + str(new_value) + "'")
        # else:
        #     case_str = case_str.replace(old_value, str(new_value))
    return yaml.safe_load(case_str)


# 读取单功能测试用例
def single_case(case_list):
    return case_list, [case_list[0]["title"]]


# 读取参数化的单功能测试用例
def parametrize_single_case(case_dict: dict):
    parametrize_dict: dict = case_dict["parametrize"]
    value_list = []
    name_list = []
    flag = True
    for key, value in parametrize_dict.items():
        if flag:
            for count in range(len(value)):
                new_case = deepcopy(case_dict)
                new_case.pop("parametrize")
                value_list.append(new_case)
            flag = False
        if key == "title":
            name_list = value
        for index in range(len(value)):
            value_list[index] = replace_parametrize(
                value_list[index], key, value[index]
            )
    return value_list, name_list


# 读取业务流程用例
def business_case(case_list):
    return [case_list], [case_list[-1]["title"]]


# 读取参数化的业务流程用例
def parametrize_business_case(case_list: list):
    value_list = []
    parametrize_dict = {}
    for index in range(len(case_list)):
        if "parametrize" in case_list[index]:
            single_value_list, name_list = parametrize_single_case(case_list[index])
            parametrize_dict[index] = single_value_list
    for count in range(len(single_value_list)):
        business_case = []
        for index in range(len(case_list)):
            if index in parametrize_dict:
                business_case.append(parametrize_dict[index][count])
            else:
                business_case.append(case_list[index])
        value_list.append(business_case)
    return value_list, name_list


# 替换参数化的值
def replace_parametrize(case: dict, key: str, value):
    case_str = yaml.safe_dump(case, allow_unicode=True)
    expr = "$parametrize{" + key + "}"
    if isinstance(value, str) and value.isdigit():
        value = "'" + value + "'"
    case_str = case_str.replace(expr, str(value))
    return yaml.safe_load(case_str)


if __name__ == "__main__":
    case_list = settings.TEST_CASE_DIR.glob("smoke/*ddt*")
    for case in case_list:
        value_list, name_list = load_case(case)
        for value in value_list:
            print(value)
        print(name_list)

import logging
from copy import deepcopy

import jsonpath

from conftest import db


# 接口断言工具类
class AssertUtil:
    @classmethod
    def assert_all(cls, response, assert_dict: dict):
        copy_response = deepcopy(response)
        try:
            copy_response.json = copy_response.json()
        except ValueError:
            copy_response.json = {"msg": "这个响应没有json数据"}
        for assert_key in assert_dict.keys():
            match assert_key:
                case "equals":
                    cls.__assert_equals(copy_response, assert_dict["equals"])
                case "contains":
                    cls.__assert_contains(copy_response, assert_dict["contains"])
                case "db_equals":
                    cls.assert_db_equals(assert_dict["db_equals"])
                case "db_contains":
                    cls.assert_db_contains(assert_dict["db_contains"])

    @classmethod
    def __assert_equals(cls, response, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result[0]
            actual_result = cls.__get_actual_result(response, assert_result)
            logging.info(
                f"响应断言{assert_result[1]}字段相等:实际结果'{actual_result}'==预期结果'{expected_result}'"
            )
            assert actual_result == expected_result

    @classmethod
    def __assert_contains(cls, response, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result[0]
            actual_result = cls.__get_actual_result(response, assert_result)
            logging.info(
                f"响应断言{assert_result[1]}字段包含:实际结果'{actual_result}'in预期结果'{expected_result}'"
            )
            assert actual_result in expected_result

    @classmethod
    def __get_actual_result(cls, response, assert_result):
        if assert_result[1] == "json":
            actual_result = jsonpath.jsonpath(response.json, assert_result[2])[0]
        else:
            actual_result = getattr(response, assert_result[1])
        return actual_result

    @classmethod
    def assert_db_equals(cls, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result[0]
            actual_result = cls.__get_db_actual_result(assert_result)
            logging.info(
                f"数据库断言{assert_result[1]}字段相等:实际结果'{actual_result}'==预期结果'{expected_result}'"
            )
            assert actual_result == expected_result

    @classmethod
    def assert_db_contains(cls, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result[0]
            actual_result = cls.__get_db_actual_result(assert_result)
            logging.info(
                f"数据库断言{assert_result[1]}字段包含:实际结果'{actual_result}'in预期结果'{expected_result}'"
            )
            assert actual_result in expected_result

    @classmethod
    def __get_db_actual_result(cls, assert_result):
        result = db.execute_sql(assert_result[1])
        if isinstance(result, list):
            if len(result) > 1:
                return True
            else:
                return result[assert_result[2]]
        return result

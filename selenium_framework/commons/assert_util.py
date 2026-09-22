import logging

from commons.kdt import KeyWord

from conftest import db


# 接口断言工具类
class AssertUtil:
    @classmethod
    def assert_all(cls, driver, assert_dict: dict):
        for assert_key in assert_dict.keys():
            match assert_key:
                case "equals":
                    cls.__assert_equals(driver, assert_dict["equals"])
                case "contains":
                    cls.__assert_contains(driver, assert_dict["contains"])
                case "db_equals":
                    cls.assert_db_equals(assert_dict["db_equals"])
                case "db_contains":
                    cls.assert_db_contains(assert_dict["db_contains"])

    @classmethod
    def __assert_equals(cls, driver, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result["expected_result"]
            actual_result = cls.__get_actual_result(
                driver, assert_result["actual_result"]
            )
            logging.info(
                f"断言相等:实际结果'{actual_result}'==预期结果'{expected_result}'"
            )
            assert actual_result == expected_result

    @classmethod
    def __assert_contains(cls, driver, assert_list: list):
        for assert_result in assert_list:
            expected_result = assert_result[0]
            actual_result = cls.__get_actual_result(
                driver, assert_result["actual_result"]
            )
            logging.info(
                f"断言字段包含:实际结果'{actual_result}'in预期结果'{expected_result}'"
            )
            assert actual_result in expected_result

    @classmethod
    def __get_actual_result(cls, driver, actual_result_dict):
        keyword = getattr(KeyWord(driver), actual_result_dict["keyword"])
        if not actual_result_dict["locator"]:
            if actual_result_dict["args"]:
                args: list = actual_result_dict["args"]
                logging.info(f"{keyword.__name__}({', '.join(repr(a) for a in args)})")
                return keyword(*args)
            else:
                return keyword()
        locator = tuple(actual_result_dict["locator"])
        if "args" in actual_result_dict.keys():
            args = actual_result_dict["args"]
            logging.info(
                f"{keyword.__name__}({locator, ', '.join(repr(a) for a in args)})"
            )
            return keyword(locator, *args)
        else:
            logging.info(f"{keyword.__name__}({locator})")
            return keyword(locator)

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

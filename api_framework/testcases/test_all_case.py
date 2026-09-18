import logging
from pathlib import Path

import allure
import pytest
import settings
from commons.ddt_util import load_case, load_function
from commons.main_util import stand_case_flow
from commons.model import verify_case
from commons.yaml_util import YamlUtil


# 存放所有测试用例
@allure.epic(settings.ALLURE_EPIC)
class TestAllCase: ...


def create_test_case(yaml_path):
    case_value, case_name = load_case(yaml_path)

    @pytest.mark.parametrize("caseinfo", case_value, ids=case_name)
    def function(self, caseinfo, get_request_util):
        if isinstance(caseinfo, dict):
            try:
                caseinfo = load_function(caseinfo)
                case_model = verify_case(caseinfo)
                if case_model:
                    set_allure_log(case_model)
                    stand_case_flow(get_request_util, case_model)
            finally:
                logging.info("----单功能测试用例执行结束----\n")
        else:
            try:
                logging.info("----运行业务流程测试用例----")
                for case in caseinfo:
                    case = load_function(case)
                    case_model = verify_case(case)
                    if case_model:
                        set_allure_log(case_model)
                        stand_case_flow(get_request_util, case_model)
            finally:
                logging.info("----业务流程测试用例执行结束----\n")

    return function


def set_allure_log(case_model):
    logging.info(f"feature:{case_model.feature}")
    logging.info(f"story:{case_model.story}")
    logging.info(f"title:{case_model.title}")
    logging.info(f"description:{case_model.description}")
    allure.dynamic.feature(case_model.feature)
    allure.dynamic.story(case_model.story)
    allure.dynamic.description(case_model.description)


# 运行测试用例列表
run_case_list = YamlUtil.read_yaml(settings.RUN_CASE_FILE)
if isinstance(run_case_list, dict):
    run_case_list = [None]
# 长度为0默认执行所有测试用例
if not run_case_list[0]:
    logging.info("====运行所有测试用例====")
    for testcase in settings.TEST_CASE_DIR.glob("*.yaml"):
        if "extract.yaml" in str(testcase):
            continue
        logging.info(f"文件名为{testcase}")
        setattr(TestAllCase, testcase.stem, create_test_case(testcase))
    logging.info("====所有测试用例执行结束====\n")
else:
    logging.info("====运行指定测试用例====")
    for testcase in run_case_list:
        path = Path(settings.TEST_CASE_DIR / testcase)
        if ".yaml" in testcase:
            logging.info(f"文件名为{path}")
            setattr(TestAllCase, path.stem, create_test_case(path))
        else:
            logging.info(f"运行{testcase}文件夹中的所有测试用例")
            for case in path.glob("*.yaml"):
                logging.info(f"文件名为{case}")
                setattr(TestAllCase, case.stem, create_test_case(case))
    logging.info("====指定测试用例执行结束====\n")

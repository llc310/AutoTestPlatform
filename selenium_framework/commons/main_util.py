import logging

from commons.assert_util import AssertUtil
from commons.model import CaseModel
from commons.step_util import StepUtil


# 标准用例执行流程
def stand_case_flow(driver, case: CaseModel):
    StepUtil.run_step(driver, case.step)

    if case.validate:
        try:
            AssertUtil.assert_all(driver, case.validate)
        except Exception:
            logging.exception(
                "断言阶段失败 | title=%s | validate=%s", case.title, case.validate
            )
            raise

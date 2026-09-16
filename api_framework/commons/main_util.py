from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model import CaseModel
from commons.request_util import RequestUtil


# 标准用例执行流程
def stand_case_flow(request_util: RequestUtil, case: CaseModel):
    # 发送接口请求
    response = request_util.send_all_requests(case)
    # 对接口响应进行断言
    if case.validate:
        AssertUtil.assert_all(response, case.validate)
    # 提取接口参数
    if case.extract:
        ExtractUtil.load_extract_params(response, case.extract)

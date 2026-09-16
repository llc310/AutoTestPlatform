import logging
from dataclasses import dataclass, field
from typing import Dict, List


# 测试用例模板类
@dataclass
class CaseModel:
    # 必填
    feature: str
    story: str
    title: str
    description: str
    requests: dict

    # 非必填
    parametrize: Dict = field(default_factory=dict)
    extract: List = field(default_factory=list)
    validate: Dict = field(default_factory=dict)


def verify_case(case):
    try:
        return CaseModel(**case)
    except Exception:
        logging.error("测试用例编写不符合模板规范")
        return None

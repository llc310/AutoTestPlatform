import logging

from commons.kdt import KeyWord


class StepUtil:
    @classmethod
    def run_step(cls, driver, action_list: list):
        for index, action in enumerate(action_list, start=1):
            logging.info("第 %d 步：%s", index, action.get("action"))
            try:
                keyword = getattr(KeyWord(driver), action.get("keyword"))
                locator = action.get("locator")
                args = action.get("args") or []

                # 拼出真实要传给关键字的位置参数：locator 在前，args 在后
                call_args = [tuple(locator)] if locator else []
                call_args.extend(args)
                logging.info(
                    "%s(%s)", keyword.__name__, ", ".join(repr(a) for a in call_args)
                )
                keyword(*call_args)
            except Exception:
                logging.exception(
                    "步骤执行失败 | 第 %d 步 | action=%s | keyword=%s | locator=%s | args=%s",
                    index,
                    action.get("action"),
                    action.get("keyword"),
                    action.get("locator"),
                    action.get("args"),
                )
                raise

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
                args = action.get("args")

                if not locator and not args:
                    logging.info(f"{keyword.__name__}()")
                    keyword()
                elif not locator:
                    logging.info(
                        f"{keyword.__name__}({', '.join(repr(a) for a in args)})"
                    )
                    keyword(*args)
                elif not args:
                    logging.info(f"{keyword.__name__}({tuple(locator)})")
                    keyword(tuple(locator))
                else:
                    logging.info(
                        f"{keyword.__name__}({tuple(locator), ', '.join(repr(a) for a in args)})"
                    )
                    keyword(tuple(locator), *args)
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

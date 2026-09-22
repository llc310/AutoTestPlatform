import logging

from commons.kdt import KeyWord


class StepUtil:
    @classmethod
    def run_step(cls, driver, action_list: list):
        for action in action_list:
            logging.info(action["action"])
            keyword = getattr(KeyWord(driver), action["keyword"])
            if not action["locator"]:
                if action["args"]:
                    args: list = action["args"]
                    logging.info(
                        f"{keyword.__name__}({', '.join(repr(a) for a in args)})"
                    )
                    keyword(*args)
                    continue
                else:
                    logging.info(f"{keyword.__name__}()")
                    keyword()
            locator = tuple(action["locator"])
            if "args" in action.keys():
                args = action["args"]
                logging.info(
                    f"{keyword.__name__}({locator,', '.join(repr(a) for a in args)})"
                )
                keyword(locator, *args)
                continue
            logging.info(f"{keyword.__name__}({locator})")
            keyword(locator)

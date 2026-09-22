import settings
from commons.third_api import get_img_code
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class KeyWord:
    def __init__(self, driver):
        self.driver = driver

    def __smart_wait_element(self, locator, function, timeout):
        wait_function = getattr(EC, function)
        WebDriverWait(self.driver, timeout).until(wait_function(locator))

    def __smart_wait_alert(self, timeout, function="alert_is_present"):
        wait_function = getattr(EC, function)
        WebDriverWait(self.driver, timeout).until(wait_function())

    # ---------------------------ELEMENT---------------------------
    def find_element(
        self,
        locator,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.__smart_wait_element(locator, function, timeout)
        return self.driver.find_element(*locator)

    def find_elements(
        self,
        locator,
        function="visibility_of_all_elements_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.__smart_wait_element(locator, function, timeout)
        return self.driver.find_elements(*locator)

    def clear(
        self,
        locator,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.find_element(locator, function, timeout).clear()

    def send_keys(
        self,
        locator,
        text,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.clear(locator, function, timeout)
        self.find_element(locator, function, timeout).send_keys(text)

    def click(
        self,
        locator,
        function="element_to_be_clickable",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.find_element(locator, function, timeout).click()

    def text(
        self,
        locator,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        return self.find_element(locator, function, timeout).text

    def save_code_img(
        self,
        locator,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        img_path = settings.TEST_DATA_DIR / "verify.png"
        self.find_element(locator, function, timeout).screenshot(str(img_path))

    def send_code(
        self,
        locator,
        function="visibility_of_element_located",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        self.send_keys(locator, get_img_code(), function, timeout)

    # ---------------------------ALERT---------------------------
    def switch_to_alert(self, timeout=settings.EXPLICIT_WAIT_TIME):
        self.__smart_wait_alert(timeout)
        return self.driver.switch_to.alert

    def alert_text(self, timeout=settings.EXPLICIT_WAIT_TIME):
        return self.switch_to_alert(timeout).text

    def alert_accept(self, timeout=settings.EXPLICIT_WAIT_TIME):
        self.switch_to_alert(timeout).accpet()

    def alert_dismiss(self, timeout=settings.EXPLICIT_WAIT_TIME):
        self.switch_to_alert(timeout).dismiss()

    def alert_send_keys(self, text, timeout=settings.EXPLICIT_WAIT_TIME):
        self.switch_to_alert(timeout).send_keys(text)

    # ---------------------------SELECT---------------------------
    def select_by_index(
        self,
        locator,
        index,
        function="element_to_be_clickable",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        select = Select(self.find_element(locator, function, timeout))
        select.select_by_index(index)

    def select_by_value(
        self,
        locator,
        value,
        function="element_to_be_clickable",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        select = Select(self.find_element(locator, function, timeout))
        select.select_by_value(value)

    def select_by_visible_text(
        self,
        locator,
        text,
        function="element_to_be_clickable",
        timeout=settings.EXPLICIT_WAIT_TIME,
    ):
        select = Select(self.find_element(locator, function, timeout))
        select.select_by_visible_text(text)

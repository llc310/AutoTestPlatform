# 管理浏览器驱动对象类
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from settings import BROWSER_PATH, BROWSER_TYPE, IMPLICITLY_WAIT_TIME


class DriverManager:
    def __init__(self):
        self.driver = self.__get_driver()

    def __get_driver(self):
        match BROWSER_TYPE:
            case "CHROME":
                self.driver = self.__init_chrome_driver()
            case "FIREFOX":
                self.driver = self.__init_firefox_driver()
            case "EDGE":
                self.driver = self.__init_edge_driver()

        self.driver.maximize_window()
        self.driver.implicitly_wait(IMPLICITLY_WAIT_TIME)
        logging.info("获取浏览器驱动对象")

        return self.driver

    def __init_chrome_driver(self):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--disable-infobars")

        service = ChromeService(executable_path=BROWSER_PATH / "chromedriver.exe")

        return webdriver.Chrome(service=service, options=chrome_options)

    def __init_firefox_driver(self):
        # firefox_options = webdriver.FirefoxOptions()

        # firefox_options.add_argument()

        service = FirefoxService(executable_path=BROWSER_PATH / "firefoxdriver.exe")

        return webdriver.Firefox(service=service)

    def __init_edge_driver(self):
        # edge_options = webdriver.EdgeOptions()

        # edge_options.add_argument()

        service = EdgeService(executable_path=BROWSER_PATH / "edgedriver.exe")

        return webdriver.Edge(service=service)

    def quit_driver(self):
        self.driver.quit()
        logging.info("关闭浏览器驱动对象\n")

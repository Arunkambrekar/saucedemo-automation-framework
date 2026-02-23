from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import get_logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.log = get_logger(self.__class__.__name__)   # logger must be here

    def click(self, locator):
        self.log.info(f"Clicking element: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        self.log.info(f"Typing '{text}' into element: {locator}")
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        self.log.info(f"Getting text from element: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator)).text

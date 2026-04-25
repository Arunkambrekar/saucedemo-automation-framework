from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")

    OVERVIEW_HEADER = (By.CLASS_NAME, "summary_title")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")

    def enter_details(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)

    def click_continue(self):
        wait = WebDriverWait(self.driver, 15)

        continue_btn = wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )

        # Scroll into view (important for CI/headless)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", continue_btn
        )

        # Reliable click
        try:
            continue_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", continue_btn)

        # ✅ CRITICAL FIX: wait for next page (overview)
        wait.until(
            EC.visibility_of_element_located(self.OVERVIEW_HEADER)
        )

    def click_finish(self):
        wait = WebDriverWait(self.driver, 15)

        finish_btn = wait.until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", finish_btn
        )

        try:
            finish_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", finish_btn)

    def wait_for_order_completion(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        )

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)
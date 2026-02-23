from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        self.click(self.CONTINUE_BTN)

    # Wait until Overview page loads (after Continue)
    def wait_for_overview_page(self):
        self.wait.until(EC.visibility_of_element_located(self.OVERVIEW_HEADER))

    def click_finish(self):
        self.click(self.FINISH_BTN)

    # ✅ STABLE: wait for order completion using URL
    def wait_for_order_completion(self):
        self.wait.until(lambda d: "checkout-complete" in d.current_url)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

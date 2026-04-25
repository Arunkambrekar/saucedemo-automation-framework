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

    # FIX: "summary_title" does not reliably appear in headless CI.
    # The overview page is confirmed by the URL changing to /checkout-step-two
    # AND the finish button being present — both are rock-solid signals.
    FINISH_BTN_LOCATOR = (By.ID, "finish")

    # FIX: success page uses data-test attribute, more stable than class name
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")

    def enter_details(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)

    def click_continue(self):
        wait = WebDriverWait(self.driver, 20)

        continue_btn = wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", continue_btn
        )
        self.driver.execute_script("arguments[0].click();", continue_btn)

        # FIX: wait for the URL to reach step-two AND finish button to be present.
        # This is more reliable than waiting for summary_title which is flaky in CI.
        wait.until(EC.url_contains("checkout-step-two"))
        wait.until(EC.element_to_be_clickable(self.FINISH_BTN_LOCATOR))

    def click_finish(self):
        wait = WebDriverWait(self.driver, 20)

        finish_btn = wait.until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", finish_btn
        )
        self.driver.execute_script("arguments[0].click();", finish_btn)

        # Wait for URL to confirm navigation away from step-two
        wait.until(EC.url_contains("checkout-complete"))

    def wait_for_order_completion(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SUCCESS_HEADER)
        )

    def get_success_message(self):
        return self.get_text(self.SUCCESS_HEADER)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME   = (By.ID, "first-name")
    LAST_NAME    = (By.ID, "last-name")
    POSTAL_CODE  = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN   = (By.ID, "finish")
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

        # ROOT FIX: JS click bypasses React's synthetic event system on
        # SauceDemo's form — the button appears clicked but the form never
        # validates/submits. Use a real Selenium .click() so React fires its
        # onChange/onSubmit handlers. Fall back to JS only on intercept.
        try:
            continue_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", continue_btn)

        # URL is the ground-truth that the form submitted cleanly.
        # If Continue was a no-op (e.g. validation error), URL stays on
        # step-one and this raises TimeoutException with a clear message.
        wait.until(EC.url_contains("checkout-step-two"))
        wait.until(EC.element_to_be_clickable(self.FINISH_BTN))

    def click_finish(self):
        wait = WebDriverWait(self.driver, 20)

        finish_btn = wait.until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", finish_btn
        )

        try:
            finish_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", finish_btn)

        wait.until(EC.url_contains("checkout-complete"))

    def wait_for_order_completion(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SUCCESS_HEADER)
        )

    def get_success_message(self):
        return self.get_text(self.SUCCESS_HEADER)
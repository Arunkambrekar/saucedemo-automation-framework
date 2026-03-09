from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class DashboardPage(BasePage):

    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")

    def get_all_products(self):
        return self.driver.find_elements(*self.INVENTORY_ITEM)

    def add_first_product_to_cart(self):
        self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTON)
        )
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        # JS click — most reliable, avoids intercept issues
        self.driver.execute_script("arguments[0].click();", buttons[0])

    def add_multiple_products(self, count):
        self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTON)
        )
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        for i in range(count):
            self.driver.execute_script("arguments[0].click();", buttons[i])

    def get_cart_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"

    def click_cart(self):
        self.click(self.CART_BUTTON)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):

    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(),'Add to cart')]")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")

    def get_all_products(self):
        return self.driver.find_elements(*self.INVENTORY_ITEM)

    def add_first_product_to_cart(self):
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        buttons[0].click()

    def get_cart_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"
  
    def click_cart(self):
        self.click(self.CART_BUTTON)

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from config.config import USERNAME, PASSWORD


def reach_checkout(driver):
    wait = WebDriverWait(driver, 20)

    # --- Login ---
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    # Wait for inventory page to be fully interactive
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    ))

    # FIX 1: Use JS click (consistent with the rest of the framework's BasePage.click())
    # to avoid intercept issues in headless CI.
    add_btn = driver.find_element(
        By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']"
    )
    driver.execute_script("arguments[0].click();", add_btn)

    # FIX 2: Wait for the cart badge to confirm the item was registered
    # BEFORE navigating away. This is the key fix — previously we navigated
    # immediately, racing the cart state update in slow CI environments.
    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "shopping_cart_badge")
    ))

    # Navigate directly to cart (avoids flaky cart icon click)
    driver.get("https://www.saucedemo.com/cart.html")

    # Confirm cart page loaded with our item
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))

    # Click checkout
    checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)

    # Wait for checkout step 1 form
    wait.until(EC.visibility_of_element_located((By.ID, "first-name")))

    return CheckoutPage(driver)


def test_complete_purchase(setup):
    checkout = reach_checkout(setup)

    checkout.enter_details("Arun", "KM", "560001")
    checkout.click_continue()
    checkout.click_finish()
    checkout.wait_for_order_completion()

    assert "checkout-complete" in setup.current_url
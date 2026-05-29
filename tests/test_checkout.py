# tests/test_checkout.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from config.config import PASSWORD  # USERNAME removed — comes from fixture now


def reach_checkout(driver):
    wait = WebDriverWait(driver, 20)

    # --- Login with worker-assigned user (prevents session collision in -n auto) ---
    username = getattr(driver, "sauce_user", "standard_user")  # fallback for serial runs

    login = LoginPage(driver)
    login.enter_username(username)   # ← was USERNAME (hardcoded)
    login.enter_password(PASSWORD)
    login.click_login()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    ))

    add_btn = driver.find_element(
        By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']"
    )
    driver.execute_script("arguments[0].click();", add_btn)

    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "shopping_cart_badge")
    ))

    driver.get("https://www.saucedemo.com/cart.html")
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))

    checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)

    wait.until(EC.visibility_of_element_located((By.ID, "first-name")))

    return CheckoutPage(driver)


def test_complete_purchase(setup):
    checkout = reach_checkout(setup)

    checkout.enter_details("Arun", "KM", "560001")
    checkout.click_continue()
    checkout.click_finish()
    checkout.wait_for_order_completion()

    assert "checkout-complete" in setup.current_url
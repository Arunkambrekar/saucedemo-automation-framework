import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from config.config import USERNAME, PASSWORD


def reach_checkout(driver):
    wait = WebDriverWait(driver, 20)

    # Login
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    # Wait for inventory page
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Add item to cart
    add_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart-sauce-labs-backpack']"))
    )
    add_btn.click()

    # Click cart icon (robust)
    cart_icon = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_icon)

    try:
        cart_icon.click()
    except:
        driver.execute_script("arguments[0].click();", cart_icon)

    # ✅ Wait for cart page properly
    wait.until(EC.url_contains("cart"))

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    # Click checkout
    checkout_btn = wait.until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )

    driver.execute_script("arguments[0].click();", checkout_btn)

    # Wait for checkout form
    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    return CheckoutPage(driver)


# ✅ FIXED (no skip anymore)
def test_complete_purchase(setup):
    checkout = reach_checkout(setup)

    checkout.enter_details("Arun", "KM", "560001")
    checkout.click_continue()

    # ✅ FIX: wait for finish button instead of URL
    WebDriverWait(setup, 15).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    checkout.click_finish()
    checkout.wait_for_order_completion()

    assert "checkout-complete" in setup.current_url
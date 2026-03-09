import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.checkout_page import CheckoutPage
from config.config import USERNAME, PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def reach_checkout(driver):
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    WebDriverWait(driver, 15).until(EC.url_contains("inventory"))
    time.sleep(2)

    driver.execute_script("""
        var buttons = document.querySelectorAll("[data-test^='add-to-cart']");
        if(buttons.length > 0) { buttons[0].click(); }
    """)
    time.sleep(3)

    driver.get("https://www.saucedemo.com/cart.html")
    time.sleep(2)

    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    if len(items) == 0:
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(2)
        driver.execute_script("""
            var buttons = document.querySelectorAll("[data-test^='add-to-cart']");
            if(buttons.length > 0) { buttons[0].click(); }
        """)
        time.sleep(3)
        driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(2)

    checkout_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )

    return CheckoutPage(driver)


def test_complete_purchase(setup):
    checkout = reach_checkout(setup)
    checkout.enter_details("Arun", "KM", "560001")
    checkout.click_continue()
    WebDriverWait(setup, 15).until(
        EC.url_contains("checkout-step-two")
    )
    time.sleep(1)
    checkout.click_finish()
    checkout.wait_for_order_completion()
    assert "checkout-complete" in setup.current_url
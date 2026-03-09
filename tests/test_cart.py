import pytest
import time
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config.config import USERNAME, PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_and_go_to_cart(driver):
    from pages.login_page import LoginPage
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    WebDriverWait(driver, 15).until(EC.url_contains("inventory"))
    time.sleep(2)

    # Add item via pure JS — bypasses all click intercept issues
    driver.execute_script("""
        var buttons = document.querySelectorAll("[data-test^='add-to-cart']");
        if(buttons.length > 0) { buttons[0].click(); }
    """)
    time.sleep(3)

    # Navigate directly to cart
    driver.get("https://www.saucedemo.com/cart.html")
    time.sleep(2)

    # Retry if cart empty
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

    return CartPage(driver)


def test_cart_has_one_item(setup):
    login_and_go_to_cart(setup)
    items = setup.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 1, "Expected 1 item in cart"


def test_cart_continue_shopping(setup):
    login_and_go_to_cart(setup)
    btn = WebDriverWait(setup, 15).until(
        EC.element_to_be_clickable((By.ID, "continue-shopping"))
    )
    setup.execute_script("arguments[0].click();", btn)
    time.sleep(3)
    assert "inventory" in setup.current_url


def test_cart_remove_item(setup):
    login_and_go_to_cart(setup)
    remove_btn = WebDriverWait(setup, 15).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-test^='remove']")
        )
    )
    setup.execute_script("arguments[0].click();", remove_btn)
    time.sleep(2)
    items = setup.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 0, "Item was not removed from cart"
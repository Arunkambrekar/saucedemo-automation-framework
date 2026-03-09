import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from config.config import USERNAME, PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_and_go_to_cart(driver):
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    WebDriverWait(driver, 15).until(EC.url_contains("inventory"))
    time.sleep(1)

    dashboard = DashboardPage(driver)
    dashboard.add_first_product_to_cart()

    # Retry click if badge not found (headless CI fallback)
    time.sleep(3)
    badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    if not badge:
        buttons = driver.find_elements(By.CSS_SELECTOR, "[data-test^='add-to-cart']")
        if buttons:
            driver.execute_script("arguments[0].click();", buttons[0])
            time.sleep(3)

    # Navigate directly to cart
    driver.get("https://www.saucedemo.com/cart.html")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    return CartPage(driver)


def test_cart_has_one_item(setup):
    login_and_go_to_cart(setup)
    items = setup.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 1, "Expected 1 item in cart"


def test_cart_continue_shopping(setup):
    login_and_go_to_cart(setup)
    btn = WebDriverWait(setup, 10).until(
        EC.element_to_be_clickable((By.ID, "continue-shopping"))
    )
    btn.click()
    WebDriverWait(setup, 10).until(EC.url_contains("inventory"))
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
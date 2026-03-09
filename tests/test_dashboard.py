import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def login_and_get_dashboard(driver):
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    return DashboardPage(driver)


def test_products_loaded(setup):
    dashboard = login_and_get_dashboard(setup)
    products = dashboard.get_all_products()
    assert len(products) == 6


def test_add_to_cart(setup):
    dashboard = login_and_get_dashboard(setup)
    dashboard.add_first_product_to_cart()
    WebDriverWait(setup, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert dashboard.get_cart_count() == "1"


def test_add_multiple_items(setup):
    dashboard = login_and_get_dashboard(setup)
    dashboard.add_multiple_products(2)
    WebDriverWait(setup, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert dashboard.get_cart_count() == "2"


def test_cart_icon_navigates_to_cart(setup):
    dashboard = login_and_get_dashboard(setup)
    dashboard.add_first_product_to_cart()
    WebDriverWait(setup, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    dashboard.click_cart()
    WebDriverWait(setup, 15).until(EC.url_contains("cart"))
    assert "cart" in setup.current_url


def test_sort_price_low_to_high(setup):
    dashboard = login_and_get_dashboard(setup)
    sort = Select(setup.find_element(
        By.CLASS_NAME, "product_sort_container")
    )
    sort.select_by_value("lohi")
    prices = setup.find_elements(By.CLASS_NAME, "inventory_item_price")
    price_values = [float(p.text.replace("$", "")) for p in prices]
    assert price_values == sorted(price_values)
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD

def test_add_to_cart(setup):
    driver = setup

    # Login
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    dashboard = DashboardPage(driver)

    # Validate products loaded
    products = dashboard.get_all_products()
    assert len(products) > 0, "No products found on dashboard"

    # Add first product to cart
    dashboard.add_first_product_to_cart()

    # Validate cart count
    assert dashboard.get_cart_count() == "1", "Cart count did not update"

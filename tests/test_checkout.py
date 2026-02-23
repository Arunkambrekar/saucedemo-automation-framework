from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.config import USERNAME, PASSWORD

def test_complete_purchase(setup):
    driver = setup

    # Login
    login = LoginPage(driver)
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    dashboard = DashboardPage(driver)

    # Add product
    dashboard.add_first_product_to_cart()

    # Go to Cart
    dashboard.click_cart()

    cart = CartPage(driver)
    cart.click_checkout()

    # Checkout Info
    checkout = CheckoutPage(driver)
    checkout.enter_details("Arun", "KM", "560001")
    checkout.click_continue()

    # Finish Order
    checkout.click_finish()

    # ✅ Stable validation (URL-based)
    checkout.wait_for_order_completion()
    assert "checkout-complete" in driver.current_url

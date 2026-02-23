from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD

def test_valid_login(setup):
    driver = setup
    login = LoginPage(driver)

    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    assert "inventory" in driver.current_url, "Login failed!"

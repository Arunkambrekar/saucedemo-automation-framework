import pytest
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD

# ---- Helper ----
def do_login(driver, user, pwd):
    login = LoginPage(driver)
    login.enter_username(user)
    login.enter_password(pwd)
    login.click_login()
    return login

# ---- Tests ----
def test_valid_login(setup):
    do_login(setup, USERNAME, PASSWORD)
    assert "inventory" in setup.current_url, "Valid login failed"

def test_invalid_password(setup):
    login = do_login(setup, USERNAME, "wrong_pass")
    error = login.get_text((
        __import__('selenium').webdriver.common.by.By.CSS_SELECTOR,
        "[data-test='error']"
    ))
    assert "do not match" in error

def test_empty_username(setup):
    login = do_login(setup, "", PASSWORD)
    error = login.get_text((
        __import__('selenium').webdriver.common.by.By.CSS_SELECTOR,
        "[data-test='error']"
    ))
    assert "Username is required" in error

def test_empty_password(setup):
    login = do_login(setup, USERNAME, "")
    error = login.get_text((
        __import__('selenium').webdriver.common.by.By.CSS_SELECTOR,
        "[data-test='error']"
    ))
    assert "Password is required" in error

def test_locked_out_user(setup):
    login = do_login(setup, "locked_out_user", PASSWORD)
    error = login.get_text((
        __import__('selenium').webdriver.common.by.By.CSS_SELECTOR,
        "[data-test='error']"
    ))
    assert "locked out" in error
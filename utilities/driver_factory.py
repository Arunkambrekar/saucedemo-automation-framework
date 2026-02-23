from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    chrome_options = Options()

    # Disable password manager popups
    chrome_prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # Disable notifications & info bars
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    # Start maximized
    chrome_options.add_argument("--start-maximized")

    # Optional (stability for automation)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Use WebDriver Manager (auto manages chromedriver)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(5)
    return driver
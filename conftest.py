# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SAUCE_USERS = [
    "standard_user",
    "error_user",
]

def get_worker_user(worker_id: str) -> str:
    if worker_id == "master":
        return SAUCE_USERS[0]
    index = int(worker_id.replace("gw", "")) % len(SAUCE_USERS)
    return SAUCE_USERS[index]


@pytest.fixture(scope="function")
def setup(request):
    worker_id = getattr(request.config, "workerinput", {}).get("workerid", "master")

    options = Options()

    # Headless in CI (GitHub Actions sets CI=true), real browser locally
    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get("https://www.saucedemo.com/")
    driver.sauce_user = get_worker_user(worker_id)

    yield driver
    driver.quit()


# Screenshot on failure — saves to screenshots/ and uploads as CI artifact
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/{item.name}.png"
            driver.save_screenshot(path)
            print(f"\nScreenshot saved: {path}")
import sys
import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_PATH)

import pytest
from utilities.driver_factory import get_driver
from config.config import BASE_URL
from utilities.screenshot import take_screenshot

@pytest.fixture
def setup(request):
    driver = get_driver()
    driver.get(BASE_URL)

    yield driver

    # Check if test failed
    outcome = request.node._report_sections
    failed = False

    for section in outcome:
        if "Call" in section[0] and section[1] == "failed":
            failed = True
            break

    if failed:
        take_screenshot(driver, request.node.name)

    driver.quit()

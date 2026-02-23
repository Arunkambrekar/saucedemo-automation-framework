def take_screenshot(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")

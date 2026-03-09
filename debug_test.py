from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

d = webdriver.Chrome()
d.get('https://www.saucedemo.com')
d.find_element(By.ID, 'user-name').send_keys('standard_user')
d.find_element(By.ID, 'password').send_keys('secret_sauce')
d.find_element(By.ID, 'login-button').click()

WebDriverWait(d, 10).until(EC.url_contains('inventory'))
time.sleep(2)

# Try data-test attribute instead of text
buttons = d.find_elements(By.CSS_SELECTOR, "[data-test^='add-to-cart']")
print('Buttons found by data-test:', len(buttons))

if buttons:
    print('First button data-test:', buttons[0].get_attribute('data-test'))
    d.execute_script("arguments[0].click();", buttons[0])  # JS click
    time.sleep(2)

badge = d.find_elements(By.CLASS_NAME, 'shopping_cart_badge')
print('Cart badge:', badge[0].text if badge else 'NO BADGE')

d.get('https://www.saucedemo.com/cart.html')
time.sleep(2)
print('Cart URL:', d.current_url)

items = d.find_elements(By.CLASS_NAME, 'cart_item')
print('Cart items found:', len(items))

d.quit()
print('DONE')
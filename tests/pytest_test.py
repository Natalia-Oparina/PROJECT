from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from time import sleep
from datetime import datetime 

########Functions##########
def launch_swaglabs():
    global driver
    driver=webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.saucedemo.com/')

def login_valid_credentials():
    launch_swaglabs()
    driver.find_element(By.CSS_SELECTOR,"#user-name").send_keys('performance_glitch_user')
    driver.find_element(By.CSS_SELECTOR,"#password").send_keys('secret_sauce')
    driver.find_element(By.CSS_SELECTOR,"#login-button").click()

def capture_evidence():
    image_name= fr"C:\PROJECT\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

@pytest.fixture()
def setup(request):
    launch_swaglabs()
    login_valid_credentials()

    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)

########Tests########

login_parameters= [
    ('performance_glitch_user', 'random', 'Username and password do not match'),
    ('random', 'secret_sauce', 'Username and password do not match'),
    ('random', 'random', 'Username and password do not match'),
    ('', 'secret_sauce','Username is required'),
    ('performance_glitch_user', '', 'Password is required'),
    ('', '', 'Username and password are required')
    ]
    
@pytest.mark.parametrize("username,password,checkpoint",login_parameters)
def test_login_invalid_credentials(username,password,checkpoint):
    launch_swaglabs()
    driver.find_element(By.CSS_SELECTOR,"#user-name").send_keys(username)
    driver.find_element(By.CSS_SELECTOR,"#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR,"#login-button").click()
    assert checkpoint.lower() in driver.page_source.lower()
    capture_evidence()
    driver.quit() 



def test_login_valid_credentials(setup):
    assert 'products'.lower() in driver.page_source.lower()
    

def test_view_product_details(setup):
    driver.find_element(By.XPATH,"//div[text()='Sauce Labs Fleece Jacket']").click()
    assert 'back to products'.lower() in driver.page_source.lower()
    sleep(5)
   

def test_add_item_to_cart(setup):
    driver.find_element(By.XPATH,"//div[text()='Sauce Labs Fleece Jacket']").click()
    driver.find_element(By.CSS_SELECTOR,"#add-to-cart-sauce-labs-fleece-jacket").click()
    assert 'remove'.lower() in driver.page_source.lower()
   

def test_open_shopping_cart(setup):
    driver.find_element(By.XPATH,"//div[text()='Sauce Labs Fleece Jacket']").click()
    driver.find_element(By.CSS_SELECTOR,"#add-to-cart-sauce-labs-fleece-jacket").click()
    driver.find_element(By.CSS_SELECTOR,".shopping_cart_link").click()
    element=driver.find_element(By.CSS_SELECTOR,"#checkout")
    assert element.text=='checkout'.upper()
      
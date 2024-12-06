import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pytest_in_robotframework import pytest_execute
from ..pytest_in_robotframework.pytest_in_robotframework import pytest_execute

"""
def open_web_page(page): 
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(page)

@externaly_pytest_execute
@pytest.mark.login
@pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce")])
def test_login_as(user,password):
    username = driver.find_element(By.ID,'user-name')
    username.send_keys(user) 
    my_password = driver.find_element(By.ID,'password')
    my_password.send_keys(password)
    time.sleep(1)
    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()
    print(__name__)
    time.sleep(5)
"""

@pytest_execute
#@pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("locked_out_user", "secret_sauce"),("problem_user", "secret_sauce")])
@pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("problem_user", "secret_sauce")])
def test_func_login_as(user,password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.saucedemo.com/')
    print("vykonal jsem prvni radek test_func_login_as...")
    time.sleep(1)
    username = driver.find_element(By.ID,'user-name')
    username.clear()
    username.send_keys(user)
    my_password = driver.find_element(By.ID,'password')
    my_password.clear()
    my_password.send_keys(password)
    time.sleep(1)
    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()
    print(__name__)
    time.sleep(1)
    button = driver.find_element(By.ID, 'react-burger-menu-btn')
    button.click()
    time.sleep(1)
    button = driver.find_element(By.ID, 'logout_sidebar_link')
    button.click()
    time.sleep(1)
    driver.close()
    driver.quit()
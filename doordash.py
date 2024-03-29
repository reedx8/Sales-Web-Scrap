'''
TODO:
1. Ensure sales value is for the appropriate store:
    - could cehck the menu button
    - coulc grab previous_sales and check if sales == previous_sales
2. Change find_element on the sales value to something more reliable
'''

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from sheet import send_data
from dotenv import load_dotenv
# from fake_useragent import UserAgent

def resource_path(relative_path):
    """Get the absolute path to the resource, works for development and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

env_path = resource_path(os.path.join('assets', '.env'))
load_dotenv(env_path)

# env_path = os.path.join('assets', '.env')
# load_dotenv(env_path)
# load_dotenv()

options = ChromeOptions()
# ua = UserAgent()
# user_agent = ua.random

# options.add_argument(f'--user-agent={user_agent}') # Needed for headless mode to work in DD
options.add_argument("--window-size=1200,600")
# options.add_argument("--headless=new") # headless browser mode (Random 2SV popup renders headless mode in DD inconsistent)

username = os.getenv('DD_USERNAME')
password = os.getenv('DD_PW')

login_url = os.getenv('DD_LOGIN_URL')

hall = "Ava Roasteria (Hall Blvd)"
barrows = "Ava Roasteria (SW Barrows Rd)"
kruse = "Ava Roasteria (Meadows Rd)"
orenco = "Ava Roasteria (Hillsboro)"
all_stores = [hall, barrows, kruse, orenco]

all_sales = {
    'Hall': 0,
    'Barrows': 0,
    'Kruse': 0,
    'Orenco': 0
}


def run_doordash():
    print("\nRunning Doordash...")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5) # Global setting that sets driver to wait a max of x seconds to find each requested element in DOM tree if they are not immediately available in DOM already
    actions = ActionChains(driver)

    driver.get(login_url)

    sleep(3) # UPDATE: Thought sleep(3) avoided 2 step verification, doesnt seem to. Will need to manually verify, or implement email scrap

    # may be nec if you need to handle the 2 stem email verification:
    # driver.alert_is_present()
    # alert = driver.switch_to.alert


    # Step 1 --  Handle log in
    for attempts in range(4):
        try:
            username_field = driver.find_element(By.XPATH, "//*[@id='FieldWrapper-0']")
            
            # "if" conditionals handle case where username and/or password entered in twice due
            # to only login_button throwing an exception, therefor failing to login:
            if (username_field.get_attribute('value') != username): # accesses the value attributes text on the element
                username_field.send_keys(username)
            
            continue_with_login = driver.find_element(By.ID, 'merchant-login-submit-button')
            actions.move_to_element(continue_with_login).click(continue_with_login).perform()

            password_field = driver.find_element(By.XPATH, "//*[@id='FieldWrapper-2']")

            if (password_field.get_attribute('value') != password):
                password_field.send_keys(password)

            login_button = driver.find_element(By.ID, 'login-submit-button')
            login_button.send_keys(Keys.RETURN)
            break #neccessary for some reason, otherwise it will both login + cauase an exception on 3rd attempt (attempts = 2)
        except Exception as error:
            if (attempts >= 3):
                print("Doordash: Couldnt login, likely due to 2SV popup")
                driver.quit()
                return 1
            else:
                print("Doordash: Login attempt made...")
                print(error)
                sleep(5)


    # Wait for the page to load after login, initial login can take awhile (adjust the wait time as needed)
    # sleep(2) # simply pauses execution for x seconds
    sleep(3) # waits to see if 2 step verification popup shows

    # Attempts to wait for 2 step verifcation success for a max of 50 seconds (+5 seconds from implicitly_wait()):
    for attempts in range(4):
        try:
            merchant_app = driver.find_element(By.ID, "MerchantApp").is_displayed()
        except Exception as error:
            if (attempts >= 3):
                print("Doordash: 2 step verification blocked, or network error")
                driver.quit()
                return 2
            else:
                print("Doordash: 2-Step verification screen shown. You must pass 2SV check before app can continue.")
                sleep(15)

    print("Successfully logged in...")
    # Step 2 -- Click on general menu button at top left after log in
    for attempts in range(4):
        try:
            store_btn = driver.find_element(By.XPATH, "//span[text()='Ava Roasteria']")
            sleep(2) # required sometimes, or else click below just wont happen (not clickable yet)
            actions.move_to_element(store_btn).click(store_btn).perform()
            sleep(1) # required sometimes
            break
        except Exception as error:
            if attempts >= 3:
                print("ERROR: Couldn't find or interact with store button")
                driver.quit()
                return 3
            else:
                try:
                    menu_btn = driver.find_element(By.XPATH, "//button[@aria-label='Show Side Menu']")
                    actions.move_to_element(menu_btn).click(menu_btn).perform()
                except Exception as error:
                    print("ERROR: Couldn't find or interact with menu button")
                    driver.quit()
                    return 3


    # Step 3 -- Grab sales for all stores
    for store_name in all_stores:
        # Go to the individual store's doordash homepage:
        for attempts in range(4):
            try:
                link = driver.find_element(By.XPATH, f"//div[text()='{store_name}']")
                actions.move_to_element(link).click(link).perform()
                break
            except Exception as error:
                if attempts >= 3:
                    print("ERROR: Couldnt find or interact with store link")
                    driver.quit()
                    return 3
                else:
                    try:
                        menu_btn = driver.find_element(By.XPATH, "//button[@aria-label='Show Side Menu']")
                        actions.move_to_element(menu_btn).click(menu_btn).perform()
                    except Exception as error:
                        print("ERROR: Couldn't find or interact with menu button")
                        driver.quit()
                        return 3

        # driver.get(store) # this caused a cloudflare "prove that youre a human" page
        sleep(5) # necessary or else sales may be grabbed before next store's sales is ready, causing identical sales across stores

        # Get the individual store's sales from its homepage:
        for attempts in range(4):
            try:
                sales = driver.find_element(By.CLASS_NAME, "bzJrJX") # 3 class duplicates on page, its taking first class
                # sales = driver.find_element(By.XPATH, "//*[@id='MerchantApp']/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/span[2]")
            except Exception as error:
                if attempts >= 3:
                    print("ERROR: Couldnt find sales (class = bzJrJX)")
                    driver.quit()
                    return 3
                else:
                    sleep(3)
        
        # output the sales value:
        # print(store_name + ": " + sales.text)


        if (store_name == hall):
            all_sales['Hall'] = sales.text[1:]
        elif (store_name == barrows):
            all_sales['Barrows'] = sales.text[1:]
        elif (store_name == kruse):
            all_sales['Kruse'] = sales.text[1:]
        elif (store_name == orenco):
            all_sales['Orenco'] = sales.text[1:]
        else:
            print("ERROR: Store name is incorrect. See 'all_stores'")

        # Click on top left menu button to dropdown
        store_btn = driver.find_element(By.XPATH, f"//span[text()='{store_name}']")
        actions.move_to_element(store_btn).click(store_btn).perform()
        sleep(1)



    # Step 3 -- Send live sales data to spreadsheet:
    send_data(all_sales, "doordash")

    # Step 4 -- Quit driver and exit program. Done:
    driver.quit()
    return all_sales





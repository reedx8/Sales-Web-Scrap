'''
TODO: 
- refactor this file first...
- Test retry if '----' properly
- navigate to avaroasteria.revelup.com/reports after logging in (target_url)
-  get sales from reports > fileres > all incluscions unchecked (can include tips) > net sales
- check that each store_link == store name you are expecting 
- actions that are highly dependant on UI not changing
- what if beaverton not loaded first after logging in?
'''

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from sheet import send_data
from threading import Thread
from fake_useragent import UserAgent

load_dotenv()

# removes 1 less variable by ensuring window size is always the same
options = ChromeOptions()
ua = UserAgent()
user_agent = ua.random

options.add_argument(f'--user-agent={user_agent}')
options.add_argument("--window-size=1200,600")
options.add_argument("--headless=new") # headless browser mode
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
# options.add_arguments("window-size=1200x600", "--headless=new", "--disable-gpu", "--disable-extensions")
# options.addArguments("window-size=1200x600", "--headless=new", "--disable-gpu", "--disable-extensions")


login_url = os.getenv('REV_LOGIN_URL')
target_url = os.getenv('REV_TARGET_URL')
username = os.getenv('REV_USERNAME')
password = os.getenv('REV_PW')

all_sales = {
    "Hall": 0,
    "Barrows": 0,
    "Kruse": 0,
    "Orenco": 0
}

# Either used multiple times in code, or location in DOM likely to be changed
establ_classname =  "sc-jSUZER"
net_sales_xpath = "//*[@id='overview-payment-widget']/div[2]/div[2]/div[5]/div[2]"
lo_menu_xpath = "//*[@id='establishments-tree']/div/div[3]/ul/li[1]/ul/li[2]/span[2]/span[3]"
orenco_menu_xpath = "//*[@id='establishments-tree']/div/div[3]/ul/li[1]/ul/li[3]/span[2]/span[3]"
barrows_menu_xpath = "//*[@id='establishments-tree']/div/div[3]/ul/li[1]/ul/li[4]/span[2]/span[3]"

def run_revel():
    print("\nRunning Revel...")

    driver = webdriver.Chrome(options=options) # Pass nothing to Chrome() if you want to see code working
    # driver.implicitly_wait(5) # Global setting that sets driver to wait a max of x seconds to find each requested element in DOM tree if they are not immediately available in DOM already
    driver.implicitly_wait(10)
    actions = ActionChains(driver)

    driver.get(login_url)

    shadow_root_script = "return document.querySelector('body > login-app').shadowRoot"

    # Step 1 --  Handle log in (4 attempts)
    for attempts in range(5):
        try:
            shadow_root = driver.execute_script(shadow_root_script)
            username_field = shadow_root.find_element(By.CSS_SELECTOR, '.login-app-1-MuiInputBase-input')
            password_field = shadow_root.find_element(By.CSS_SELECTOR, '.login-app-1-MuiOutlinedInput-inputAdornedEnd')
            
            # if checks handle case where username and/or password entered in twice due
            # to only login_button throwing an exception, therefor failing to login:
            if(username_field.get_attribute('value') != username): # accesses the value attributes text on the element
                username_field.send_keys(username)
            if(password_field.get_attribute('value') != password):
                password_field.send_keys(password)

            login_button = shadow_root.find_element(By.CSS_SELECTOR, '.login-app-1-MuiButton-root')
            login_button.send_keys(Keys.RETURN)
        except Exception as error:
            if (attempts >= 4):
                # print('ERROR: Username, password, or login button wasnt yet loaded in the HTML DOM. Try waiting longer.')
                print(error)
                driver.quit()
                return 1
            else:
                print("Login attempt made...")
                sleep(2)
        else:
            break #needed, else code will login after succesfull atempt but also error and quit from exception at times (bug)


    # Wait for the page to load after login, initial login can take awhile (adjust the wait time as needed)
    # sleep(10) # simply pauses execution for x seconds
    sleep(8) # simply pauses execution for x seconds

    # Step 2 -- Get shadow root from html dom
    shadow_root_script = "return document.querySelector('body > div.mf-header-wrapper > management-console-header').shadowRoot"
    shadow_root = driver.execute_script(shadow_root_script)
    establishment_link = shadow_root.find_element(By.CLASS_NAME, establ_classname)

    print("Successfully logged in...")

    # Step 3 -- Make 3 total attempts to get beaverton's net sales:
    for attempts in range(4):
        # DNU: relative xpath worked here where full xpath didnt for some reason
        net_sales = driver.find_element(By.XPATH, net_sales_xpath).text # accesses text inside element
        if (attempts >= 3):
            print("ERROR: Net sales not loading. Check internet connection and try again.")
            net_sales = "--"
            # driver.quit()
            # exit()
        elif (net_sales == "----"):
            sleep(3) # net sales not loaded yet, wait x seconds
        else:
            break # got net sales figure
    # print("Hall: $", net_sales)
    all_sales["Hall"] = net_sales

    # DNU: full xpath worked here in the menu though for some reason
    stores_xpaths = [
        lo_menu_xpath,
        orenco_menu_xpath,
        barrows_menu_xpath
    ]

    # go to each of the 3 other stores and grab net sales
    for i in range(3):
        # click on establishmnet link to bring up menu
        # DNU: establishment_link.send_keys(Keys.RETURN) does NOT work here
        actions.move_to_element(establishment_link).click(establishment_link).perform()

        # Wait up to a max of 3 times for menu to load
        for attempts in range(4):
            if (attempts >= 3):
                print("ERROR: Menu not loading. Check internet connection and try again.")
                driver.quit()
                exit()
            elif (driver.find_element(By.XPATH, stores_xpaths[i]).is_displayed()):
                # element is ready/displayed
                store_link = driver.find_element(By.XPATH, stores_xpaths[i]) 
                # print(store_link.is_displayed())
                break
            else:
                # loading wheel is present
                print("loading wheel: ", driver.find_element(By.XPATH, stores_xpaths[i]).is_displayed())
                sleep(3)
                
        actions.move_to_element(store_link).click(store_link).perform()

        # new page: wait for page to load
        # sleep(5)
        sleep(3)

        # You need to re-establish shadow_root and its children after each page load
        shadow_root = driver.execute_script(shadow_root_script)
        establishment_link = shadow_root.find_element(By.CLASS_NAME, establ_classname)

        # make 3 attempts to grab net sales. done.
        for attempts in range(4):
            # DNU: both full and relative xpaths worked here for some reason
            net_sales = driver.find_element(By.XPATH, net_sales_xpath).text # accesses text inside element

            if (attempts >= 3):
                print("ERROR: Net sales not loading. Check internet connection and try again.")
                net_sales = "--"
                # driver.quit()
                # exit()
            elif (net_sales == "----"):
                sleep(3)
            else:
                # got net sales figure
                break

        if (i == 0):
            all_sales["Kruse"] = net_sales
            # print("Kruse: $", net_sales)
        elif(i == 1):
            all_sales["Orenco"] = net_sales
            # print("Orenco: $", net_sales)
        elif (i == 2):
            all_sales["Barrows"] = net_sales
            # print("Barrows: $", net_sales)
        
        
    send_data(all_sales, "revel")

    # Final step -- Close the Selenium WebDriver
    driver.quit()
    return all_sales
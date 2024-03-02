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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import platform
from fake_useragent import UserAgent

load_dotenv()

options = ChromeOptions()
ua = UserAgent()
user_agent = ua.random

# options.add_argument(f'--user-agent={user_agent}')
options.add_argument("--window-size=1200,600")
# options.add_argument("--headless=new") # Cant do headless mode in uber (login's next button never found)
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

login_url = os.getenv("UBER_LOGIN_URL")
username = os.getenv("UBER_USERNAME")
password = os.getenv("UBER_PW")

hall = "AVA Roasteria (SW Hall Blvd)"
barrows = "Ava Roasteria (Barrows Road)"
kruse = "AVA Roasteria (Lake Oswego)"
orenco = "Ava Roasteria (Orenco Station)"

all_stores = [
    hall,
    barrows,
    kruse,
    orenco
]

all_sales = {
    "Hall": 0,
    "Barrows": 0,
    "Kruse": 0, 
    "Orenco": 0
}

def run_uber():
    print("\nRunning Uber Eats...")

    # step 0: install OS specific chromedriver
    currentOS = platform.system().lower()
    if currentOS== "darwin": # mac os
        driver = webdriver.Chrome(options=options)
    elif currentOS == "windows":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        print("Linux OS detected. Program has not been tested on linux. Exiting program...")
        exit()

    driver.implicitly_wait(15) 
    actions = ActionChains(driver) 


    # Step 1: Handle Google Login
    driver.get(login_url)
    try:
        cont_with_google_btn = driver.find_element(By.XPATH, "//p[text()='Continue with Google']")
        actions.move_to_element(cont_with_google_btn).click(cont_with_google_btn).perform()

        popup = driver.window_handles[1]
        driver.switch_to.window(popup)

        username_field = driver.find_element(By.XPATH, "//input[@type='email']")
        username_field.send_keys(username)

        next_btn = driver.find_element(By.XPATH, "//span[text()='Next']") # Fails here in headless mode
        actions.move_to_element(next_btn).click(next_btn).perform()

        sleep(3)

        pw_field = driver.find_element(By.XPATH, "//input[@type='password']")
        pw_field.send_keys(password)

        next_btn = driver.find_element(By.XPATH, "//span[text()='Next']") # otherwise stale element....
        actions.move_to_element(next_btn).click(next_btn).perform()
    except Exception as e:
        print("Couldn't log in")
        print("Error message shown below:\n")
        print(e)
        driver.quit()
        return 1

    # Handles sign in to uber confirm screen possibility:
    try:
        sign_in_confirm = driver.find_element(By.XPATH, "//span[text()='Continue']")
        actions.move_to_element(sign_in_confirm).click(sign_in_confirm).perform()
    except:
        print("Sign in confirm screen did not show")

    # sleep(10)


    driver.switch_to.window(driver.window_handles[0])
    # sleep(5)

    #TODO: Handle all set screen possibility (automatically continues on own)
    '''
    try:
        all_set_confirm = driver.find_element(By.XPATH, "//span[text()='Continue']")
        actions.move_to_element(all_set_confirm).click(all_set_confirm).perform()
    except:
        print("All Set screen did not show")
    '''


    # Step 2: Grab live sales from each store
    # sleep(5) # needed, else stale element error on menu_btn
    sleep(15) # needed, else stale element error on menu_btn, or it will grab total business sales for hall
    for store in all_stores:
        try:
            menu_btn = driver.find_element(By.XPATH, "//*[@id='wrapper']/div[1]/div[2]/div[2]/div[1]/div/div[1]/button")
            actions.move_to_element(menu_btn).click(menu_btn).perform()
        except:
            print("Menu button not found")
        # sleep(5) #Needed. sleep(3) seconds wasnt always long enough wait for menu+element to load
        # sleep(4)
        try:
            store_link = driver.find_element(By.XPATH, f"//p[text()='{store}']")
            sleep(1)
            actions.move_to_element(store_link).click(store_link).perform()
        except:
            print("Store link in menu not found")
        # sleep(10) # must wait
        sleep(8)

        try:
            sales = driver.find_element(By.XPATH, "//h5[@data-baseweb='typo-headingsmall']").text
        except:
            print("Cant find sales yet")

        print(store, ": ", sales)

        if (store == hall):
            all_sales["Hall"] = sales[1:]
        elif (store == barrows):
            all_sales["Barrows"] = sales[1:]
        elif (store == kruse):
            all_sales["Kruse"] = sales[1:]
        elif (store == orenco):
            all_sales["Orenco"] = sales[1:]
        
    # Step 3: Send live sales data to spreadsheet
    send_data(all_sales, "uber")

    # Step 4: Quit selenium properly, and exit program. Done. 
    driver.quit()
    return all_sales
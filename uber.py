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

load_dotenv()

if sys.argv[1] == 'x3':
    driver = webdriver.Chrome('C:\\Users\\reedx\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe')
else:
    driver = webdriver.Chrome()
driver.implicitly_wait(5) 
actions = ActionChains(driver)
options = ChromeOptions()
options.add_argument("window-size=1200x600") 

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

print("\nRunning Uber Eats...")

# Step 1: Handle Login
driver.get(login_url)
cont_with_google_btn = driver.find_element(By.XPATH, "//p[text()='Continue with Google']")
actions.move_to_element(cont_with_google_btn).click(cont_with_google_btn).perform()

popup = driver.window_handles[1]
driver.switch_to.window(popup)

username_field = driver.find_element(By.XPATH, "//input[@type='email']")
username_field.send_keys(username)

next_btn = driver.find_element(By.XPATH, "//span[text()='Next']")
actions.move_to_element(next_btn).click(next_btn).perform()

sleep(3)

pw_field = driver.find_element(By.XPATH, "//input[@type='password']")
pw_field.send_keys(password)

next_btn = driver.find_element(By.XPATH, "//span[text()='Next']") # otherwise stale element....
actions.move_to_element(next_btn).click(next_btn).perform()


sleep(10)


# Step 2: Grab live sales from each store
driver.switch_to.window(driver.window_handles[0])
sleep(5) # needed, else stale element error on menu_btn
for store in all_stores:
    menu_btn = driver.find_element(By.XPATH, "//*[@id='wrapper']/div[1]/div[2]/div[2]/div[1]/div/div[1]/button")
    actions.move_to_element(menu_btn).click(menu_btn).perform()
    sleep(3)
    store_link = driver.find_element(By.XPATH, f"//p[text()='{store}']")
    sleep(1)
    actions.move_to_element(store_link).click(store_link).perform()
    sleep(10)

    sales = driver.find_element(By.XPATH, "//h5[@data-baseweb='typo-headingsmall']").text
    print(store, ": ", sales)

    if (store == hall):
        all_sales["Hall"] = sales
    elif (store == barrows):
        all_sales["Barrows"] = sales
    elif (store == kruse):
        all_sales["Kruse"] = sales
    elif (store == orenco):
        all_sales["Orenco"] = sales
    
# Step 3: Send live sales data to spreadsheet
send_data(all_sales, "uber")

# Step 4: Quit selenium properly, and exit program. Done. 
driver.quit()
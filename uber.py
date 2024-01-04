import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep # but not used here
from selenium.webdriver.common.action_chains import ActionChains # dont always need, not ussed here
from sheet import send_data
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome()
driver.implicitly_wait(5) # Global setting that sets driver to wait a max of x seconds to find each requested element in DOM tree if they are not immediately available in DOM already
actions = ActionChains(driver)
options = ChromeOptions()
options.add_argument("window-size=1200x600") # sets window size to remove variables (avoids mobile view)

login_url = os.getenv("UBER_LOGIN_URL")
# target_url = 'https://example.com/dashboard/' 
username = os.getenv("UBER_USERNAME")
password = os.getenv("UBER_PW")

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
# ...

# Step 3: Quit selenium properly, and exit program. Done. 
driver.quit()
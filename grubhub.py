import os
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from sheet import send_data
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import platform
from fake_useragent import UserAgent

env_path = os.path.join('assets', '.env')
load_dotenv(env_path)
# load_dotenv()

options = ChromeOptions()
# ua = UserAgent() # user_agent doesnt avoid login security check, commented out for now
# user_agent = ua.random

# Option attempts to avoid login security check (dont work for grubhub it seems):
# options.add_argument(f'--user-agent={user_agent}')
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# The rest of the options:
options.add_argument("--window-size=1200,600")
# options.add_argument("--headless=new") # TODO: doesnt work yet for grubhub
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

login_url = os.getenv("GRUBHUB_LOGIN_URL")
username = os.getenv("GRUBHUB_USERNAME")
password = os.getenv("GRUBHUB_PW")

hall = "Ava Roasteria - SW Hall Blvd"
barrows = "Ava Roasteria - SW Barrows Rd"
kruse = "Ava Roasteria - Meadows Rd"
orenco = "Ava Roasteria - NE Orenco Station Loop"

all_stores = [hall, barrows, kruse, orenco]

all_sales = {"Hall": 0, "Barrows": 0, "Kruse": 0, "Orenco": 0}

def fetch_subtotals(driver):
    # Locate the table containing the subtotal data
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'fin-transactions-display__transaction-totals')]"))
    )

    # Fetch rows from the table
    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    # Initialize a dictionary to store subtotal data for each restaurant
    subtotals = {}

    # Loop through each row and extract data
    for row in rows:
        # Extract restaurant name and subtotal
        restaurant_name = row.find_element(By.XPATH, "./td[@class='gfr-table__row__cell fin-transactions-display__table-data--ceil']").text
        subtotal = row.find_element(By.XPATH, "./td[@class='gfr-table__row__cell'][1]").text

        # Store data in the dictionary
        if "meadows" in str(restaurant_name).lower():
            subtotals["Kruse"] = subtotal[1:]
        elif "orenco" in str(restaurant_name).lower():
            subtotals["Orenco"] = subtotal[1:]
        elif "barrows" in str(restaurant_name).lower():
            subtotals["Barrows"] = subtotal[1:]
        elif "hall" in str(restaurant_name).lower():
            subtotals["Hall"] = subtotal[1:]

    return subtotals

# def send_data(subtotals, grubhub):
#     # Additional check for the existence of keys before accessing them
#     sales_data = {
#         "Hall": subtotals.get("Ava Roasteria - SW Hall Blvd", 0),
#         "Barrows": subtotals.get("Ava Roasteria - SW Barrows Rd", 0),
#         "Kruse": subtotals.get("Ava Roasteria - Meadows Rd", 0),
#         "Orenco": subtotals.get("Ava Roasteria - NE Orenco Station Loop", 0),
#     }

def run_grubhub():
    print("\nRunning Grubhub...")

    currentOS = platform.system().lower()
    if currentOS == "darwin": # mac os
        driver = webdriver.Chrome(options=options)
    elif currentOS == "windows":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        print("Linux OS detected. Program has not been tested on linux. Exiting program...")
        exit()

    driver.implicitly_wait(5)
    actions = ActionChains(driver)

    # Step 1: Handle Login
    driver.get(login_url)
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gfr-login-authentication-username"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gfr-login-authentication-password"))
        )

        sleep(3)
        username_field.send_keys(username)
        sleep(3)
        password_field.send_keys(password)
        sleep(5)

        
        '''
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
        )
        sleep(3)
        login_button.click()
        '''

        # login_button = driver.find_element(By.XPATH, "//span[text()='Sign in']")
        # actions.move_to_element(login_button).click(login_button).perform()
        # driver.send_keys
    except Exception as e:
        print("\nCouldnt log in")
        print("Error message shown below:\n")
        print(e)
        driver.quit()
        return 1

    try:
        login_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
        )
        login_button.click()
    except:
        print("Sign in button clicked, or couldnt log in. Continuing anyways...")



    '''
    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Financials']"))
    )
    financials.click()

    transactions = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Transactions']"))
    )
    transactions.click()
    '''

    '''
    # Step 2: Wait for the "Transactions" page to load directly
    try:
        print("Before WebDriverWait")
        transactions_page = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='multi-location-selector']"))
        )
        print("After WebDriverWait")
    except TimeoutException as e:
        print(f"Failed to load the Transactions page. Exception: {e}")
        driver.quit()
        sys.exit(1)
    '''

    driver.switch_to.window(driver.window_handles[0])
    sleep(2)
    # sleep(120)
    max_attempts = 1 
    for attempt in range(0,max_attempts+1):
        try:
            dashboard = driver.find_element(By.XPATH, "//h2[text()='Dashboard']")
            print("Successfully logged in...")
            break
        except Exception as e:
            if attempt >= max_attempts:
                print("\nGrubhub: Blocked by Login Security check")
                driver.quit()
                return 2
            else:
                # No use waiting for user, user can never pass this security check
                print(f"Grubhub: Waiting for user to pass login security check... (Attempt: {attempt+1}/{max_attempts})")
                sleep(2)
    

    # Get subtotals for only 4 stores:
    driver.get("https://restaurant.grubhub.com/financials/transactions/909517,909519,909523,909536")
    sleep(1)

    # Step 3: Set date range to the current date
    try:
        date_picker_input = driver.find_element(By.XPATH, "//input[@data-testid='export-modal-date-picker-input']")

        # Get the current date and format it as MM/DD/YYYY
        current_date = datetime.datetime.now().strftime("%m/%d/%Y")

        date_picker_input.clear()
        date_picker_input.send_keys(f"{current_date} - {current_date}")
        # print(("Successfully logged in..."))
    except Exception as e:
        print("Blocked by Login Security check screen")
        print("Error message shown below:\n")
        print(e)
        driver.quit()
        return 2


    # sleep(3)
    sleep(2)

     # Step 5: Fetch subtotal data after clicking update button
    subtotals = fetch_subtotals(driver)

    # Print the fetched data (for testing purposes)
    '''
    for restaurant, subtotal in subtotals.items():
        print(f"{restaurant}: {subtotal}")
    '''

    # sleep(5)  # Add a sleep here to wait for the page to update

    # Step 6: Send live sales data to the spreadsheet
    send_data(subtotals, "grubhub")

    # Step 7: Quit selenium properly, and exit the program. Done.
    driver.quit()
    return subtotals

# Run the function if this script is executed
if __name__ == "__main__":
    run_grubhub()
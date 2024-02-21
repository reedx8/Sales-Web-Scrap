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

load_dotenv()

options = ChromeOptions()
options.add_argument("window-size=1200x600")

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
        driver = webdriver.Chrome()
    elif currentOS == "windows":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        print("Linux OS detected. Program has not been tested on linux. Exiting program...")
        exit()

    driver.implicitly_wait(5)
    actions = ActionChains(driver)

    # Step 1: Handle Login
    driver.get(login_url)

    # Fetch username and password elements
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gfr-login-authentication-username"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gfr-login-authentication-password"))
    )

    # Input login credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
    )
    login_button.click()

    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Financials']"))
    )
    financials.click()

    transactions = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Transactions']"))
    )
    transactions.click()

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
    sleep(3)

    driver.get("https://restaurant.grubhub.com/financials/transactions/909517,909519,909523,909536")

    # Step 3: Set date range to the current date
    date_picker_input = driver.find_element(By.XPATH, "//input[@data-testid='export-modal-date-picker-input']")

    # Get the current date and format it as MM/DD/YYYY
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")

    date_picker_input.clear()
    date_picker_input.send_keys(f"{current_date} - {current_date}")
    sleep(3)

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
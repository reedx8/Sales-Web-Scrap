import os
import sys
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
        subtotal = row.find_element(By.XPATH, "./td[@class='gfr-table__row__cell'][2]").text

        # Store data in the dictionary
        subtotals[restaurant_name] = subtotal

    return subtotals

def run_grubhub():
    print("\nRunning Grubhub...")

    # Step 0: x3 path option for windows, else run for macs
    if sys.argv[1] == 'x3':
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        driver = webdriver.Chrome()
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

    # Click the "Show" button to reveal the password (if needed)
    show_password_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h6[text()='Show']"))
    )
    show_password_button.click()

    # Submit the login form
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']"))
    )
    login_button.click()

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
    
    driver.switch_to.window(driver.window_handles[0])
    sleep(5)

    # Step 3: Fetch subtotal data
    subtotals = fetch_subtotals(driver)

    # Print the fetched data (for testing purposes)
    for restaurant, subtotal in subtotals.items():
        print(f"{restaurant}: {subtotal}")

    # for store in all_stores:
    #     menu_btn = driver.find_element(By.XPATH, "//*[@id='wrapper']/div[1]/div[2]/div[2]/div[1]/div/div[1]/button")
    #     actions.move_to_element(menu_btn).click(menu_btn).perform()
    #     sleep(5)  # Needed. sleep(3) seconds wasn't always long enough wait for menu+element to load
    #     store_link = driver.find_element(By.XPATH, f"//p[text()='{store}']")
    #     sleep(1)
    #     actions.move_to_element(store_link).click(store_link).perform()
    #     sleep(10)

    #     sales = driver.find_element(By.XPATH, "//h5[@data-baseweb='typo-headingsmall']").text
    #     print(store, ": ", sales)

    #     if store == hall:
    #         all_sales["Hall"] = sales
    #     elif store == barrows:
    #         all_sales["Barrows"] = sales
    #     elif store == kruse:
    #         all_sales["Kruse"] = sales
    #     elif store == orenco:
    #         all_sales["Orenco"] = sales

     # Step 3: Select all locations
    location_selector = driver.find_element(By.XPATH, "//div[@aria-label='multi-location-selector']")
    actions.move_to_element(location_selector).click(location_selector).perform()
    sleep(2)

    # Step 4: Set date range to current date
    # Step 4: Set date range to current date
    date_picker_input = driver.find_element(By.XPATH, "//input[@data-testid='export-modal-date-picker-input']")
    date_picker_input.clear()
    date_picker_input.send_keys("01/23/2024 - 01/23/2024")

    # Click update button (with error handling)
    try:
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Update']"))
        )
        driver.execute_script("window.onerror = function(msg, url, line, col, error) { console.error('Error:', msg, 'URL:', url, 'Line:', line, 'Column:', col, 'Error object:', error); };")
        update_button.click()
    except NoSuchElementException:
        print("Failed to locate the 'Update' button.")
        driver.quit()
        sys.exit(1)
    except TimeoutException:
        print("Timed out waiting for the 'Update' button to be clickable.")
        driver.quit()
        sys.exit(1)

    sleep(5)  # Add a sleep here to wait for the page to update
    
    # Step 3: Send live sales data to spreadsheet
    send_data(all_sales, "grubhub")

    # Step 4: Quit selenium properly, and exit program. Done. 
    driver.quit()

# Run the function if this script is executed
if __name__ == "__main__":
    run_grubhub()

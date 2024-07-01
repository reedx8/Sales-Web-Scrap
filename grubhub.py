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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import platform
from selenium_stealth import stealth

def resource_path(relative_path):
    """Get the absolute path to the resource, works for development and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

env_path = resource_path(os.path.join('assets', '.env'))
load_dotenv(env_path)

options = ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1200,600")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

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
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'fin-transactions-display__transaction-totals')]"))
    )
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    subtotals = {}
    for row in rows:
        restaurant_name = row.find_element(By.XPATH, "./td[@class='gfr-table__row__cell fin-transactions-display__table-data--ceil']").text
        subtotal = row.find_element(By.XPATH, "./td[@class='gfr-table__row__cell'][1]").text
        if "meadows" in str(restaurant_name).lower():
            subtotals["Kruse"] = subtotal[1:]
        elif "orenco" in str(restaurant_name).lower():
            subtotals["Orenco"] = subtotal[1:]
        elif "barrows" in str(restaurant_name).lower():
            subtotals["Barrows"] = subtotal[1:]
        elif "hall" in str(restaurant_name).lower():
            subtotals["Hall"] = subtotal[1:]
    return subtotals

def run_grubhub():
    print("\nRunning Grubhub...")

    currentOS = platform.system().lower()
    if currentOS == "darwin":
        driver = webdriver.Chrome(options=options)
    elif currentOS == "windows":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        print("Linux OS detected. Program has not been tested on linux. Exiting program...")
        exit()

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.implicitly_wait(5)
    actions = ActionChains(driver)
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
    except Exception as e:
        print("\nCould not log in")
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
        print("Sign in button clicked, or couldn't log in. Continuing anyways...")

    driver.switch_to.window(driver.window_handles[0])
    sleep(2)
    max_attempts = 1 
    for attempt in range(max_attempts):
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
                print(f"Grubhub: Waiting for user to pass login security check... (Attempt: {attempt+1}/{max_attempts})")
                sleep(2)
    
    driver.get("https://restaurant.grubhub.com/financials/transactions/909517,909519,909523,909536")
    sleep(1)

    try:
        date_picker_input = driver.find_element(By.XPATH, "//input[@data-testid='export-modal-date-picker-input']")
        current_date = datetime.datetime.now().strftime("%m/%d/%Y")
        date_picker_input.clear()
        date_picker_input.send_keys(f"{current_date} - {current_date}")
    except Exception as e:
        print("Blocked by Login Security check screen")
        print("Error message shown below:\n")
        print(e)
        driver.quit()
        return 2

    sleep(2)

    subtotals = fetch_subtotals(driver)

    send_data(subtotals, "grubhub")

    driver.quit()
    return subtotals

if __name__ == "__main__":
    run_grubhub()

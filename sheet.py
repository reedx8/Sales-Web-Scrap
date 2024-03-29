import os
import sys
import pygsheets
import pandas as pd
from datetime import datetime

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Authorization: Add path to your google api credentials JSOn file here. 
# paths = [
#     '/Users/xvrmac/code/Sales-Web-Scrap/google_api_cred.json',
#     '/Users/xreed/code/Sales-Web-Scrap/google_api_cred.json',
#     'C:\\Users\\reedx\\Code\\Sales-Web-Scrap\\google_api_cred.json',
#     "D:\\Ava\\Sales-Web-Scrap\\google_api_cred.json",
#     "C:\\Users\\reedx\\Desktop\\code\\Sales-Web-Scrap\\google_api_cred.json"
# ]
pathFound = False

# for path in paths:
try:
    # gc = pygsheets.authorize(service_file=path)
    gc = pygsheets.authorize(service_file=resource_path(os.path.join("assets", "google_api_cred.json")))
    pathFound = True
    # break
except OSError as error:
    pass
except Exception as error:
    print("ERROR: ", error)
    exit()

if not pathFound:
    print("ERROR: App needs the correct path to the google api credentials JSON file")
    print("Exiting program...")
    exit()


# Sends live sales data to google spreadsheet ("Live Sales" spreadsheet)
def send_data(sales_data, platform):
    # Create empty dataframe
    df = pd.DataFrame()

    # open the google spreadsheet
    ss = gc.open_by_key('1deyIpmet1Fa9bRqAI9IbRpMC60Z1NmM3Jt6cOFOwZe0')

    # select "todays sales" sheet
    sh = ss.worksheet("title", "Today's Sales")

    # Create a column with Doordash/Revel column title and its sales_data
    # Ensure to insert sales data in the following order: Hall, Barrows, Kruse, then Orenco
    if platform.lower() == "doordash":
        df['Doordash'] = [
            sales_data['Hall'],
            sales_data['Barrows'],
            sales_data['Kruse'],
            sales_data['Orenco']
        ]
        # Update sheet with df, starting at cell C1 (Doordash)
        sh.set_dataframe(df, (1, 3))  # set_dataframe(df, (row, column))
    elif platform.lower() == "revel":
        df['Revel'] = [
            sales_data['Hall'],
            sales_data['Barrows'],
            sales_data['Kruse'],
            sales_data['Orenco']
        ]
        sh.set_dataframe(df, (1, 2))
    elif platform.lower() == "uber":
        df["Uber Eats"] = [
            sales_data['Hall'],
            sales_data['Barrows'],
            sales_data['Kruse'],
            sales_data['Orenco']
        ]
        sh.set_dataframe(df, (1, 5))
    elif platform.lower() == "grubhub":
        df["Grubhub"] = [
            sales_data['Hall'],
            sales_data['Barrows'],
            sales_data['Kruse'],
            sales_data['Orenco']
        ]
        sh.set_dataframe(df, (1, 4))
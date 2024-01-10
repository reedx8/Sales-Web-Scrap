'''
TODO:
- Grab today's date, output to the correct column in the sheet
'''
import sys
import pygsheets
import pandas as pd
from datetime import datetime

# authorization: replace with your own path option. The path is the file path to where your google_api_cred.json file is located on your machine.
try:
    if (sys.argv[1] == 'x'):
        # path option 1 ('x') -- Xavier's macbook machine
        path = '/Users/xreed/Desktop/web-scrap-ava/google_api_cred.json'
    elif (sys.argv[1] == 'x2'): 
        # path option 2 ('x2') -- Xavier's mac mini machine
        path = '/Users/xvrmac/code/Sales-Web-Scrap/google_api_cred.json'
    elif (sys.argv[1] == 'x3'):
        # path option 3 -- Xavier's asus windows machine
        path = 'C:\\Users\\reedx\\Code\\Sales-Web-Scrap\\google_api_cred.json'
    elif (sys.argv[1] == 'z'):
        # path option 4 -- zarrins office computer
        path = "D:\\Ava\\Sales-Web-Scrap\\google_api_cred.json"

except Exception as error:
    print("\n*************************")
    print("Exception: Missing command line argument (see sheet.py). Please try again.\n")
    print("Example: python3 doordash.py x2")
    print("'x' = Running on xavier's macbook")
    print("'x2' = Running on xavier's mac mini\n")
    print("Program terminated")
    print("*************************\n")
    print(error)
    print()
    exit()

gc = pygsheets.authorize(service_file=path)

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

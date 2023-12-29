'''
TODO:
- Grab todays date, output to correct column in sheet
'''

import pygsheets
import pandas as pd

# authorization: replace with your own path
path = '/Users/xreed/Desktop/web-scrap-ava/google_api_cred.json'
gc = pygsheets.authorize(service_file=path)

def send_data(store, platform):
    # Create empty dataframe
    df = pd.DataFrame()

    # open the google spreadsheet
    ss = gc.open_by_key('1deyIpmet1Fa9bRqAI9IbRpMC60Z1NmM3Jt6cOFOwZe0')

    # select "todays sales" sheet
    sh = ss.worksheet("title", "Today's Sales")

    # Create a column with Doordash/Revel column title and its data
    if (platform.lower() == "doordash"):
        df['Doordash'] = [
            store['Hall'],
            store['Barrows'],
            store['Kruse'],
            store['Orenco']
        ]
        # update sheet with df, starting at cell C1 (doordash)
        sh.set_dataframe(df,(1,3)) # set_dataframe(df, (row, column))
    elif (platform.lower() == "revel"):
        df['Revel'] = ['John', 'Steve', 'Sarah'] # dummy data
        sh.set_datafram(df, (1,2))

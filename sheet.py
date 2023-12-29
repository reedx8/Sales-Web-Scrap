import pygsheets
import pandas as pd

# authorization: replace with your own path
path = '/Users/xreed/Desktop/web-scrap-ava/google_api_cred.json'
gc = pygsheets.authorize(service_file=path)

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Live Sales')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))

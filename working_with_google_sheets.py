# install libraries using pip3 install pygsheets, gspread, oauth2client, pandas

# importing libraries
import pygsheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# gets sheet data as a pandas df
def get_sheet_as_df(sheetKey):  # get sheet key from the URL of your sheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # make sure you have given read permissions to your service account from the google sheets UI
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/path/to/credentials.json', scope)  # Your json file here
    

    sheet_key = sheetKey
    gc = gspread.authorize(credentials)

    # opening the first sheet in the spreadsheet
    # replace sheet1 with sheet of your choice
    wks = gc.open_by_key(sheet_key).sheet1 
    data = wks.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    return(df)


def overwrite_sheet_with_df(df, sheetKey):  # get sheet key from the URL of your sheet
    # make sure you have given write permissions to your service account from the google sheets UI
    gc = pygsheets.authorize(
        service_file='sylvan-fusion-266408-0853a45d4452.json')  # Your json file here
    
    # open the google spreadsheet
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/' + sheetKey)
    
    #select the first sheet
    wks = sh[0]
    
    # overwrite the first sheet with df
    wks.clear()
    wks.set_dataframe(df, 'A1')

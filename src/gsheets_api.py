import os
import pygsheets
import pandas as pd
from init import DIR_DUMPS, DIR_KEYS

if __name__ == '__main__':

    FILE_CREDENTIALS = [file for file in os.listdir(DIR_KEYS) if 'google_sheets_api' in file][0]
    FILE_CREDENTIALS = f'{DIR_KEYS}/{FILE_CREDENTIALS}'

    # # If modifying these scopes, delete the file token.pickle.
    # SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # # The ID and range of a sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1iKPrDlxORlyK5rX6Kpr6Yu1K-Okb0cjPvEX42ku9tuI'
    # SAMPLE_RANGE_NAME = 'Video:Summary'
    # main()

    gc = pygsheets.authorize(client_secret='/Users/majid/Dropbox/code/api_keys/google_sheets_api_credentials.json')
    gsheet = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1SSjcxmx-qWjqsG-whwK6-Qj4fkPGAxReRqHinJ5xZwE/edit#gid=0')
    dir(gsheet)
    gsheet._sheet_list
    # gsheet.worksheets()
    # dir(gsheet[1])
    # gsheet[1].get_all_records()
    # gsheet[1].get_as_df()
    # gsheet[1].title
    # gsheet[1].url

    for sheet in gsheet:
        # df_sheet = sheet.get_as_df()
        # dir(sheet)
        # sheet.get_all_records()[10]
        # sheet.get_col(3)
        df_sheet = pd.DataFrame(sheet.get_all_values())
        df_sheet['sheet_title'] = sheet.title
        df_sheet['sheet_url'] = sheet.url
        df_sheet.to_csv(f'{DIR_EF}/gdrive/df_google_sheet_{sheet.title}.csv', index=False)



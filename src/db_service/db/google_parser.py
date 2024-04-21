import gspread

class GoogleSheetParser:
    def __init__(self, credentials_filename, authorized_user_filename):
        self.gc = gspread.oauth(
            credentials_filename=credentials_filename,
            authorized_user_filename=authorized_user_filename
        )
    
    def __exit__(self):
        if self.gc is not None:
            self.gc.session.close()

    def get_worksheet(self, table_name: str, sheet_name: str):
        if self.gc is not None:
            self.tb = self.gc.open(table_name)
            return self.tb.worksheet(sheet_name).get_all_values()

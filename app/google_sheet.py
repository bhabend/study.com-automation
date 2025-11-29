import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GoogleSheet:
    def __init__(self):
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        creds = Credentials.from_service_account_info(json.loads(creds_json))
        self.service = build("sheets", "v4", credentials=creds)

    def fetch_input_rows(self):
        # Expect columns: Degree | URL
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range="Raw Data!A2:B"
        ).execute()
        rows = result.get("values", [])
        return [{"degree": r[0], "url": r[1]} for r in rows if len(r) >= 2]

    def push_output(self, rows):
        output = [[r["degree"], r["final"]] for r in rows]
        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range="Processed Data!A2",
            valueInputOption="RAW",
            body={"values": output}
        ).execute()

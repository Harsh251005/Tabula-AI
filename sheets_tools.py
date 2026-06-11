from googleapiclient.discovery import build

from google_auth import authenticate


def create_spreadsheet(title: str):
    creds = authenticate()

    service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    spreadsheet = {
        "properties": {
            "title": title
        }
    }

    result = (
        service.spreadsheets()
        .create(body=spreadsheet)
        .execute()
    )

    return {
        "spreadsheet_id": result["spreadsheetId"],
        "spreadsheet_url": result["spreadsheetUrl"],
    }
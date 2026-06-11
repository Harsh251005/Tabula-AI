from googleapiclient.discovery import build

from google_auth import authenticate


def get_sheets_service():
    """
    Returns an authenticated Google Sheets service.
    """
    creds = authenticate()
    return build("sheets", "v4", credentials=creds)


def create_spreadsheet(title: str) -> dict:
    """
    Creates a new Google Spreadsheet.
    """
    service = get_sheets_service()

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


def read_range(
    spreadsheet_id: str,
    range_name: str
) -> list:
    """
    Reads values from a specified range.
    Example range: 'A1:C10'
    """
    service = get_sheets_service()

    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        )
        .execute()
    )

    return result.get("values", [])

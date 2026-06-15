from agents import function_tool
from tabula_ai.tools.sheets_service import get_sheets_service


@function_tool
def create_spreadsheet(title: str) -> dict:
    """
    Creates a new Google Spreadsheet.
    """
    service = get_sheets_service()

    print(f"[TOOL] Creating new spreadsheet with title {title}")

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
from tabula_ai.tools.sheets_service import get_sheets_service
from agents import function_tool

@function_tool
def evaluate_formula(spreadsheet_id: str, formula: str, temp_sheet: str = "_temp_eval") -> str:
    """
    Evaluates a formula against spreadsheet data and returns the result.
    Does NOT persist anything — cleans up after itself.
    Use this for any calculation the user wants answered conversationally.
    """
    service = get_sheets_service()

    # Write to a temp cell, read back, then clear
    sheet_range = f"{temp_sheet}!A1"

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        body={"values": [[formula]]}
    ).execute()

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()

    value = result.get("values", [[None]])[0][0]

    # Clear the temp cell
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()

    return str(value)
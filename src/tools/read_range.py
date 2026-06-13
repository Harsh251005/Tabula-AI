from agents import function_tool
from src.tools.sheets_service import get_sheets_service


@function_tool
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
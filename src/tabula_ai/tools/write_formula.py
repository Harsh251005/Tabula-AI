from agents import function_tool
from tabula_ai.tools.sheets_service import get_sheets_service


@function_tool
def write_formula(
    spreadsheet_id: str,
    sheet_name: str,
    cell: str,
    formula: str
) -> dict:
    """
    Writes a single formula to a cell. The formula stays live in the sheet.
    Use this for calculated columns, summaries, or any Excel/Sheets formula.
    Prefer this over run_code for simple calculations.
    
    Args:
        spreadsheet_id: The ID of the spreadsheet.
        sheet_name: Exact sheet name (e.g. 'Sheet1'). Get this from schema.
        cell: Target cell (e.g. 'D2', 'F10').
        formula: A valid Sheets formula starting with '='. e.g. '=SUM(A2:A100)'
    """
    service = get_sheets_service()

    print(f"[TOOL] Writing formula{formula} in {cell} to {sheet_name}")

    range_name = f"{sheet_name}!{cell}"

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",  # required for formulas to be evaluated
            body={"values": [[formula]]},
        )
        .execute()
    )

    return {
        "cell": result.get("updatedRange"),
        "formula": formula,
    }
# tabula_ai/runtime/sheets_runtime.py

from tabula_ai.tools.sheets_service import get_sheets_service


def runtime_append_rows(
    spreadsheet_id: str,
    sheet_name: str,
    values: list[list]
) -> dict:

    service = get_sheets_service()

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        )
        .execute()
    )

    updates = result.get("updates", {})

    return {
        "appended_range": updates.get("updatedRange"),
        "appended_rows": updates.get("updatedRows"),
        "appended_cells": updates.get("updatedCells"),
    }
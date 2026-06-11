from googleapiclient.discovery import build

from google_auth import authenticate

from langchain_core.tools import tool


def get_sheets_service():
    """
    Returns an authenticated Google Sheets service.
    """
    creds = authenticate()
    return build("sheets", "v4", credentials=creds)


@tool("create_spreadsheet")
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


@tool("read_range")
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


@tool("update_range")
def update_range(
    spreadsheet_id: str,
    range_name: str,
    values: list[list]
) -> dict:
    """
    Updates a range with provided values.
    """
    service = get_sheets_service()

    body = {
        "values": values
    }

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        )
        .execute()
    )

    return result


@tool("append_rows")
def append_rows(
    spreadsheet_id: str,
    range_name: str,
    values: list[list]
) -> dict:
    """
    Appends rows after the last non-empty row.
    """
    service = get_sheets_service()

    body = {
        "values": values
    }

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        )
        .execute()
    )

    return result

def get_sheet_metadata(
    spreadsheet_id: str
) -> dict:
    """
    Returns spreadsheet metadata including sheet names.
    """
    service = get_sheets_service()

    return (
        service.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id
        )
        .execute()
    )

@tool("get_sheet_schema")
def get_sheet_schema(spreadsheet_id: str) -> dict:
    """
    Returns sheet names, headers and dimensions.
    Useful for LLM context.
    """

    service = get_sheets_service()

    metadata = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id)
        .execute()
    )

    sheets_info = []

    for sheet in metadata["sheets"]:

        title = sheet["properties"]["title"]
        row_count = sheet["properties"]["gridProperties"]["rowCount"]
        column_count = sheet["properties"]["gridProperties"]["columnCount"]

        try:
            header_result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=f"{title}!1:1"
                )
                .execute()
            )

            headers = header_result.get("values", [[]])[0]

        except Exception:
            headers = []

        sheets_info.append(
            {
                "sheet_name": title,
                "row_count": row_count,
                "column_count": column_count,
                "headers": headers,
            }
        )

    return {
        "spreadsheet_title": metadata["properties"]["title"],
        "sheets": sheets_info,
    }

TOOLS = [
    create_spreadsheet,
    read_range,
    update_range,
    append_rows,
    get_sheet_schema
]
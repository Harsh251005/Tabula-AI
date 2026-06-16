from agents import function_tool

from tabula_ai.tools.drive_service import get_drive_service


@function_tool
def list_spreadsheets() -> dict:
    """
    Lists all Google Spreadsheets available to the authenticated user.
    """

    print("[TOOL] Getting Google Spreadsheets")

    service = get_drive_service()

    results = (
        service.files()
        .list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            fields="files(id,name)"
        )
        .execute()
    )

    spreadsheets = results.get("files", [])

    return {
        "spreadsheets": spreadsheets
    }
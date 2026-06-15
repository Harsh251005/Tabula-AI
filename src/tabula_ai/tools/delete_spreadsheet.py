from agents import function_tool
from googleapiclient.discovery import build
from typing import Annotated


@function_tool
def delete_spreadsheet(
    spreadsheet_id: Annotated[
        str,
        "The Google Spreadsheet ID to delete."
    ],
) -> str:
    """
    Permanently moves a Google Spreadsheet to trash.
    """

    from tabula_ai.authentication.google_auth import authenticate

    creds = authenticate()

    drive_service = build(
        "drive",
        "v3",
        credentials=creds,
    )

    try:
        # Move file to trash instead of hard delete
        drive_service.files().update(
            fileId=spreadsheet_id,
            body={"trashed": True},
        ).execute()

        return (
            f"Spreadsheet {spreadsheet_id} was successfully moved to trash."
        )

    except Exception as e:
        return f"Failed to delete spreadsheet: {str(e)}"
from rapidfuzz import process, fuzz

from agents import function_tool
from tabula_ai.tools.drive_service import get_drive_service


@function_tool
def find_spreadsheet(
    name: str,
    limit: int = 10,
    score_cutoff: int = 60,
) -> dict:
    """
    Find spreadsheets using fuzzy matching.

    Args:
        name: Search query.
        limit: Maximum number of results.
        score_cutoff: Minimum similarity score (0-100).

    Returns:
        Ranked spreadsheet matches.
    """

    print(f"[TOOL] Finding spreadsheet similar to: {name}")

    service = get_drive_service()

    results = (
        service.files()
        .list(
            q=(
                "mimeType='application/vnd.google-apps.spreadsheet' "
                "and trashed=false"
            ),
            fields="files(id,name)",
            pageSize=1000,
        )
        .execute()
    )

    files = results.get("files", [])

    if not files:
        return {
            "query": name,
            "matches": [],
        }

    # Map normalized names to file metadata
    name_to_file = {}

    for file in files:
        normalized_name = " ".join(
            file["name"].lower().strip().split()
        )
        name_to_file[normalized_name] = file

    query = " ".join(name.lower().strip().split())

    matches = process.extract(
        query,
        name_to_file.keys(),
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=score_cutoff,
    )

    return {
        "query": name,
        "matches": [
            {
                "id": name_to_file[matched_name]["id"],
                "name": name_to_file[matched_name]["name"],
                "score": round(score, 2),
            }
            for matched_name, score, _ in matches
        ],
    }
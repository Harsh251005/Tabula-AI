from pydantic import BaseModel
from typing import List, Optional


class ColumnInfo(BaseModel):
    name: str
    data_type: str


class SheetInfo(BaseModel):
    sheet_name: str
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    columns: List[ColumnInfo]


class SpreadsheetContext(BaseModel):
    spreadsheet_id: str
    spreadsheet_name: str

    active_sheet: Optional[str] = None

    sheets: List[SheetInfo]

    discovery_confidence: float

    reasoning: str
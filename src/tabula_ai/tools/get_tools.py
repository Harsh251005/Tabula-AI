from tabula_ai.tools.create_spreadsheet import create_spreadsheet
from tabula_ai.tools.get_spreadsheet_schema import get_spreadsheet_schema
from tabula_ai.tools.open_spreadsheet import open_spreadsheet
from tabula_ai.tools.read_range import read_range
from tabula_ai.tools.web_search import web_search
from tabula_ai.tools.write_range import write_range
from tabula_ai.tools.append_rows import append_rows
from tabula_ai.tools.write_formula import write_formula
from tabula_ai.tools.clear_range import clear_range
from tabula_ai.tools.add_sheet import add_sheet
from tabula_ai.tools.delete_sheet import delete_sheet
from tabula_ai.tools.evaluate_formula import evaluate_formula
from tabula_ai.tools.delete_spreadsheet import delete_spreadsheet
from tabula_ai.tools.rename_spreadsheet import rename_spreadsheet
from tabula_ai.tools.monitor_spreadsheet import monitor_spreadsheet
from tabula_ai.tools.code_execution import execute_python

TOOLS = [
    create_spreadsheet,
    read_range,
    web_search,
    get_spreadsheet_schema,
    write_range,
    open_spreadsheet,
    append_rows,
    write_formula,
    clear_range,
    add_sheet,
    delete_sheet,
    evaluate_formula,
    delete_spreadsheet,
    rename_spreadsheet,
    execute_python
]
from config.settings import settings

from src.tools.create_spreadsheet import create_spreadsheet
from src.tools.read_range import read_range
from src.tools.web_search import web_search
from src.tools.get_spreadsheet_schema import get_spreadsheet_schema
from src.tools.write_range import write_range
from src.tools.open_spreadsheet import open_spreadsheet

from src.instructions.sheet_agent_instruction import sheets_agent_instruction

from agents import Agent, Runner

SPREADSHEET_ID = "1DJjlO0OnrFJq0uUw_Ac_w5a_fdCvHDK6BGMcTiVIZnc"

agent = Agent(
    name="Sheets_Agent",
    model=settings.MODEL_NAME,
    instructions=sheets_agent_instruction(spreadsheet_id=SPREADSHEET_ID),
    tools=[
        create_spreadsheet,
        read_range,
        web_search,
        get_spreadsheet_schema,
        write_range,
        open_spreadsheet
    ]
)

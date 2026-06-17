from src.tabula_ai.tools.create_spreadsheet import create_spreadsheet
from src.tabula_ai.tools.rename_spreadsheet import rename_spreadsheet
from src.tabula_ai.tools.delete_spreadsheet import delete_spreadsheet
from src.tabula_ai.tools.delete_sheet import delete_sheet
from tabula_ai.ai_agents.discovery_agent.agent import discovery_agent_tool
from tabula_ai.ai_agents.formula_agent.agent import formula_agent_tool

SUPERVISOR_AGENT_TOOLS = [
    discovery_agent_tool, formula_agent_tool, create_spreadsheet, rename_spreadsheet, delete_spreadsheet, delete_sheet
]
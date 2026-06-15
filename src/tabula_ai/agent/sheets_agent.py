from agents import Agent
from tabula_ai.config.settings import settings
from tabula_ai.instructions.sheet_agent_instruction import sheets_agent_instruction
from tabula_ai.tools.get_tools import TOOLS

agent = Agent(
    name="Sheets_Agent",
    model=settings.MODEL_NAME,
    instructions=sheets_agent_instruction(),
    tools=TOOLS
)
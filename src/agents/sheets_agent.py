from config.settings import settings
from src.instructions.sheet_agent_instruction import sheets_agent_instruction
from src.tools.get_tools import TOOLS


from agents import Agent, Runner

agent = Agent(
    name="Sheets_Agent",
    model=settings.MODEL_NAME,
    instructions=sheets_agent_instruction(),
    tools=TOOLS
)

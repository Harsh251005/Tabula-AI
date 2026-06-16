from src.tabula_ai.config.settings import settings
from .instructions import discovery_agent_instruction
from .tools import DISCOVERY_TOOLS
from .schema import SpreadsheetContext

from agents import Agent

discovery_agent = Agent(
    name="discovery_agent",
    model=settings.MODEL_NAME,
    instructions=discovery_agent_instruction(),
    tools = DISCOVERY_TOOLS,
    output_type=SpreadsheetContext
)

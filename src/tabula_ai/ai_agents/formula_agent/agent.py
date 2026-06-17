from agents import Agent

from tabula_ai.config.settings import settings
from .instructions import formula_agent_instructions
from .tools import FORMULA_TOOLS

formula_agent = Agent(
    name="formula_agent",
    model=settings.MODEL_NAME,
    instructions=formula_agent_instructions(),
    tools=FORMULA_TOOLS
)

formula_agent_tool = formula_agent.as_tool(
    tool_name="formula_agent_tool",
    tool_description="Formula Agent Tool responsible for writing, testing and self-correcting spreadsheet formulas"
)
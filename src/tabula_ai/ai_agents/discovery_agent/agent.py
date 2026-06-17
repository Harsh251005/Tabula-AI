from tabula_ai.config.settings import settings
from .instructions import discovery_agent_instruction
from .tools import DISCOVERY_TOOLS

from agents import Agent

discovery_agent = Agent(
    name="discovery_agent",
    model=settings.MODEL_NAME,
    instructions=discovery_agent_instruction(),
    tools = DISCOVERY_TOOLS,
)

discovery_agent_tool = discovery_agent.as_tool(
    tool_name="discovery_agent_tool",
    tool_description="Discovery Agent Tool responsible to locate right spreadsheet and extract it's schema so downstream agents can act on real data"
)
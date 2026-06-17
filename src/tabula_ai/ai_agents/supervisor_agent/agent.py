from agents import Agent

from tabula_ai.config.settings import settings
from .instructions import supervisor_agent_instructions
from .tools import SUPERVISOR_AGENT_TOOLS

supervisor_agent = Agent(
    name="supervisor_agent",
    model=settings.MODEL_NAME,
    instructions=supervisor_agent_instructions(),
    tools = SUPERVISOR_AGENT_TOOLS
)
from agents import Agent

from tabula_ai.config.settings import settings
from tabula_ai.instructions.supervisor_agent_instructions import supervisor_agent_instructions
from tabula_ai.agent.workspace_agent import workspace_tool
from tabula_ai.tools.list_spreadsheets import list_spreadsheets

supervisor_agent = Agent(
    name="supervisor_agent",
    model=settings.MODEL_NAME,
    instructions=supervisor_agent_instructions(),
    tools=[list_spreadsheets, workspace_tool]
)

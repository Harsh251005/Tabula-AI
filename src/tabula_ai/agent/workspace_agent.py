from agents import Agent

from tabula_ai.tools.get_tools import workspace_admin_tools
from tabula_ai.instructions.workspace_agent_instruction import workspace_agent_instruction

from tabula_ai.config.settings import settings


workspace_admin_agent = Agent(
    name="workspace_admin_agent",
    model=settings.MODEL_NAME,
    handoff_description=(
        "Handles spreadsheet lifecycle operations such as "
        "creating, opening, renaming, deleting, and monitoring spreadsheets."
    ),
    instructions=workspace_agent_instruction(),
    tools = workspace_admin_tools
)

workspace_tool = workspace_admin_agent.as_tool(
    tool_name="workspace_admin",
    tool_description="Creates, opens, renames and deletes spreadsheets."
)

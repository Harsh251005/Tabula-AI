from agents import Agent, Runner

from tabula_ai.tools.get_tools import workspace_admin_tools
from tabula_ai.instructions.workspace_agent_instruction import workspace_agent_instruction
import asyncio

from tabula_ai.config.settings import settings


workspace_admin_agent = Agent(
    name="Workspace Admin Agent",
    model=settings.MODEL_NAME,
    instructions=workspace_agent_instruction(),
    tools = workspace_admin_tools
)


async def _run():

    while True:
        try:
            user_input = input("User: ").strip()

            if user_input.lower() == "exit":
                break

            result = await Runner.run(
                workspace_admin_agent,
                input=user_input
            )

            print(f"\nAgent: {result.final_output}\n")

        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    asyncio.run(_run())
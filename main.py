from src.tabula_ai.ai_agents.discovery_agent.agent import discovery_agent
import asyncio
from agents import Runner

async def main():
    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        result = await Runner.run(discovery_agent, user_input)
        response = result.final_output
        print(response, "\n")

if __name__ == "__main__":
    asyncio.run(main())
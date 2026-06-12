import asyncio
from src.agents.sheets_agent import agent
from agents import Runner


async def main():

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        result = await Runner.run(agent, user_input)
        print(f"TabulaAI: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

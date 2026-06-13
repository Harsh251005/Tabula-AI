import asyncio
from src.agents.sheets_agent import agent
from agents import Runner


async def main():
    SPREADSHEET_ID = input("Enter spreadsheet ID: ")

    if not SPREADSHEET_ID:
        print("Spreadsheet ID invalid or not provided")
        exit()

    while True:

        user_input = input("User: ")

        if user_input.lower() == "exit":
            break

        context = f"""
user input: {user_input}
spreadsheet ID: {SPREADSHEET_ID}
"""

        result = await Runner.run(agent, context)
        print(f"TabulaAI: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

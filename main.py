from multiprocessing import context

from agent import run_agent

def main():

    SPREADSHEET_ID = "19aNDs4yLdmDgQ2u49DJlDOFUf8aZ0H8t59QmcUvhtcQ"

    user_query = "Remove all the duplicate data present in the sheet"

    response = run_agent(user_query=user_query, spreadsheet_id=SPREADSHEET_ID)

    print(f"Tool Call: {response.tool_calls}")
    print(response.content)


if __name__ == "__main__":
    main()
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from tools.sheets_tools import TOOLS
from prompts.agent_prompt import AGENT_PROMPT
from config.settings import settings
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    api_key=settings.OPENAI_API_KEY
)

llm_with_tools = llm.bind_tools(TOOLS)

# Build a name → callable map for tool dispatch
TOOLS_MAP = {tool.name: tool for tool in TOOLS}


def run_agent(user_query: str, spreadsheet_id: str):
    system_prompt = f"""{AGENT_PROMPT}

    Current Spreadsheet ID:
    {spreadsheet_id}"""

    messages = [
        HumanMessage(content=f"{system_prompt}\n\nUser Request: {user_query}")
    ]

    while True:
        response: AIMessage = llm_with_tools.invoke(messages)
        messages.append(response)

        # No tool calls → final answer, break out
        if not response.tool_calls:
            break

        # Execute each tool call and collect results
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name not in TOOLS_MAP:
                tool_result = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    tool_result = TOOLS_MAP[tool_name].invoke(tool_args)
                except Exception as e:
                    tool_result = f"Error executing {tool_name}: {str(e)}"

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )

    return response  # Final AIMessage with no tool calls
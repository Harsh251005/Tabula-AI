from agents import function_tool
from tavily import AsyncTavilyClient
from tabula_ai.config.settings import settings


@function_tool
async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for a given query."""
    print(f"[TOOL] Searching for {query}")
    client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
    response = await client.search(query, max_results=max_results)
    results = [
        f"[{i+1}] {r['title']}\n{r['content']}\nURL: {r['url']}"
        for i, r in enumerate(response["results"])
    ]
    return "\n\n".join(results) if results else "No results found."

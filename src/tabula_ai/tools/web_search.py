import asyncio
import time
from agents import function_tool
from tavily import AsyncTavilyClient
from config.settings import settings

def _get_client() -> AsyncTavilyClient:
    api_key = settings.TAVILY_API_KEY
    if not api_key:
        raise EnvironmentError(
            "TAVILY_API_KEY not set. Get a free key at https://tavily.com "
            "and add it to your ~/.tabula/.env file."
        )
    return AsyncTavilyClient(api_key=api_key)


async def _search_one(client: AsyncTavilyClient, query: str) -> dict:
    """Run a single Tavily search and return structured, LLM-ready results."""
    try:
        print(f"[TOOL] Searching for {query}")

        response = await client.search(
            query=query,
            search_depth="advanced",       # deep crawl, not just snippets
            include_answer=True,           # Tavily's own AI-generated summary
            include_raw_content=False,     # keep payload lean
            max_results=5,
        )

        results = []
        for r in response.get("results", []):
            score = r.get("score", 0)
            if score < 0.3:                # drop low-confidence results
                continue
            results.append({
                "title":   r.get("title", "").strip(),
                "url":     r.get("url", ""),
                "summary": r.get("content", "").strip()[:600],  # cap per-result length
                "score":   round(score, 2),
            })

        # sort by relevance score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query":          query,
            "direct_answer":  response.get("answer", "").strip(),
            "results":        results,
            "error":          None,
        }

    except Exception as e:
        return {
            "query":         query,
            "direct_answer": "",
            "results":       [],
            "error":         str(e),
        }


async def _parallel_search(queries: list[str]) -> list[dict]:
    """Fire all queries simultaneously using asyncio.gather."""
    client = _get_client()
    tasks = [_search_one(client, q) for q in queries]
    return await asyncio.gather(*tasks)


def _deduplicate(search_outputs: list[dict]) -> list[dict]:
    """Remove duplicate URLs across results from different queries."""
    seen_urls = set()
    for output in search_outputs:
        unique = []
        for r in output["results"]:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique.append(r)
        output["results"] = unique
    return search_outputs


def _format_for_llm(search_outputs: list[dict]) -> str:
    """
    Render search results into a compact, structured string
    the LLM can reason over directly — no noise, no filler.
    """
    sections = []

    for output in search_outputs:
        query   = output["query"]
        answer  = output["direct_answer"]
        results = output["results"]
        error   = output["error"]

        if error:
            sections.append(f"## Query: {query}\n⚠ Search failed: {error}")
            continue

        block = [f"## Query: {query}"]

        if answer:
            block.append(f"**Direct Answer:** {answer}")

        if results:
            block.append("**Top Sources:**")
            for i, r in enumerate(results, 1):
                block.append(
                    f"{i}. [{r['title']}]({r['url']}) — relevance {r['score']}\n"
                    f"   {r['summary']}"
                )
        else:
            block.append("No high-confidence results found.")

        sections.append("\n".join(block))

    return "\n\n---\n\n".join(sections)


@function_tool
def web_search(queries: list[str]) -> str:
    """
    Search the web in parallel across multiple queries simultaneously.

    Use this when you need current information, recent news, facts beyond
    your training data, or any topic requiring live web results.

    Args:
        queries: List of search queries to run in parallel.
                 Each query should be specific and self-contained.
                 Example: ["AI ethics news June 2025", "EU AI Act updates 2025"]

    Returns:
        Structured search results for all queries, formatted for direct reasoning.
        Each query includes a direct AI-generated answer + top ranked sources.
    """
    if not queries:
        return "No queries provided."

    if len(queries) > 10:
        return "Maximum 10 parallel queries allowed per call. Split into multiple calls if needed."

    # strip empty/whitespace queries
    queries = [q.strip() for q in queries if q.strip()]

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # inside an already-running event loop (e.g. Jupyter / async context)
            import nest_asyncio
            nest_asyncio.apply()
            results = loop.run_until_complete(_parallel_search(queries))
        else:
            results = asyncio.run(_parallel_search(queries))
    except RuntimeError:
        results = asyncio.run(_parallel_search(queries))

    results = _deduplicate(results)
    return _format_for_llm(results)
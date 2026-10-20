# Tabula AI: your spreadsheets, controlled by conversation

![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB)
![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI-Agents%20SDK-412991)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A terminal app for working on Google Sheets in plain English. Pick a
spreadsheet from your Drive, then ask: "what's the total revenue by
region?", "put a running balance in column F", "make a new sheet called
Q3". A supervisor agent works out what you mean and hands the work to
specialised agents.

## How it works

```
             you (terminal, rich UI)
                       │
                       ▼
               Supervisor agent ── create / rename / delete files and tabs
                       │               (asks before anything destructive)
      ┌────────────────┴─┐
      ▼                  ▼
 Discovery agent     Formula agent
 finds the right     writes a formula, evaluates it in a
 spreadsheet and     scratch cell, reads the result back,
 extracts its        and corrects itself before writing
 schema              the final formula; looks up Sheets
                     quirks with Tavily web search
```

- **Multi-agent, OpenAI Agents SDK.** The discovery and formula agents are
  exposed to the supervisor as tools (`Agent.as_tool`). The supervisor
  classifies each request (read, write, formula, management, mixed,
  ambiguous), plans the order of calls, and keeps the active file and
  schema so it doesn't rediscover them every turn.
- **Safety gates.** The supervisor is instructed to state exactly what a
  delete will remove and wait for an explicit yes.
- **Memory across sessions.** Conversations are stored in SQLite
  (`~/.tabula_ai/tabula_memory.db`), keyed by your credentials and the
  spreadsheet, so reopening a sheet picks up where you left off.

## Run it

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/), and a Google Cloud
OAuth client (Desktop app) with the Sheets and Drive APIs enabled.

```bash
git clone https://github.com/Harsh251005/Tabula-AI.git
cd Tabula-AI
uv sync
cp .env.example .env      # OPENAI_API_KEY, TAVILY_API_KEY
uv run tabula-ai
```

On first launch Tabula asks for the path to your OAuth `credentials.json`,
opens a browser to sign in, then lists your spreadsheets. Inside a session:
`/switch` (open another spreadsheet), `/history`, `/clear`, `/help`, `/exit`.

## Stack

**Agents:** OpenAI Agents SDK (gpt-5-mini), Tavily search (parallel queries).
**Integrations:** Google Sheets and Drive APIs (OAuth).
**App:** Python 3.12, rich (terminal UI), SQLite, Pydantic, uv.

## Status

Working: the supervisor, discovery and formula agents, file and tab
management, session memory. Planned: a data agent for bulk reads, writes
and clean-up, and an Apps Script agent for automation beyond formulas.

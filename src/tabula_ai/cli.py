import asyncio
import sys
import shutil
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.live import Live
from rich.rule import Rule
from rich.table import Table
from rich import box
from rich.align import Align
from rich.padding import Padding

console = Console()

# ── Theme ─────────────────────────────────────────────────────────────────────

ACCENT      = "bright_white"
DIM         = "grey50"
PURPLE      = "medium_purple"
TEAL        = "cyan"
ERROR_CLR   = "red"
SUCCESS_CLR = "green"
USER_CLR    = "bright_white"
BOT_CLR     = "medium_purple"


# ── Branding ──────────────────────────────────────────────────────────────────

def print_banner():
    console.print()
    banner = Text()
    banner.append("  ████████╗ █████╗ ██████╗ ██╗   ██╗██╗      █████╗ \n", style="medium_purple bold")
    banner.append("     ██╔══╝██╔══██╗██╔══██╗██║   ██║██║     ██╔══██╗\n", style="medium_purple bold")
    banner.append("     ██║   ███████║██████╔╝██║   ██║██║     ███████║\n", style="medium_purple bold")
    banner.append("     ██║   ██╔══██║██╔══██╗██║   ██║██║     ██╔══██║\n", style="medium_purple bold")
    banner.append("     ██║   ██║  ██║██████╔╝╚██████╔╝███████╗██║  ██║\n", style="medium_purple bold")
    banner.append("     ╚═╝   ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝\n", style="medium_purple bold")
    console.print(Align.center(banner))
    console.print(Align.center(Text("Your spreadsheets, controlled by conversation.", style=f"{DIM} italic")))
    console.print()


def print_divider(label: str = ""):
    if label:
        console.print(Rule(f"[{DIM}] {label} [/{DIM}]", style=DIM))
    else:
        console.print(Rule(style=DIM))


# ── Setup wizard ──────────────────────────────────────────────────────────────

def run_setup() -> Path:
    config_dir = Path.home() / ".tabula"
    config_dir.mkdir(exist_ok=True)
    creds_dest = config_dir / "credentials.json"

    console.print(Panel(
        "[bold white]Welcome to Tabula![/bold white]\n\n"
        "Before we start, Tabula needs permission to access your Google Sheets.\n"
        f"[{DIM}]Don't worry — it only touches sheets you choose, nothing else.[/{DIM}]\n\n"
        f"[{DIM}]To get your credentials file:[/{DIM}]\n"
        f"  1. Go to [cyan]console.cloud.google.com[/cyan]\n"
        f"  2. Create a project → Enable Sheets + Drive APIs\n"
        f"  3. OAuth 2.0 → Desktop app → Download JSON\n",
        title="[medium_purple]  One-time Setup[/medium_purple]",
        border_style=PURPLE,
        padding=(1, 2),
    ))

    while True:
        raw = Prompt.ask(f"\n[{ACCENT}] Drop your credentials.json path here[/{ACCENT}]")
        path = Path(raw.strip().strip("'\"")).expanduser().resolve()

        if not path.exists():
            console.print(f"  [{ERROR_CLR}]✗  Can't find that file. Try again.[/{ERROR_CLR}]")
            continue
        if not path.suffix == ".json":
            console.print(f"  [{ERROR_CLR}]✗  That doesn't look like a .json file.[/{ERROR_CLR}]")
            continue

        shutil.copy(path, creds_dest)
        console.print(f"  [{SUCCESS_CLR}]✓  All set! Credentials saved.[/{SUCCESS_CLR}]")
        return creds_dest


def ensure_credentials() -> Path:
    config_dir = Path.home() / ".tabula"
    creds_path = config_dir / "credentials.json"
    if not creds_path.exists():
        return run_setup()
    return creds_path


def ensure_authenticated(creds_path: Path):
    import tabula_ai.authentication.google_auth as auth_module

    token_path = Path.home() / ".tabula" / "token.json"

    def patched_authenticate():
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = None
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                console.print()
                console.print(Panel(
                    "A browser window will open for Google sign-in.\n"
                    f"[{DIM}]Tabula only requests access to your spreadsheets — nothing else.[/{DIM}]",
                    title="[medium_purple]  Google Sign-in[/medium_purple]",
                    border_style=PURPLE,
                    padding=(1, 2),
                ))
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)

            token_path.parent.mkdir(exist_ok=True)
            with open(token_path, "w") as f:
                f.write(creds.to_json())

            console.print(f"  [{SUCCESS_CLR}]✓  Signed in successfully![/{SUCCESS_CLR}]")

        return creds

    auth_module.authenticate = patched_authenticate
    return patched_authenticate()


# ── Spreadsheet picker ────────────────────────────────────────────────────────

def pick_spreadsheet(creds) -> tuple[str, str]:
    from googleapiclient.discovery import build

    with Live(Spinner("dots", text=Text("  Fetching your spreadsheets...", style=DIM)), refresh_per_second=12):
        drive = build("drive", "v3", credentials=creds)
        results = drive.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            fields="files(id, name)",
            orderBy="modifiedTime desc",
            pageSize=20,
        ).execute()
        files = results.get("files", [])

    if not files:
        console.print(f"\n  [{ERROR_CLR}]No spreadsheets found in your Google Drive.[/{ERROR_CLR}]")
        sys.exit(1)

    console.print()
    print_divider("Pick a Spreadsheet")
    console.print()

    table = Table(
        box=box.SIMPLE,
        show_header=False,
        padding=(0, 2),
        border_style=DIM,
    )
    table.add_column("idx", style=PURPLE, width=5, justify="right")
    table.add_column("name", style=ACCENT)

    for i, f in enumerate(files, 1):
        table.add_row(f"{i}", f["name"])

    console.print(Padding(table, (0, 2)))
    console.print()

    while True:
        raw = Prompt.ask(f"[{ACCENT}]  Enter a number[/{ACCENT}] [{DIM}]or paste a URL / Sheet ID[/{DIM}]").strip()

        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(files):
                chosen = files[idx]
                return chosen["id"], chosen["name"]
            console.print(f"  [{ERROR_CLR}]✗  Pick a number between 1 and {len(files)}[/{ERROR_CLR}]")
            continue

        if "spreadsheets/d/" in raw:
            sid = raw.split("spreadsheets/d/")[1].split("/")[0]
            return sid, "Spreadsheet"

        if len(raw) > 20:
            return raw, "Spreadsheet"

        console.print(f"  [{ERROR_CLR}]✗  Not sure what that is — try a number, URL, or Sheet ID[/{ERROR_CLR}]")


# ── Message rendering ─────────────────────────────────────────────────────────

def render_user(message: str):
    ts = datetime.now().strftime("%I:%M %p")
    console.print()
    console.print(Align.right(
        Panel(
            Text(message, style=USER_CLR),
            border_style="grey30",
            padding=(0, 1),
            width=min(len(message) + 8, console.width - 10),
        )
    ))
    console.print(Align.right(Text(f"  {ts}", style=DIM)))


def render_assistant(message: str):
    ts = datetime.now().strftime("%I:%M %p")
    console.print()
    console.print(Panel(
        Markdown(message),
        title=Text("✦ Tabula", style=f"{BOT_CLR} bold"),
        title_align="left",
        border_style=PURPLE,
        padding=(0, 1),
        width=min(max(len(line) for line in message.splitlines() or [""]) + 10, console.width - 6),
    ))
    console.print(Text(f"  {ts}", style=DIM))


def render_error(message: str):
    console.print()
    console.print(Panel(
        Text(f"Something went wrong — {message}", style=ERROR_CLR),
        title="[red]Oops![/red]",
        border_style=ERROR_CLR,
        padding=(0, 1),
    ))


# ── Agent runner ──────────────────────────────────────────────────────────────

def run_agent(user_input: str, conversation_id: str, spreadsheet_id: str) -> str:
    from tabula_ai.agent.sheets_agent import agent
    from tabula_ai.db.memory import save_message, get_recent_messages
    from agents import Runner

    async def _run():
        save_message(conversation_id, role="user", content=user_input)

        history = get_recent_messages(conversation_id, limit=20)

        input_messages = [
            {"role": "user", "content": f"Active spreadsheet ID: {spreadsheet_id}"},
            {"role": "assistant", "content": "Got it."},
            *[{"role": m["role"], "content": m["content"]} for m in history],
        ]

        result = await Runner.run(agent, input=input_messages)
        response = result.final_output

        save_message(conversation_id, role="assistant", content=response)
        return response

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(_run())


# ── Help ──────────────────────────────────────────────────────────────────────

def print_help():
    console.print()
    console.print(Panel(
        f"[{PURPLE}]/switch[/{PURPLE}]   [{DIM}]Open a different spreadsheet[/{DIM}]\n"
        f"[{PURPLE}]/login[/{PURPLE}]    [{DIM}]Sign in with a different Google account[/{DIM}]\n"
        f"[{PURPLE}]/history[/{PURPLE}]  [{DIM}]See recent messages in this session[/{DIM}]\n"
        f"[{PURPLE}]/clear[/{PURPLE}]    [{DIM}]Clear the screen[/{DIM}]\n"
        f"[{PURPLE}]/help[/{PURPLE}]     [{DIM}]Show this message[/{DIM}]\n"
        f"[{PURPLE}]/exit[/{PURPLE}]     [{DIM}]Quit Tabula[/{DIM}]",
        title="[medium_purple]  Commands[/medium_purple]",
        border_style=DIM,
        padding=(1, 2),
    ))


# ── Main chat loop ────────────────────────────────────────────────────────────

def chat_loop(spreadsheet_id: str, spreadsheet_name: str, creds_hash: str):
    from tabula_ai.db.memory import get_or_create_conversation, get_recent_messages

    conversation_id = get_or_create_conversation(creds_hash, spreadsheet_id)

    msgs = get_recent_messages(conversation_id)
    if msgs:
        console.print(f"  [{DIM}]↩  Resuming previous conversation on this sheet.[/{DIM}]")

    console.print()
    print_divider()
    console.print(Align.center(Text(f"  {spreadsheet_name}", style=f"{ACCENT} bold")))
    console.print(Align.center(Text("Ask me anything about this sheet  ·  /help for commands", style=DIM)))
    print_divider()

    while True:
        try:
            console.print()
            user_input = Prompt.ask(f"[{ACCENT}]  You[/{ACCENT}]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n\n  [{DIM}]See you next time! 👋[/{DIM}]\n")
            break

        if not user_input:
            continue

        # ── Commands ──────────────────────────────────────────────────────────
        if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
            console.print(f"\n  [{DIM}]See you next time! 👋[/{DIM}]\n")
            break

        if user_input.lower() == "/help":
            print_help()
            continue

        if user_input.lower() == "/clear":
            console.clear()
            print_banner()
            continue

        if user_input.lower() == "/switch":
            return "switch"

        if user_input.lower() == "/login":
            console.print()
            console.print(Panel(
                "This will sign you out and open Google sign-in in your browser.\n"
                f"[{DIM}]Use this to switch to a different Google account.[/{DIM}]",
                title="[medium_purple]  Switch Account[/medium_purple]",
                border_style=PURPLE,
                padding=(1, 2),
            ))
            confirm = Prompt.ask(f"[{ACCENT}]  Continue?[/{ACCENT}] [{DIM}]yes / no[/{DIM}]").strip().lower()
            if confirm in ("yes", "y"):
                return "login"
            continue

        if user_input.lower() == "/history":
            msgs = get_recent_messages(conversation_id)
            if not msgs:
                console.print(f"  [{DIM}]No messages yet in this session.[/{DIM}]")
            else:
                console.print()
                print_divider("Conversation History")
                for m in msgs[-10:]:
                    ts = m["created_at"][:16].replace("T", "  ")
                    if m["role"] == "user":
                        console.print(f"  [{DIM}]{ts}[/{DIM}]  [{ACCENT}]You:[/{ACCENT}] {m['content']}")
                    else:
                        console.print(f"  [{DIM}]{ts}[/{DIM}]  [{BOT_CLR}]Tabula:[/{BOT_CLR}] {m['content'][:120]}{'...' if len(m['content']) > 120 else ''}")
                print_divider()
            continue

        # ── Agent call ────────────────────────────────────────────────────────
        render_user(user_input)

        with Live(
            Padding(Spinner("dots", text=Text("  Working on it...", style=DIM)), (0, 2)),
            refresh_per_second=12,
            transient=True,
        ):
            try:
                response = run_agent(user_input, conversation_id, spreadsheet_id)
            except Exception as e:
                render_error(str(e))
                continue

        render_assistant(response)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    from tabula_ai.db import init_db
    from tabula_ai.db.memory import get_credentials_hash

    init_db()
    print_banner()

    creds_path = ensure_credentials()
    creds = ensure_authenticated(creds_path)
    creds_hash = get_credentials_hash(creds_path)

    console.print(f"  [{SUCCESS_CLR}]✓[/{SUCCESS_CLR}]  Signed in and ready.")

    while True:
        sid, sname = pick_spreadsheet(creds)
        result = chat_loop(sid, sname, creds_hash)
        if result == "switch":
            continue
        if result == "login":
            token_path = Path.home() / ".tabula" / "token.json"
            if token_path.exists():
                token_path.unlink()
            console.print(f"\n  [{DIM}]Signing out...[/{DIM}]\n")
            main()
            return
        break


if __name__ == "__main__":
    main()
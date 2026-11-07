from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
from dotenv import load_dotenv

from jaxo.auth import authenticate
from jaxo.client import JaxoClient
from jaxo.brain import JaxoBrain
from jaxo.voice import VoiceEngine

console = Console()


def draw_home():
    """Render JAXO's Copilot-inspired terminal home screen."""
    console.clear()

    tabs = Text()
    tabs.append("[Current]", style="bold white on blue")
    tabs.append("  Sessions", style="bright_white")
    tabs.append("  Issues", style="dim")
    tabs.append("  Pull requests", style="dim")
    tabs.append("  Gists", style="dim")
    console.print(tabs)
    console.print()

    left = (
        "[bold bright_blue]▣  ▣[/bold bright_blue]\n"
        "[bold magenta]▰ ▣▣ ▰[/bold magenta]\n"
        "[bold magenta] ▣▣▣[/bold magenta]\n"
        "[white]JAXO uses AI.[/white]\n"
        "[dim]Check important results.[/dim]"
    )
    right = (
        "[bold bright_blue]Getting started[/bold bright_blue]\n"
        "[white]Chat with JAXO, build projects, inspect websites and write code.[/white]\n"
        "[white]/help[/white]  Show commands\n"
        "[white]/voice[/white]  Toggle spoken replies\n"
        "[white]/listen[/white]  Talk to JAXO"
    )
    intro = Table.grid(expand=True)
    intro.add_column(ratio=1)
    intro.add_column(ratio=2)
    intro.add_row(left, right)
    console.print(Panel(intro, border_style="bright_blue", padding=(1, 2), box=box.ROUNDED))
    console.print()
    console.print("[bright_blue]●[/bright_blue] JAXO ready · AI connection initialized · Workspace tools available")
    console.print()
    console.print("[dim]Type a message below. Use /help for commands.[/dim]")


def draw_footer():
    console.print()
    console.rule(style="dim")
    console.print(
        "[dim]↵ send  ·  / commands  ·  /help help  ·  /voice voice  ·  /exit quit[/dim]"
    )


def main():
    load_dotenv()
    if not authenticate(console):
        return

    try:
        client = JaxoClient()
        brain = JaxoBrain(client, console)
        voice = VoiceEngine(console)
        brain.voice = voice
    except Exception as exc:
        console.print(f"[red]Startup failed:[/] {exc}")
        return

    draw_home()

    while True:
        try:
            user_text = Prompt.ask("[bold bright_blue]❯[/bold bright_blue]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]JAXO signing off.[/dim]")
            break

        if not user_text:
            continue
        command = user_text.lower()

        if command in {"/exit", "/quit"}:
            console.print("[dim]JAXO signing off.[/dim]")
            break
        if command == "/help":
            console.print(
                "[bold bright_blue]JAXO commands[/bold bright_blue]\n"
                "  /help          Show commands\n"
                "  /tree          Show workspace files\n"
                "  /source        List JAXO source files\n"
                "  /source PATH   Read a JAXO source file\n"
                "  /self-check    Inspect JAXO source inventory\n"
                "  /evolve        Draft a self-improvement plan\n"
                "  /voice         Toggle spoken AI replies\n"
                "  /listen        Speak a prompt into your microphone\n"
                "  /clear         Return to the home screen\n"
                "  /exit          Quit JAXO\n"
            )
            continue
        if command == "/voice":
            voice.toggle()
            continue
        if command == "/listen":
            spoken_text = voice.listen()
            if spoken_text:
                console.print(f"[dim]You said:[/] {spoken_text}")
                brain.respond(spoken_text)
            continue
        if command == "/clear":
            draw_home()
            continue
        if command == "/tree":
            from jaxo.tools import workspace_tree
            console.print(Panel(workspace_tree(), title="Workspace", border_style="bright_blue"))
            continue
        if command == "/source" or command.startswith("/source "):
            from jaxo.tools import list_source_files, read_source_file
            path = user_text.partition(" ")[2].strip()
            if path:
                try:
                    console.print(Panel(read_source_file(path), title=f"JAXO source · {path}", border_style="cyan"))
                except Exception as exc:
                    console.print(f"[red]Cannot read source:[/] {exc}")
            else:
                console.print(Panel(list_source_files(), title="JAXO readable source files", border_style="cyan"))
            continue
        if command == "/self-check":
            from jaxo.tools import list_source_files
            console.print(Panel(list_source_files(), title="JAXO source inventory · read-only", border_style="green"))
            continue
        if command == "/evolve":
            from pathlib import Path
            from rich.prompt import Prompt as RichPrompt
            from jaxo.evolution.inspector import inspect_source
            from jaxo.evolution.planner import make_plan
            goal = RichPrompt.ask("What should JAXO improve?")
            findings = inspect_source(Path(__file__).resolve().parent)
            console.print(Panel(make_plan(goal, findings), title="Evolution Engine · proposal only", border_style="yellow"))
            console.print("[yellow]No source files were changed. Self-modification remains disabled.[/yellow]")
            continue

        brain.respond(user_text)

    client.close()


if __name__ == "__main__":
    main()

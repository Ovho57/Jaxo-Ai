from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from dotenv import load_dotenv

from jaxo.auth import authenticate
from jaxo.client import JaxoClient
from jaxo.brain import JaxoBrain

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold bright_green]J A X O[/bold bright_green]\n"
        "[dim]Your terminal. Your AI. Your workflow.[/dim]\n"
        "[dim green]General AI • Coding • Projects • Self-awareness[/dim green]",
        border_style="bright_green",
    ))


def main():
    load_dotenv()
    banner()
    if not authenticate(console):
        return

    try:
        brain = JaxoBrain(JaxoClient(), console)
    except Exception as exc:
        console.print(f"[red]Startup failed:[/] {exc}")
        return

    # Keep the banner for startup only; chat gets a clean terminal.
    console.clear()
    console.print("[dim]JAXO ready · /help for commands · /exit to quit[/dim]\n")

    while True:
        try:
            user_text = Prompt.ask("[bold bright_green]❯[/bold bright_green]").strip()
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
                "[bold]Commands[/bold]\n"
                "  /help          Show commands\n"
                "  /tree          Show workspace files\n"
                "  /source        List JAXO's readable source files\n"
                "  /source PATH   Read a JAXO source file\n"
                "  /self-check    Inspect JAXO source inventory\n"
                "  /evolve        Draft a self-improvement plan\n"
                "  /clear         Clear the terminal\n"
                "  /exit          Quit JAXO\n\n"
                "[dim]Or just talk naturally. Ask JAXO to explain its code, inspect a module, "
                "debug a project, write code, or build something.[/dim]\n"
            )
            continue
        if command == "/clear":
            console.clear()
            continue
        if command == "/tree":
            from jaxo.tools import workspace_tree
            console.print(workspace_tree())
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


if __name__ == "__main__":
    main()

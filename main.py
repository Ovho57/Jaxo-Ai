from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

from jaxo.auth import authenticate
from jaxo.client import JaxoClient
from jaxo.brain import JaxoBrain

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold bright_green]J A X O[/bold bright_green]\n[dim]Your terminal. Your AI. Your workflow.[/dim]\n[dim green]Standalone AI assistant • Project builder • Workspace tools[/dim green]",
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
        console.print(f"[red]Startup failed:[/red] {exc}")
        return

    console.print("[dim]Type naturally to chat. Use /help for commands, /exit to quit.[/dim]\n")
    while True:
        try:
            user_text = Prompt.ask("[bold bright_green]you[/bold bright_green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break
        if not user_text:
            continue
        if user_text.lower() in {"/exit", "/quit"}:
            console.print("[dim]JAXO signing off.[/dim]")
            break
        if user_text.lower() == "/help":
            console.print(Panel(
                "/help     Show commands\n"
                "/tree     Show the workspace tree\n"
                "/mkdir    Create a workspace folder\n"
                "/write    Create or replace a workspace file\n"
                "/clear    Clear the terminal\n"
                "/exit     Quit JAXO\n\n"
                "You can also ask JAXO in plain language to create project folders and files.",
                title="JAXO help", border_style="green"
            ))
            continue
        if user_text.lower() == "/self-check":
            from pathlib import Path
            from jaxo.evolution.inspector import inspect_source
            findings = inspect_source(Path(__file__).resolve().parent)
            console.print(Panel("\\n".join(findings) or "No Python source files found.", title="JAXO source inspection", border_style="green"))
            continue
        if user_text.lower() == "/evolve":
            from pathlib import Path
            from rich.prompt import Prompt as RichPrompt
            from jaxo.evolution.inspector import inspect_source
            from jaxo.evolution.planner import make_plan
            goal = RichPrompt.ask("What should JAXO improve?")
            findings = inspect_source(Path(__file__).resolve().parent)
            console.print(Panel(make_plan(goal, findings), title="Evolution Engine • proposal only", border_style="yellow"))
            console.print("[yellow]No source files were changed. Automatic patching is not enabled.[/yellow]")
            continue
        if user_text.lower() == "/clear":
            console.clear()
            continue
        if user_text.lower() == "/tree":
            from jaxo.tools import workspace_tree
            console.print(workspace_tree())
            continue
        if user_text.lower() == "/mkdir":
            name = Prompt.ask("Folder path (inside workspace)")
            from jaxo.tools import create_folder
            console.print(create_folder(name, console))
            continue
        if user_text.lower() == "/write":
            path = Prompt.ask("File path (inside workspace)")
            content = Prompt.ask("File content", default="")
            from jaxo.tools import create_file
            console.print(create_file(path, content, console))
            continue
        brain.respond(user_text)


if __name__ == "__main__":
    main()

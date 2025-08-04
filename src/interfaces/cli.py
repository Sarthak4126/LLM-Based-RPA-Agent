# src/interfaces/cli.py
import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# We import the new central workflow function
from src.core.workflow import run_automation_workflow

# The alias expander stays here as it's CLI-related
def expand_simple_task(goal: str) -> str:
    if not goal: return ""
    parts = goal.lower().split()
    command = parts[0]
    args = " ".join(parts[1:])
    
    app_aliases = { "notepad": f"Open notepad and type '{args}'", "calc": "Open calculator" }
    web_aliases = { "google": f"On google, search for '{args}'", "youtube": f"On youtube, search for and play '{args}'"}

    if command in app_aliases and args: return app_aliases[command]
    if command in app_aliases: return app_aliases[command]
    if command in web_aliases and args: return web_aliases[command]
    
    return goal

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="OpenAgent-Lite CLI")
    parser.add_argument('--goal', help='The natural language goal for the agent.')
    parser.add_argument('--keep-open', action='store_true', help='Keep the browser open after finishing.')
    args = parser.parse_args()
    
    is_interactive = not args.goal 
    
    raw_goal_text = ""
    if is_interactive:
        console.print("\n💬 [bold cyan]Enter your goal for the agent:[/bold cyan]")
        raw_goal_text = input("   > ").strip()
    else:
        raw_goal_text = args.goal.strip()

    if not raw_goal_text:
        console.print("[bold red]No goal provided. Exiting.[/bold red]"); return
    
    # Define a simple print callback for the CLI
    def cli_output(message):
        print(message, end='')

    # Run the workflow
    run_automation_workflow(raw_goal_text, args.keep_open, is_interactive, cli_output)

    # The waiting logic for CLI needs to be handled here if needed
    # but the current structure handles it implicitly.

if __name__ == "__main__":
    main()
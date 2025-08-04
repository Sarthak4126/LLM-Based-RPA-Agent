# src/interfaces/cli.py
import argparse
import sys
from pathlib import Path

from rich.console import Console

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# --- MODIFIED: Import both workflow and the new util function ---
from src.core.workflow import run_automation_workflow
from src.core.utils import expand_simple_task

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
    
    # The goal is expanded here before being passed to the workflow
    expanded_goal = expand_simple_task(raw_goal_text)

    def cli_output(message):
        print(message, end='')

    run_automation_workflow(expanded_goal, args.keep_open, is_interactive, cli_output)

if __name__ == "__main__":
    main()
# src/interfaces/cli.py
import argparse
import sys, logger
from pathlib import Path

from rich.console import Console

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.workflow import run_automation_workflow
from src.core.utils import expand_simple_task
from src.core.executor import TaskExecutor # Import Executor here

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="OpenAgent-Lite CLI")
    parser.add_argument('--goal', help='The natural language goal for the agent.')
    parser.add_argument('--keep-open', action='store_true', help='Keep the browser open after finishing.')
    args = parser.parse_args()

    # The CLI will manage its own executor lifecycle
    executor = TaskExecutor()
    
    try:
        raw_goal_text = ""
        if not args.goal: # Interactive mode
            console.print("\n💬 [bold cyan]Enter your goal for the agent:[/bold cyan]")
            raw_goal_text = input("   > ").strip()
        else: # Direct mode
            raw_goal_text = args.goal.strip()

        if not raw_goal_text:
            console.print("[bold red]No goal provided. Exiting.[/bold red]"); return

        def cli_output(message):
            print(message, end='')

        # Run the workflow, passing the executor instance
        run_automation_workflow(raw_goal_text, executor, cli_output)

    finally:
        # The CLI's cleanup logic is now handled here, outside the workflow
        if args.keep_open:
            input("--> Press Enter in this terminal to close the browser and exit. <--")
        
        console.print("\n🧹 [bold blue]Cleaning up resources...[/bold blue]")
        executor.cleanup()
        logger.info("--- OpenAgent-Lite CLI session finished ---")
        console.print("👋 [bold]Goodbye![/bold]")

if __name__ == "__main__":
    main()
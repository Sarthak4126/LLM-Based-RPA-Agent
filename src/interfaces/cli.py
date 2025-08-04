# src/interfaces/cli.py
import argparse
import sys
from pathlib import Path

# --- NEW IMPORTS ---
from rich.console import Console
from rich.panel import Panel

# Ensure the project root is in the Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.planner import GoalPlanner
from src.core.executor import TaskExecutor
from src.core.logger import logger

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
    logger.info("--- OpenAgent-Lite session started ---")
    # --- NEW: Initialize Rich Console ---
    console = Console()

    parser = argparse.ArgumentParser(description="OpenAgent-Lite")
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
    
    expanded_goal = expand_simple_task(raw_goal_text)
    run_automation(expanded_goal, args, is_interactive)

def run_automation(goal_text, args, is_interactive: bool):
    # --- NEW: Initialize Rich Console ---
    console = Console()
    planner = GoalPlanner()
    executor = TaskExecutor()
    plan = None
    try:
        # --- MODIFIED: Display goal in a Panel ---
        console.print(Panel(
            f"[bold cyan]{goal_text}[/bold cyan]",
            title="🎯 Your Goal",
            border_style="green"
        ))

        plan = planner.plan_goal(goal_text)
        if not plan:
            console.print("[bold red]❌ I couldn't create a valid plan. Please check logs.[/bold red]"); return

        console.print(f"\n📋 [bold]Plan Generated:[/bold] {plan.get('goal', 'N/A')}")
        for i, task in enumerate(plan.get('subtasks', [])):
            console.print(f"  [yellow]Step {i+1}:[/yellow] {task['module']}.{task['action']} [dim]params: {task.get('parameters', {})}[/dim]")

        console.print("\n🚀 [bold magenta]Executing Plan...[/bold magenta]")
        results = executor.execute_plan(plan)
        
        console.print("\n✨ [bold]Results:[/bold]")
        for res in results:
            if res['status'] == 'success':
                console.print(f"  [green]✅ SUCCESS:[/green] {res['task']}")
            else:
                console.print(f"  [bold red]❌ FAILED:[/bold red] {res['task']} [dim](Error: {res['error']})[/dim]")
    
    except Exception as e:
        logger.error("A critical error occurred in run_automation.", exc_info=True)
        console.print(f"\n🚨 [bold red]A critical error occurred: {e}[/bold red]")
    finally:
        should_wait = False
        if args.keep_open:
            should_wait = True
        elif is_interactive and plan:
            is_web_task = any(task.get("module") == "web" for task in plan.get("subtasks", []))
            if is_web_task:
                should_wait = True

        if should_wait:
            console.print("\n[green]✅ Task finished. Browser remains open.[/green]")
            input("--> Press Enter in this terminal to close the browser and exit. <--")
        
        console.print("\n🧹 [bold blue]Cleaning up resources...[/bold blue]")
        executor.cleanup()
        logger.info("--- OpenAgent-Lite session finished ---")
        console.print("👋 [bold]Goodbye![/bold]")

if __name__ == "__main__":
    main()
# src/interfaces/cli.py
import argparse
import sys
from pathlib import Path

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
    parser = argparse.ArgumentParser(description="OpenAgent-Lite")
    parser.add_argument('--goal', help='The natural language goal for the agent.')
    parser.add_argument('--keep-open', action='store_true', help='Keep the browser open after finishing.')
    args = parser.parse_args()

    # Determine if we are in interactive mode before getting input
    is_interactive = not args.goal 
    
    raw_goal_text = args.goal or input("💬 Enter your goal: ").strip()
    if not raw_goal_text:
        print("No goal provided. Exiting."); return
    
    expanded_goal = expand_simple_task(raw_goal_text)
    # Pass the interactive flag to the run function
    run_automation(expanded_goal, args, is_interactive)

def run_automation(goal_text, args, is_interactive: bool):
    planner = GoalPlanner()
    executor = TaskExecutor()
    plan = None  # Initialize plan to None
    try:
        print(f"\n🎯 Your Goal: {goal_text}")
        plan = planner.plan_goal(goal_text)
        if not plan:
            print("❌ I couldn't create a valid plan. Please check logs."); return

        print(f"\n📋 Plan Generated: {plan.get('goal', 'N/A')}")
        for i, task in enumerate(plan.get('subtasks', [])):
            print(f"  Step {i+1}: {task['module']}.{task['action']} params: {task.get('parameters', {})}")

        print("\n🚀 Executing Plan...")
        results = executor.execute_plan(plan)
        
        print("\n✨ Results:")
        for res in results:
            status = "✅ SUCCESS" if res['status'] == 'success' else "❌ FAILED"
            print(f"  {status}: {res['task']}" + (f" (Error: {res['error']})" if res['status'] == 'failed' else ""))
    
    except Exception as e:
        logger.error("A critical error occurred in run_automation.", exc_info=True)
        print(f"\n🚨 A critical error occurred: {e}")
    finally:
        # NEW LOGIC: Determine if we should wait before closing
        should_wait = False
        if args.keep_open:
            should_wait = True
        elif is_interactive and plan:
            # Check if any task in the plan used the 'web' module
            is_web_task = any(task.get("module") == "web" for task in plan.get("subtasks", []))
            if is_web_task:
                should_wait = True

        if should_wait:
            print("\n✅ Task finished. Browser remains open.")
            input("--> Press Enter in this terminal to close the browser and exit. <--")
        
        print("\n🧹 Cleaning up resources...")
        executor.cleanup()
        logger.info("--- OpenAgent-Lite session finished ---")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
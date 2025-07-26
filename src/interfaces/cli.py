# src/interfaces/cli.py
import argparse
import sys
from pathlib import Path
from typing import Optional

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.planner import GoalPlanner
from src.core.executor import TaskExecutor
from src.core.logger import logger

def expand_simple_task(goal: str) -> str:
    """
    (NEW) Expands shorthand commands into full, natural language goals.
    """
    if not goal:
        return ""
    
    parts = goal.lower().split()
    command = parts[0]
    args = " ".join(parts[1:])

    # Dictionary of known shorthand commands
    app_aliases = {
        "notepad": f"Open notepad and type '{args}'",
        "calc": "Open the calculator app",
        "calculator": "Open the calculator app",
    }

    web_aliases = {
        "google": f"On google, search for '{args}'",
        "youtube": f"On youtube, search for and play '{args}'",
    }

    if command in app_aliases and args:
        logger.info(f"Expanding shorthand '{goal}' to '{app_aliases[command]}'")
        return app_aliases[command]
    elif command in app_aliases: # For commands with no arguments
         logger.info(f"Expanding shorthand '{goal}' to '{app_aliases[command]}'")
         return app_aliases[command]
    elif command in web_aliases and args:
        logger.info(f"Expanding shorthand '{goal}' to '{web_aliases[command]}'")
        return web_aliases[command]

    # If no shorthand is matched, return the original goal for the LLM to process
    return goal


def main():
    logger.info("--- OpenAgent-Lite session started ---")
    parser = argparse.ArgumentParser(description="OpenAgent-Lite: Your personal RPA agent.")
    parser.add_argument('--goal', help='The natural language goal for the agent to achieve.')
    parser.add_argument('--keep-open', action='store_true', help='Keep the browser open after the task is finished.')
    args = parser.parse_args()

    raw_goal_text = args.goal or input("💬 Enter your goal: ").strip()
    if not raw_goal_text:
        print("No goal provided. Exiting.")
        return
    
    # Expand the goal before sending it to the automation engine
    expanded_goal = expand_simple_task(raw_goal_text)

    run_automation(expanded_goal, args)

def run_automation(goal_text, args):
    planner = GoalPlanner()
    executor = TaskExecutor()
    try:
        print(f"\n🎯 Your Goal: {goal_text}")
        plan = planner.plan_goal(goal_text)
        if not plan:
            print("❌ I couldn't create a valid plan for that request. Please check the logs.")
            return

        print(f"\n📋 Plan Generated: {plan.get('goal', 'No description')}")
        for i, task in enumerate(plan.get('subtasks', [])):
            print(f"  Step {i+1}: {task['module']}.{task['action']} with params {task.get('parameters', {})}")

        print("\n🚀 Executing Plan...")
        results = executor.execute_plan(plan)
        
        print("\n✨ Results:")
        for result in results:
            if result['status'] == 'success':
                print(f"  ✅ SUCCESS: {result['task']}")
            else:
                print(f"  ❌ FAILED: {result['task']} (Error: {result['error']})")
    
    except Exception as e:
        logger.error("A critical error occurred in run_automation.", exc_info=True)
        print(f"\n🚨 A critical error occurred: {e}")
    finally:
        if args.keep_open:
            print("\n✅ Task finished. The browser will remain open.")
            input("--> Press Enter in this terminal to close the browser and exit. <--")
        
        print("\n🧹 Cleaning up resources...")
        executor.cleanup()
        logger.info("--- OpenAgent-Lite session finished ---")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
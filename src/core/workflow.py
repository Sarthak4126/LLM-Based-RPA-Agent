# src/core/workflow.py
import sys
from typing import Callable
from pathlib import Path

# Adjust path to import from other src directories
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.planner import GoalPlanner
from src.core.executor import TaskExecutor # Keep this import
from src.core.logger import logger
from src.core.utils import expand_simple_task

# MODIFIED: The function now accepts an executor instance and no longer handles cleanup.
def run_automation_workflow(goal_text: str, executor: TaskExecutor, output_callback: Callable[[str], None]):
    planner = GoalPlanner()
    try:
        expanded_goal = expand_simple_task(goal_text)
        output_callback(f"🎯 Your Goal: {expanded_goal}\n")

        plan = planner.plan_goal(expanded_goal)
        if not plan:
            output_callback("❌ I couldn't create a valid plan. Please check logs.\n")
            return

        plan_details = f"📋 Plan Generated: {plan.get('goal', 'N/A')}\n"
        for i, task in enumerate(plan.get('subtasks', [])):
            plan_details += f"  Step {i+1}: {task['module']}.{task['action']} params: {task.get('parameters', {})}\n"
        output_callback(plan_details)

        output_callback("🚀 Executing Plan...\n")
        results = executor.execute_plan(plan)
        
        output_callback("✨ Results:\n")
        for res in results:
            if res['status'] == 'success':
                output_callback(f"  ✅ SUCCESS: {res['task']}\n")
            else:
                output_callback(f"  ❌ FAILED: {res['task']} (Error: {res['error']})\n")
        
        output_callback("✅ Task complete. Browser remains open by default.\n")

    except Exception as e:
        logger.error("A critical error occurred in the workflow.", exc_info=True)
        output_callback(f"🚨 A critical error occurred: {e}\n")
    finally:
        logger.info("--- Workflow for one goal finished ---\n")
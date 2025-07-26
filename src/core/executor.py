# src/core/executor.py
import importlib
import time
from typing import Dict, List, Any
from .logger import logger

class TaskExecutor:
    def __init__(self):
        self.modules = {
            "desktop": "src.automation.desktop.DesktopAutomator",
            "web": "src.automation.web.WebAutomator",
            "files": "src.automation.files.FileManager",
            "office": "src.automation.office.OfficeAutomator"
        }
        self.active_sessions = {}

    def execute_plan(self, action_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        logger.info(f"--- Starting Execution for Goal: {action_plan.get('goal', 'N/A')} ---")
        for task in action_plan.get("subtasks", []):
            task_description = f"{task['module']}.{task['action']}"
            logger.info(f"Executing task: {task_description} with params: {task.get('parameters', {})}")
            try:
                if task["module"] not in self.active_sessions:
                    module_path = self.modules[task["module"]]
                    module_name, class_name = module_path.rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    self.active_sessions[task["module"]] = getattr(module, class_name)()
                instance = self.active_sessions[task["module"]]
                method = getattr(instance, task["action"])
                result = method(**task.get("parameters", {}))
                logger.info(f"Task '{task_description}' completed successfully.")
                results.append({"task": task_description, "status": "success", "result": result})
                time.sleep(task.get("wait_after", 1.0))
            except Exception as e:
                logger.error(f"Task '{task_description}' failed. Error: {e}", exc_info=True)
                results.append({"task": task_description, "status": "failed", "error": str(e)})
        logger.info("--- Plan Execution Finished ---")
        return results

    def cleanup(self):
        logger.info("Cleaning up active sessions...")
        for instance in self.active_sessions.values():
            if hasattr(instance, 'close'):
                instance.close()
        self.active_sessions.clear()
        logger.info("Cleanup complete.")
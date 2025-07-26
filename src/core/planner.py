#### **`src/core/planner.py`**

# src/core/planner.py
from typing import Dict, Any
from .llm_provider import LLMProvider
from .logger import logger

class GoalPlanner:
    def __init__(self):
        self.llm_provider = LLMProvider()
        self.available_actions = self._get_available_actions()

    def _get_available_actions(self) -> Dict[str, Any]:
        return {
            "desktop": {
                "open_app": "Opens a desktop application. Parameter: 'app_name'.",
                "keyboard_input": "Types text using the keyboard. Parameter: 'text'.",
                "mouse_click": "Performs a click at specific (x,y) coordinates."
            },
            "web": {
                "search": "Searches 'google' or 'youtube'. Opens browser automatically. Parameters: 'site', 'query'.",
                "click_element": "Clicks a web element using a CSS selector. Parameter: 'selector'."
            }
        }

    def _validate_and_clean_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        if not plan or not plan.get("subtasks"): return None
        
        valid_tasks = []
        for task in plan["subtasks"]:
            module_name = task.get("module")
            action_name = task.get("action")
            
            # Universal Schema Check: Does the module and action exist?
            if module_name in self.available_actions and action_name in self.available_actions[module_name]:
                valid_tasks.append(task)
            else:
                logger.warning(f"Validator: Discarding hallucinated action: {module_name}.{action_name}")

        plan["subtasks"] = valid_tasks
        return plan if valid_tasks else None

    def plan_goal(self, goal_text: str) -> Dict[str, Any]:
        logger.info(f"Received goal: '{goal_text}'")
        raw_plan = self.llm_provider.generate_plan(goal_text, self.available_actions)
        if not raw_plan: return None
        logger.info("Validating plan...")
        clean_plan = self._validate_and_clean_plan(raw_plan)
        if not clean_plan:
            logger.error("Plan is invalid after validation.")
            return None
        logger.info("Plan validation complete.")
        return clean_plan
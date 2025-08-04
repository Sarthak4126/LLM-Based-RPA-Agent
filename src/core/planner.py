# src/core/planner.py
from typing import Dict, Any
from .llm_provider import LLMProvider
from .logger import logger
import re

class GoalPlanner:
    def __init__(self):
        self.llm_provider = LLMProvider()
        self.available_actions = self._get_available_actions()

    def _get_available_actions(self) -> Dict[str, Any]:
        return {
            "desktop": {
                "open_app": "Opens a NON-BROWSER application (e.g., 'notepad'). Parameter: 'app_name'.",
                "keyboard_input": "Types text using the keyboard. Parameter: 'text'.",
                "mouse_click": "Performs a click at specific (x,y) coordinates."
            },
            "web": {
                "search": "Use to search 'google' or 'youtube'. Opens the browser automatically. Parameters: 'site', 'query'.",
                "click_element": "Clicks a web element using a CSS selector. Parameter: 'selector'."
            }
        }

    def _validate_and_clean_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        if not plan or not plan.get("subtasks"): return None
        
        tasks = plan["subtasks"]
        
        first_web_action_index = -1
        for i, task in enumerate(tasks):
            if task.get("module") == "web":
                first_web_action_index = i
                break
        
        if first_web_action_index > 0:
            logger.warning(f"Validator: Discarding {first_web_action_index} invalid preliminary steps.")
            tasks = tasks[first_web_action_index:]
        
        plan["subtasks"] = tasks
        return plan

    def plan_goal(self, goal_text: str) -> Dict[str, Any]:
        logger.info(f"Received goal: '{goal_text}'")

        match = re.search(r"write an? (article|paragraph) about (.*)", goal_text, re.IGNORECASE)
        if match:
            topic = match.group(2).strip()
            logger.info(f"Article generation goal detected. Topic: '{topic}'")
            print(f"✍️ Understood. I will now write about '{topic}'. This may take a moment...")
            
            article_content = self.llm_provider.generate_content(topic)
            if not article_content or "Error:" in article_content:
                logger.error(f"Failed to generate content for topic: {topic}")
                return None

            # --- NEW: FORMATTING LOGIC ---
            # Capitalize the topic to make it look like a title
            title = topic.title()
            # Combine the title, two new lines, and the content into a single string
            full_text_to_write = f"{title}\n\n{article_content}"
            # --- END OF NEW LOGIC ---

            logger.info("Content generated, now building a manual plan.")
            manual_plan = {
                "goal": f"Write an article about {topic}",
                "subtasks": [
                    {
                        "module": "desktop",
                        "action": "open_app",
                        "parameters": {"app_name": "notepad"}
                    },
                    {
                        "module": "desktop",
                        "action": "keyboard_input",
                        # MODIFIED: Use the new formatted string here
                        "parameters": {"text": full_text_to_write}
                    }
                ]
            }
            return manual_plan

        logger.info("Standard goal detected. Generating a JSON plan...")
        raw_plan = self.llm_provider.generate_plan(goal_text, self.available_actions)
        if not raw_plan: return None

        logger.info("Validating and cleaning generated plan...")
        clean_plan = self._validate_and_clean_plan(raw_plan)
        if not clean_plan or not clean_plan.get("subtasks"):
            logger.error("Plan is invalid or empty after validation.")
            return None
            
        logger.info("Plan validation complete.")
        return clean_plan
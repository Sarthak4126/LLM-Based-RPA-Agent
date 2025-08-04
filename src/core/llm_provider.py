# src/core/llm_provider.py
import json
import requests
from typing import Dict, Any
from .logger import logger

class LLMProvider:
    def __init__(self, model_name: str = "mistral", ollama_host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_url = f"{ollama_host}/api/generate"
        logger.info(f"LLMProvider configured for Ollama model '{self.model_name}' at {ollama_host}")

    def generate_plan(self, goal: str, available_actions: Dict) -> Dict[str, Any]:
        logger.info(f"Generating plan for goal: '{goal}'")
        prompt = self._create_plan_prompt(goal, available_actions)
        payload = {"model": self.model_name, "prompt": prompt, "format": "json", "stream": False}
        try:
            response = requests.post(self.api_url, json=payload, timeout=180) # Increased timeout
            response.raise_for_status()
            response_text = response.json().get('response', '')
            logger.info("Received plan response from Ollama.")
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"LLM plan generation failed: {e}", exc_info=True)
            return None

    # --- NEW FUNCTION FOR CONTENT GENERATION ---
    def generate_content(self, topic: str) -> str:
        logger.info(f"Generating content for topic: '{topic}'")
        prompt = self._create_content_prompt(topic)
        # Note: No "format: json" here, we want raw text
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.api_url, json=payload, timeout=180) # Increased timeout
            response.raise_for_status()
            response_text = response.json().get('response', '')
            logger.info("Received content response from Ollama.")
            return response_text.strip()
        except Exception as e:
            logger.error(f"LLM content generation failed: {e}", exc_info=True)
            return f"Error: Could not generate content for the topic '{topic}'."

    def _create_content_prompt(self, topic: str) -> str:
        return f"""You are a helpful assistant. Write a concise, well-structured paragraph about the following topic. Do not include a title or any introductory phrases like "Here is a paragraph about...". Just provide the text of the paragraph itself.

Topic: "{topic}"
"""

    def _create_plan_prompt(self, goal: str, actions: Dict) -> str:
        actions_formatted = json.dumps(actions, indent=2)
        return f"""You are a robot that creates a JSON plan from a user's goal.

### CRITICAL RULES
1. You MUST ONLY use the exact module and action names from the "Tools Available" list.
2. To 'play' a video, the plan MUST be a `web.search` step followed by a `web.click_element` step.
3. To 'type' text, the action is `keyboard_input`.

### Tools Available
```json
{actions_formatted}
Example 1 (Desktop Task)
User Goal: "Open notepad and write 'hello there'"
Correct JSON Plan:

JSON

{{
  "goal": "Open notepad and write 'hello there'",
  "subtasks": [
    {{
      "module": "desktop",
      "action": "open_app",
      "parameters": {{
        "app_name": "notepad"
      }}
    }},
    {{
      "module": "desktop",
      "action": "keyboard_input",
      "parameters": {{
        "text": "hello there"
      }}
    }}
  ]
}}
Example 2 (Web Task)
User Goal: "Play 'Do I Wanna Know' on YouTube."
Correct JSON Plan:

JSON

{{
  "goal": "Play the song 'Do I Wanna Know' on YouTube",
  "subtasks": [
    {{
      "module": "web",
      "action": "search",
      "parameters": {{
        "site": "youtube",
        "query": "Do I Wanna Know"
      }}
    }},
    {{
      "module": "web",
      "action": "click_element",
      "parameters": {{
        "selector": "ytd-video-renderer a#video-title"
      }}
    }}
  ]
}}
Your Task
User Goal: "{goal}"
Correct JSON Plan:
"""
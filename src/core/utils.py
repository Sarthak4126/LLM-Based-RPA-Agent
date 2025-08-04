# src/core/utils.py

# This function expands simple shorthand commands into full natural language goals.
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
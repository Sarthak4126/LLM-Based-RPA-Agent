# src/utils/helpers.py

# This file is reserved for utility functions that can be used across the project.
# For example, functions for data parsing, validation, or formatting.

def format_results(results: list) -> str:
    """
    Formats a list of execution results into a readable string.
    """
    formatted_string = "Execution Results:\n"
    for res in results:
        status = "✅" if res['status'] == 'success' else "❌"
        formatted_string += f"{status} Task: {res['task']}\n"
        if res['status'] == 'failed':
            formatted_string += f"   - Error: {res['error']}\n"
    return formatted_string
# src/interfaces/simple_cli.py
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.planner import GoalPlanner
from src.core.executor import TaskExecutor

def main():
    print("🤖 OpenAgent-Lite: Just tell me what to do")
    print("Type 'exit' to quit\n")
    
    planner = GoalPlanner()
    executor = TaskExecutor()
    
    while True:
        try:
            goal = input("> ").strip()
            if goal.lower() in ('exit', 'quit'):
                break
            if not goal:
                continue
            
            run_automation(goal, planner, executor)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️  Error: {str(e)}")
            
    print("\nGoodbye!")
    executor.cleanup()


def run_automation(goal_text, planner, executor):
    try:
        plan = planner.plan_goal(goal_text)
        if not plan or not plan.get("subtasks"):
            print("❌ I couldn't understand that request")
            return
            
        print(f"\n🔧 Executing: {plan.get('goal', goal_text)}")
        results = executor.execute_plan(plan)
        
        for result in results:
            if result['status'] == 'success':
                print(f"  ✅ {result['task']}")
            else:
                print(f"  ❌ {result['task']} (Error: {result['error']})")
        print("-" * 20)
    except Exception as e:
        print(f"\n🚨 A critical error occurred during automation: {e}")

if __name__ == "__main__":
    main()
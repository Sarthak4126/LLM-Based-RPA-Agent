import speech_recognition as sr
from src.core.planner import GoalPlanner
from src.core.executor import TaskExecutor

def main():
    recognizer = sr.Recognizer()
    planner = GoalPlanner()
    executor = TaskExecutor()
    
    print("🤖 OpenAgent-Lite: Say your command (or 'exit' to quit)")
    
    while True:
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                print(f"\n👂 Heard: {command}")
                
                if command.lower() == 'exit':
                    executor.full_cleanup()
                    break
                
                plan = planner.plan_goal(command)
                print(f"\n🔧 Executing: {plan['goal']}")
                
                results = executor.execute_plan(plan)
                for result in results:
                    if result['status'] == 'success':
                        print(f"✅ {result['task']}")
                    else:
                        print(f"❌ {result['task']} (Error: {result['error']})")
                
            except sr.WaitTimeoutError:
                print("⏳ No speech detected, listening again...")
            except sr.UnknownValueError:
                print("❓ Could not understand audio, please try again")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
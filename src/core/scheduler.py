# src/core/scheduler.py
import schedule
import time
from threading import Thread
from src.core.executor import TaskExecutor

class TaskScheduler:
    def __init__(self):
        self.executor = TaskExecutor()
        self.scheduled_jobs = {}

    def add_scheduled_task(self, task_id, action_plan, schedule_time):
        job = schedule.every().day.at(schedule_time).do(
            self.executor.execute_plan, action_plan
        )
        self.scheduled_jobs[task_id] = job

    def run_pending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_scheduler(self):
        scheduler_thread = Thread(target=self.run_pending)
        scheduler_thread.daemon = True
        scheduler_thread.start()
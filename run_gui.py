# run_gui.py
import customtkinter as ctk
import threading
import queue

from src.core.workflow import run_automation_workflow
from src.core.executor import TaskExecutor

class OpenAgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OpenAgent-Lite")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- NEW: The GUI now owns the executor ---
        self.executor = TaskExecutor()

        # --- NEW: Bind the window closing event to our cleanup function ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- CONFIGURE GRID ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- WIDGETS ---
        self.top_frame = ctk.CTkFrame(self, corner_radius=10)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.goal_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Enter your goal here...", height=40, font=("Arial", 14))
        self.goal_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.run_button = ctk.CTkButton(self.top_frame, text="Run Goal", command=self.start_automation_thread, height=40)
        self.run_button.grid(row=0, column=1, padx=10, pady=10)
        
        # --- REMOVED: The "Keep Browser Open" checkbox is no longer needed ---

        self.output_textbox = ctk.CTkTextbox(self, corner_radius=10, font=("Courier New", 12), state="disabled")
        self.output_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.output_queue = queue.Queue()
        self.after(100, self.process_queue)

    def update_output(self, message):
        self.output_textbox.configure(state="normal")
        self.output_textbox.insert("end", message)
        self.output_textbox.see("end")
        self.output_textbox.configure(state="disabled")

    def start_automation_thread(self):
        goal = self.goal_entry.get()
        if not goal:
            self.update_output("Please enter a goal first.\n")
            return
        
        self.run_button.configure(state="disabled", text="Running...")
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.configure(state="disabled")

        # Run the workflow, passing the GUI's executor instance
        thread = threading.Thread(
            target=run_automation_workflow,
            args=(goal, self.executor, self.queue_output)
        )
        thread.daemon = True
        thread.start()

    def queue_output(self, message):
        self.output_queue.put(message)

    def process_queue(self):
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.update_output(message)
                # Re-enable the button after the task is done
                if "Task complete" in message or "A critical error occurred" in message:
                    self.run_button.configure(state="normal", text="Run Goal")
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    # --- NEW: This function is called when you click the 'X' on the window ---
    def on_closing(self):
        print("GUI is closing, cleaning up browser session...")
        self.executor.cleanup()
        self.destroy()

if __name__ == "__main__":
    app = OpenAgentGUI()
    app.mainloop()
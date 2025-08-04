# run_gui.py
import customtkinter as ctk
import threading
import queue

from src.core.workflow import run_automation_workflow

class OpenAgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OpenAgent-Lite")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- CONFIGURE GRID ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- WIDGETS ---
        # Top Frame for Input
        self.top_frame = ctk.CTkFrame(self, corner_radius=10)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.goal_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Enter your goal here...", height=40, font=("Arial", 14))
        self.goal_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.run_button = ctk.CTkButton(self.top_frame, text="Run Goal", command=self.start_automation_thread, height=40)
        self.run_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.keep_open_var = ctk.StringVar(value="off")
        self.keep_open_checkbox = ctk.CTkCheckBox(self.top_frame, text="Keep Browser Open", variable=self.keep_open_var, onvalue="on", offvalue="off")
        self.keep_open_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Output Textbox
        self.output_textbox = ctk.CTkTextbox(self, corner_radius=10, font=("Courier New", 12), state="disabled")
        self.output_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Queue for thread communication
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

        keep_open = self.keep_open_var.get() == "on"

        # Run the workflow in a separate thread to keep the GUI responsive
        thread = threading.Thread(
            target=run_automation_workflow,
            args=(goal, keep_open, False, self.queue_output) # is_interactive is False for GUI
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
                # Check if the process is finished to re-enable the button
                if "Goodbye!" in message or "A critical error occurred" in message:
                    self.run_button.configure(state="normal", text="Run Goal")
        except queue.Empty:
            pass
        self.after(100, self.process_queue)


if __name__ == "__main__":
    app = OpenAgentGUI()
    app.mainloop()
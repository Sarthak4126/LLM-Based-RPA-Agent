# OpenAgent-Lite 🤖

A powerful, multitasking desktop assistant built in Python. It uses a local LLM (via Ollama) to understand natural language goals, create plans, and autonomously execute them using web and desktop automation tools.

### 🎥 Demo

[Check out the video demo on my LinkedIn!](https://www.linkedin.com/posts/sarthak-singh-manhas-2223b71b7_python-ai-multitasking-activity-7358188975397720064-IDiV?utm_source=share&utm_medium=member_desktop)

---

### ✨ Key Features

* **🧠 Intelligent Planning:** Translates high-level goals into concrete, multi-step execution plans.
* **✍️ AI Content Generation:** Can write and save complete articles on any given topic.
* **🌐 Robust Web Automation:** Uses Selenium to control web browsers for tasks like searching and media playback.
* **🖥️ Desktop Control:** Uses PyAutoGUI to open and interact with local desktop applications.
* **⚡ True Multitasking:** Capable of managing background tasks (like playing music) while executing new foreground tasks.
* **✨ Custom GUI:** A clean and user-friendly interface built with CustomTkinter.

---

### 🏛️ Architecture

The project is designed with a clean, modular architecture to separate concerns and allow for future scalability.

LLM-Based-RPA-Agent/
│
├── run_gui.py          # Main entry point for the GUI application
├── requirements.txt    # Project dependencies
│
└── src/
├── core/           # The "brain" of the agent
│   ├── workflow.py   # Main logic for running a goal
│   ├── planner.py    # Interfaces with the LLM to create plans
│   ├── executor.py   # Executes the steps in the plan
│   ├── llm_provider.py
│   ├── utils.py
│   └── logger.py
│
├── automation/     # The "hands" of the agent
│   ├── desktop.py    # Controls keyboard and mouse (PyAutoGUI)
│   └── web.py        # Controls the web browser (Selenium)
│
└── interfaces/
└── cli.py        # The legacy command-line interface


---

### 🛠️ Tech Stack

* **Core:** Python
* **AI:** Ollama (with Mistral model)
* **GUI:** CustomTkinter
* **Web Automation:** Selenium
* **Desktop Automation:** PyAutoGUI
* **CLI Formatting:** Rich

---

### 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Sarthak4126/LLM-Based-RPA-Agent.git](https://github.com/Sarthak4126/LLM-Based-RPA-Agent.git)
    cd LLM-Based-RPA-Agent
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ensure Ollama is running** with the `mistral` model pulled.
4.  **Run the application:**
    ```bash
    python run_gui.py
    ```

---

### 📄 License

Licensed under the MIT License.

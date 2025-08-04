# 🤖 LLM-Based RPA Agent

A lightweight, goal-driven desktop automation assistant powered by small Language Models (LLMs). It interprets natural language instructions, creates action plans, and performs tasks autonomously across desktop and web.

---

## 🎯 Objective

To create an open-source RPA tool that:
- Understands plain English goals
- Uses an LLM to plan the steps
- Executes them via desktop/web automation

---

## 🧠 Architecture

LLM-Based-RPA-Agent/
├── src/
│ ├── agent/
│ │ ├── llm_planner.py # Goal parsing
│ │ └── plan_executor.py # Action executor
│ ├── automation/
│ │ ├── desktop.py # Mouse, keyboard
│ │ ├── file_system.py # File ops
│ │ └── web.py # Web (Selenium)
│ ├── utils/
│ │ └── logger.py
│ └── main.py # Entry point
├── app.py # App-level logic
├── requirements.txt # Dependencies

yaml
Copy
Edit

---

## 💻 Technologies

| Component    | Tool/Library              |
|--------------|---------------------------|
| LLM          | TinyLLaMA / Mistral / Phi-2 |
| Automation   | PyAutoGUI, Selenium       |
| CLI/App      | Python, Gradio (optional) |
| Logging      | Python logging module     |

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/LLM-Based-RPA-Agent.git
cd LLM-Based-RPA-Agent
pip install -r requirements.txt
python src/main.py
✅ Sample Goals
Input Goal	Action Type
Open Notepad and type "Hello"	Desktop Automation
Search GitHub on Chrome	Web Automation
Create folder named "Reports"	File System

🚧 Future Features
GUI using Gradio/Streamlit

Voice command integration

Advanced planning with finetuned LLMs

Secure command execution sandbox

📄 License
Licensed under the MIT License.

yaml
Copy
Edit

---

## ✅ `.gitignore` (Final)

Here’s the `.gitignore` again — no need to change it:

```gitignore
__pycache__/
*.pyc
*.log
.env
.DS_Store
.idea/
.vscode/
logs/

----------------------------------------------------
# OpenAgent-Lite 🤖

OpenAgent-Lite is a powerful, multitasking desktop assistant built in Python. It uses a local LLM (via Ollama) to understand natural language goals, create plans, and autonomously execute them using web and desktop automation tools.

### 🎥 Demo
*I will be adding a link to the LinkedIn post with the video here soon!*
[Check out the video demo on my LinkedIn!](https://www.linkedin.com/posts/sarthak-singh-manhas-2223b71b7_python-ai-multitasking-activity-7358188975397720064-IDiV?utm_source=share&utm_medium=member_desktop&rcm=ACoAADJtP3oBOBpy--GlnxUK7jFuPxUvepeINl8)
---

### ✨ Key Features

* **🧠 Intelligent Planning:** Translates high-level goals into concrete, multi-step execution plans.
* **✍️ AI Content Generation:** Can write and save complete articles on any given topic.
* **🌐 Robust Web Automation:** Uses Selenium to control web browsers for tasks like searching and media playback.
* **🖥️ Desktop Control:** Uses PyAutoGUI to open and interact with local desktop applications.
* **⚡ True Multitasking:** Capable of managing background tasks (like playing music) while executing new foreground tasks.
* **✨ Custom GUI:** A clean and user-friendly interface built with CustomTkinter.

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

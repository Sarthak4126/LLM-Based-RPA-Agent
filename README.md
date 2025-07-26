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

🤖 Local AI Terminal Assistant(V1 + V2)

A lightweight, fully local AI-powered terminal assistant that automatically
detects command errors and explains them in plain English.

No internet required. No paid APIs. Everything runs on your own machine.

---

📋 Table of Contents

- [What This Does](#what-this-does)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Limitations](#limitations)
- [Future Plans](#future-plans)

---

🎯 What This Does

When you run a terminal command that fails, this assistant:

1. Automatically detects the error
2. Sends it to a local AI model
3. Explains what went wrong
4. Tells you exactly how to fix it

Supported Error Types
- Python errors (ModuleNotFoundError, SyntaxError, etc.)
- Linux command errors (Permission denied, File not found, etc.)
- Git errors (not a repo, merge conflicts, etc.)
- Any other terminal command failure

---
 ⚙️ How It Works

You type a command
│
▼
Assistant runs it using Python subprocess
│
▼
Captures stdout and stderr separately
│
▼
Checks exit code (0 = success, non-zero = error)
│
▼
If error detected → sends to Ollama API
│
▼
gemma:2b model analyzes the error locally
│
▼
Explanation printed in your terminal

Everything happens on your machine. Your data never leaves your computer.

---

 💻 Requirements

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Ubuntu Linux | 22.04+ | Operating system |
| Python | 3.10+ | Running the assistant |
| Ollama | 0.24+ | Local AI engine |
| gemma:2b | latest | AI model for explanations |
| RAM | 4GB minimum | Running the AI model |
| Disk Space | 5GB free | Storing the AI model |

---

🚀 Installation

 Step 1 — Clone This Repository

```bash
git clone https://github.com/YOURUSERNAME/terminal-assistant.git
cd terminal-assistant

 Step 2 - Install Pythonn Dependencies 

pip3 install requests

 Step 3 - Install Ollama 

curl -fsSL https://ollama.com/install.sh | sh

 Step 4 - Dowmload The AI Model

ollama pull gemma:2b

 Step 5 - Verify Ollama Is Running

systemctl status ollama

📖 Usage
Start the Assistant

python3 assistant.py

You Will See:

==================================================
   LOCAL AI TERMINAL ASSISTANT
   Powered by gemma:2b + Ollama
   Type 'exit' to quit
==================================================

⚡ Enter command:

Type Any Terminal Command 

⚡ Enter command: python3 -c 'import flask'

Exit The Assistant

⚡ Enter command: exit

📺 Example Output
Example 1 — Python Module Error

⚡ Enter command: python3 -c 'import flask'

>>> Running: python3 -c 'import flask'

❌ Error detected!
ModuleNotFoundError: No module named 'flask'

🤔 Analyzing error with AI...

==================================================
💡 AI EXPLANATION:
==================================================
What went wrong:
Python cannot find the Flask library on your system.

Why it happened:
Flask is not a built-in Python library. It needs
to be installed separately before you can use it.

How to fix it:
Run this command:
    pip install flask

Then try your original command again.
==================================================

Example 2 — Permission Error

⚡ Enter command: cat /etc/shadow

>>> Running: cat /etc/shadow

❌ Error detected!
cat: /etc/shadow: Permission denied

🤔 Analyzing error with AI...

==================================================
💡 AI EXPLANATION:
==================================================
What went wrong:
You don't have permission to read this file.

Why it happened:
/etc/shadow contains password hashes and is
protected. Only the root user can read it.

How to fix it:
If you genuinely need to read it:
    sudo cat /etc/shadow

But be careful with sudo — it gives full system access.

## 🧠 Version 2 — Memory Features

Run Version 2 for context-aware assistance:

```bash
python3 assistant_v2.py

Special Commands in V2

Command               What It Does

memory                Shows last 5 commands with status
exit                  Saves session and exits
any command           Runs it with memory-aware AI


## How Memory WorksFirst time error → AI explains → saved to memory
Second time     → "Seen 1 time before!" → smarter explanation
Third time      → "Seen 2 times before!" → even more context

## Memory Database
All history stored locally in terminal_memory.db
•Never sent to internet
•Grows smarter over time
•Persists between sessions

==================================================

📁 Project Structure

terminal-assistant/
│
├── assistant.py      # Main assistant script
└── README.md         # This file

🛠️ Tech Stack

TOOL            ROLE

Python 3        Core programming language
Subprocess      Running terminal commands
requests        Communicating with Ollama API
Ollama          Local AI model server
gemma:2b        AI model (by Google DeepMind)
Ubuntu Linux    Operating system


⚠️ Limitations
•Reactive only — explains errors, does not prevent them
•No memory — each command is treated independently
•No file reading — only sees error messages, not your code
•Model intelligence — gemma:2b is lightweight, complex errors
may get incomplete explanations
•Heat sensitive — running AI on laptops generates heat,
use on hard flat surfaces only

🔮 Future Plans
[*] Version 2: Memory and context awareness ✅
[*] Version 2: Command History tracking ✅
[*] Version 2: Repeat error detection ✅
[*] Version 2: Context aware AI responses ✅
[*] Version 2: SQLite memory database ✅
[ ] Version 3: Color coded terminal output
[ ] Version 3: Error history log file
[ ] Version 4: Code file reading for smarter debugging
[ ] Version 4: Memory of past errors in same session
[ ] Version 5: Docker, npm, Git specific error handlers
[ ] Version 5: Suggested next commands

👤 Author
Built by Meghana Nagiri
Learning project — built from scratch on Ubuntu Linux


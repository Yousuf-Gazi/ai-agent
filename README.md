# AI Agent

A toy agentic AI tool built with **Google's Gemini API**. Inspired by OpenCode, Cursor, and Claude Code, this project demonstrates how to build a custom AI agent capable of reasoning, interacting with a codebase, and performing tasks autonomously.

---

## Project Overview

This CLI-based AI agent can assist with coding tasks by interacting directly with a project directory. Using Google's Gemini LLM, it can:

- Analyze code
- Read and modify files
- Execute Python scripts
- Repeat these steps iteratively to complete user-defined tasks

The project is designed as a **sandboxed, safe environment** where the agent only interacts with a specific working directory (`./calculator`) to prevent unintended file operations.

---

## Project Structure

```bash
ai-agent/
├── .gitignore
├── .python-version
├── calculator/
│   ├── lorem.txt
│   ├── main.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   ├── morelorem.txt
│   │   └── render.py
│   ├── README.md
│   └── tests.py
├── call_function.py
├── config.py
├── functions/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python.py
│   └── write_file.py
├── main.py
├── prompts.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── tests.py
└── uv.lock

```

---

## Demo Video

Check out the AI Agent in action:

[▶️ Watch the Demo](https://youtu.be/tsA5Pcy9_ok?si=zAbSgtWxcbVkNuiq)

---

## Features

- Multi-turn conversation with the AI for planning and executing coding tasks
- Function-based toolset for safe, controlled code operations:
  - Scan directories
  - Read file contents
  - Overwrite files
  - Execute Python scripts
- CLI interface for simple, interactive use
- Context preservation across multiple tool calls
- Extensible architecture to add more functions or integrate other LLM providers

---

## Tech Stack

- **Python 3.12+**
- **Google Gemini API** (`google-genai`)
- CLI-based interface with `argparse`

---

## Setup & Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd ai-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key in a .env file:

```bash
GEMINI_API_KEY=your_api_key_here
```

4. Verify Python version (3.12+ recommended):

```bash
python --version
```

---

## Usage

Run the agent from the command line:

```bash
python main.py "fix my calculator app, it's not starting correctly" --verbose
```

- `--verbose` will print detailed debug logs for tool calls and LLM interactions.
- The agent iteratively chooses the best functions to solve the task.

---

## Architecture & How It Works

### Core Components

- **main.py** – Orchestrates the agent workflow:
  - Loads the API key
  - Collects user prompts
  - Handles multi-turn execution loop (up to `MAX_ITERATIONS`)
- **call_function.py** – Maps LLM function calls to Python functions:
  - Provides the agent with a toolbox (`available_functions`)
  - Executes tool calls safely within the working directory
- **functions/** – Implements tools available to the AI:
  - `get_files_info.py` – Lists files in a directory
  - `get_file_content.py` – Reads file content with length constraints
  - `write_file.py` – Writes or overwrites files safely
  - `run_python.py` – Executes Python scripts and returns stdout/stderr
- **prompts.py** – Contains system prompt instructions to guide the AI agent’s behavior.
- **config.py** - Project configuration
  ```py
  MAX_CHARS = 10000        # Maximum characters read from files
  WORKING_DIR = "./calculator"  # Sandbox directory
  MAX_ITERATIONS = 20      # Number of iterations per task
  ```
- **calculator/** – Example working directory used to simulate real code operations.

### Workflow

1. User provides a coding task as input.
2. Agent creates a plan using Gemini LLM: which functions to call and in what order.
3. Functions are executed in a **sandboxed directory**, results are returned to the agent.
4. Agent updates context and decides the next action.
5. Iterates until the task is complete or `MAX_ITERATIONS` is reached.

---

## Example

```bash
python main.py "fix my calculator app, it's not starting correctly" --verbose
```

Sample output:

```shell
 Calling function: get_files_info
 Calling function: get_file_content
 Calling function: write_file
 Calling function: run_python_file
 Calling function: write_file
 Calling function: run_python_file
 Final response:
 Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```

---

## Skills Demonstrated

- Multi-directory Python project organization
- How agentic AI tools interact with codebases
- Functional programming with Python
- Building an AI agent using pre-trained LLMs for autonomous reasoning

---

## Extending the Project

After completing the core project, you can experiment with:

- Fixing more complex bugs or refactoring code
- Adding new functions to the AI’s toolbox
- Integrating other LLM providers or models
- Running the agent on different codebases

> ⚠️ **Warning:** Giving an LLM access to filesystem and Python interpreter should always be done cautiously.

---

## License

This project is for learning purposes and personal use.  
Use at your own risk.

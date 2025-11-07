# Gemini CLI AI Agent

A simple command-line AI agent using the free tier from Google Gemini AI Studio.

## Description

This project is a command-line based AI agent that connects to the Gemini model (`gemini-2.0-flash-001`). The agent can operate in an interactive mode, maintaining conversation context, or accept single-shot commands.

The agent's primary feature is its ability to invoke local tools (Python scripts) based on user commands. The AI model is instructed to format its response as a tool-call request when needed, allowing it to interact with the local file system.

## Requirements

* **Python 3.12+**
* **Dependencies**:
    * `google-genai==1.12.1`
    * `python-dotenv==1.1.0`

## Installation and Setup

1.  Clone the repository (or download the files).

2.  Install the required dependencies. Using a virtual environment is recommended:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install google-genai==1.12.1 python-dotenv==1.1.0
    ```
    (Alternatively, if you use `uv`, you can install from the `uv.lock` file).

3.  Obtain an API key from [Google AI Studio](https://aistudio.google.com/).

4.  Create a `.env` file in the root directory of the project and add your API key:
    ```
    GEMINI_API_KEY=YOUR_API_KEY_HERE
    ```

## Usage

The main script is `main.py`.

### Interactive Mode

To run the agent in interactive mode, where it remembers conversation history and can call tools:

```bash
python main.py

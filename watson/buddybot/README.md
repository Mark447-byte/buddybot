# BuddyBot - Local Agentic Assistant

BuddyBot is a local-first, agentic virtual assistant built in Python, designed to operate on low-resource hardware. It supports both text and voice input (Push-to-Talk) and uses a local language model (via Ollama) for reasoning and planning.

## Features
- **Agentic Loop:** Plans, executes tools, and reflects on results.
- **Multi-Modal Input:** CLI-based text input and user-triggered voice input.
- **Local Memory:** SQLite-backed task management and interaction history.
- **Privacy First:** All processing happens locally (except optional online STT).

## Requirements
- Python 3.10 or higher
- [Ollama](https://ollama.com/) (running locally)
- Microphone (for voice input)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r buddybot/requirements.txt
   ```
   *Note: On Windows, if PyAudio installation fails, try `pip install pipwin` then `pipwin install pyaudio`.*

2. **Setup Ollama:**
   - Install Ollama from [ollama.com](https://ollama.com/).
   - Pull the default model:
     ```bash
     ollama pull phi3:mini
     ```

## Usage

1. **Start the assistant:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python buddybot/main.py
   ```

2. **Interaction:**
   - BuddyBot will prompt you to choose between **Text (T)** or **Voice (V)**.
   - For **Voice**, press Enter to start recording, speak your goal, and BuddyBot will transcribe and process it.
   - Type `exit` to quit.

## Project Structure
- `buddybot/main.py`: Entry point.
- `buddybot/agent/`: Core reasoning and loop logic.
- `buddybot/llm/`: Client for Ollama.
- `buddybot/tools/`: Python-based tools (file, task, shell).
- `buddybot/memory/`: Long-term (SQLite) and short-term (RAM) memory.
- `buddybot/speech/`: Audio recording and transcription modules.
- `buddybot/input/`: User input routing and handlers.
- `buddybot/utils/`: System health checks and utilities.
- `buddybot/data/`: SQLite database storage.
- `buddybot/logs/`: Temporary audio files and logs.

## Configuration
Settings can be adjusted in `buddybot/config/settings.yaml`.

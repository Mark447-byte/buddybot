import os
import yaml
import sys

from llm.ollama_client import OllamaClient
from memory.long_term import LongTermMemory
from memory.short_term import ShortTermMemory
from tools.task_tools import TaskTools
from agent.loop import AgentLoop
from input.input_controller import InputController
from utils.system_check import run_all_checks, wait_for_ollama

def load_config():
    # Calculate path relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "settings.yaml")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading config: {str(e)}")
    return {}

def _setup_voice_input(config):
    """Try to set up voice input. Returns VoiceInput or None for text-only mode."""
    try:
        from speech.audio_recorder import AudioRecorder
        from speech.speech_to_text import SpeechToText
        from input.voice_input import VoiceInput
        recorder = AudioRecorder(max_seconds=config.get('voice', {}).get('max_record_seconds', 10))
        stt = SpeechToText(
            mode=config.get('voice', {}).get('transcription_mode', 'online'),
            language=config.get('voice', {}).get('language', 'en-US')
        )
        return VoiceInput(recorder, stt)
    except Exception as e:
        print(f"  Voice setup failed: {e}")
        return None

def main():
    print("=== BuddyBot: Local Agentic Assistant ===")
    config = load_config()
    
    # System checks (Ollama + Voice)
    ollama_ok, voice_ok = run_all_checks(config)
    
    # Wait for Ollama so LLM features work (retry until ready or user skips)
    if not ollama_ok:
        wait_for_ollama(config)
    
    # Initialize components
    llm_client = OllamaClient(
        model=config.get('llm', {}).get('model', 'tinyllama'),
        api_url=config.get('llm', {}).get('api_url', 'http://localhost:11434/api/generate')
    )
    
    long_term_mem = LongTermMemory()
    short_term_mem = ShortTermMemory()
    task_tools = TaskTools(long_term_mem)
    
    # Pass short_term_mem to AgentLoop
    agent = AgentLoop(llm_client, task_tools, long_term_mem, short_term_mem)
    
    # Voice input: use if available, else text-only
    voice_in = _setup_voice_input(config) if voice_ok else None
    input_ctrl = InputController(voice_input=voice_in)
    
    print("\nBuddyBot is ready. Type 'exit' to quit.")
    
    while True:
        try:
            user_goal = input_ctrl.get_user_goal()
            
            if user_goal.lower() in ['exit', 'quit']:
                print("BuddyBot: Goodbye!")
                break
                
            if not user_goal.strip():
                continue
                
            response = agent.run(user_goal)
            print(f"\nBuddyBot Execution Summary:\n{response}")
            
        except KeyboardInterrupt:
            print("\nBuddyBot: Goodbye!")
            break
        except EOFError:
            print("\nBuddyBot: Goodbye!")
            break
        except Exception as e:
            print(f"BuddyBot encountered a system error: {str(e)}")

if __name__ == "__main__":
    main()

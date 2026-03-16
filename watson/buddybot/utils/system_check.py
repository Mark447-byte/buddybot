import requests
import os

def check_ollama(api_url, model_name):
    """Checks if Ollama is running and has the required model."""
    try:
        # Check connectivity
        tags_url = api_url.replace("/generate", "/tags")
        response = requests.get(tags_url, timeout=5)
        if response.status_code != 200:
            return False, f"Ollama returned status code {response.status_code}"
            
        models = response.json().get("models", [])
        model_exists = any(m.get("name") == model_name or (m.get("name") or "").startswith(model_name) for m in models)
        
        if not model_exists:
            return False, f"Model '{model_name}' not found. Run: ollama pull {model_name}"
            
        return True, "Ollama is running and model is available."
    except requests.exceptions.ConnectionError:
        return False, "Ollama is not running."
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_microphone():
    """Checks if voice input (PyAudio + microphone) is available. Safe to call even if deps missing."""
    try:
        import speech_recognition as sr
        with sr.Microphone() as source:
            return True, "Microphone is accessible."
    except ImportError as e:
        return False, f"Voice deps missing (PyAudio/SpeechRecognition): {e}"
    except Exception as e:
        return False, f"Microphone access failed: {str(e)}"

def run_all_checks(config):
    """Run health checks. Returns (ollama_ok, voice_ok)."""
    llm_conf = config.get('llm', {})
    api_url = llm_conf.get('api_url', 'http://localhost:11434/api/generate')
    model_name = llm_conf.get('model', 'tinyllama')
    
    print("\nBuddyBot System Health Check:")
    
    ollama_ok, ollama_msg = check_ollama(api_url, model_name)
    print(f"  [{'OK' if ollama_ok else 'FAIL'}] Ollama: {ollama_msg}")
    
    mic_ok, mic_msg = check_microphone()
    print(f"  [{'OK' if mic_ok else 'WARN'}] Voice: {mic_msg}")
    
    if not ollama_ok:
        print("\n  To fix: 1) Run 'ollama serve' in a terminal  2) Run 'ollama pull " + model_name + "'")
    if not mic_ok:
        print("  Running in text-only mode (voice input disabled).")
    
    return ollama_ok, mic_ok

def wait_for_ollama(config):
    """Retry Ollama check until ready or user skips. Returns True if Ollama is ready."""
    llm_conf = config.get('llm', {})
    api_url = llm_conf.get('api_url', 'http://localhost:11434/api/generate')
    model_name = llm_conf.get('model', 'tinyllama')
    
    while True:
        ok, msg = check_ollama(api_url, model_name)
        if ok:
            return True
        print("\n" + "="*50)
        print("Ollama is not ready. LLM features require Ollama.")
        print("  1. Open a new terminal")
        print("  2. Run: ollama serve")
        print("  3. Run: ollama pull " + model_name)
        print("="*50)
        choice = input("Press Enter to retry, or type 'skip' to continue anyway: ").strip().lower()
        if choice == 'skip':
            print("Continuing without Ollama. LLM features will return errors.")
            return False

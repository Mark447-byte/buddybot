import requests
import json

class OllamaClient:
    def __init__(self, model="tinyllama", api_url="http://localhost:11434/api/generate"):
        self.model = model
        # Use chat API (more stable); fallback to generate for older Ollama
        base = api_url.replace("/api/generate", "").replace("/api/chat", "")
        self.chat_url = f"{base.rstrip('/')}/api/chat"
        self.generate_url = f"{base.rstrip('/')}/api/generate"

    def generate(self, prompt, system_prompt=None):
        # Prefer chat API (avoids 500 errors seen with /api/generate in some Ollama versions)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            payload = {"model": self.model, "messages": messages, "stream": False}
            response = requests.post(self.chat_url, json=payload, timeout=60)
            if response.status_code == 404:
                # Older Ollama: fallback to generate API
                return self._generate_legacy(prompt, system_prompt)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "") or ""
        except requests.exceptions.HTTPError as e:
            body = ""
            try:
                body = response.text[:500] if response else ""
            except Exception:
                pass
            return f"Error connecting to Ollama: {e}. {body}"
        except requests.exceptions.ConnectionError:
            return "Error connecting to Ollama: Connection refused. Is Ollama running? Run 'ollama serve'."
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def _generate_legacy(self, prompt, system_prompt=None):
        """Fallback for Ollama versions that only have /api/generate."""
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system_prompt:
            payload["system"] = system_prompt
        try:
            response = requests.post(self.generate_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def chat(self, messages):
        try:
            payload = {"model": self.model, "messages": messages, "stream": False}
            response = requests.post(self.chat_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

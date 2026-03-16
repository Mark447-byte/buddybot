import json

class Planner:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def plan(self, user_goal, context=""):
        # Explicitly mention context in the prompt if it exists
        context_prompt = ""
        if context:
            context_prompt = f"\nRecent Interaction History:\n{context}\nUse this history to understand the user's intent or follow-up questions."

        prompt = f"""
You are BuddyBot, a local agentic assistant.
User Goal: {user_goal}
{context_prompt}

Break down the user goal into a list of steps. 
Available tools:
- list_files(directory)
- read_file(filepath)
- write_file(filepath, content)
- add_task(content)
- list_tasks(status)
- complete_task(task_id)
- execute_shell(command)

Output ONLY a JSON list of steps. Do not include any other text or markdown formatting. 
Each step must have a 'description' and a 'tool' if applicable (with 'args').

Example 1:
Goal: "Tell me what files are in this folder"
[
  {{"description": "List files in current directory", "tool": "list_files", "args": {{"directory": "."}}}}
]

Example 2:
Goal: "Remind me to buy milk"
[
  {{"description": "Add a task to buy milk", "tool": "add_task", "args": {{"content": "Buy milk"}}}}
]

Example 3:
Goal: "Check the contents of secrets.txt"
[
  {{"description": "Read the secrets.txt file", "tool": "read_file", "args": {{"filepath": "secrets.txt"}}}}
]

Example 4 (informational - no tool needed):
Goal: "What can you do?"
[
  {{"description": "BuddyBot can: list_files(directory), read_file(filepath), write_file(filepath, content), add_task(content), list_tasks(status), complete_task(task_id), execute_shell(command). I help with file operations, task management, and running shell commands.", "tool": null, "args": {{}}}}
]

Now, generate the steps for: "{user_goal}"
"""
        response = self.llm_client.generate(prompt)
        # If LLM returned an error (e.g. Ollama 500), don't try to parse as JSON
        if response.strip().lower().startswith("error connecting to ollama"):
            return [{
                "description": "Ollama connection failed. Ensure Ollama is running (ollama serve) and the model is pulled (ollama pull tinyllama). Run 'ollama list' to see available models.",
                "tool": None,
                "args": {}
            }]
        try:
            # Try to find JSON in the response
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                parsed = json.loads(json_str)
                if not isinstance(parsed, list):
                    raise ValueError("Expected JSON array")
                # Ensure each step has description, tool, args
                for s in parsed:
                    if not isinstance(s, dict):
                        continue
                    s.setdefault("description", "Unknown step")
                    s.setdefault("tool", None)
                    s.setdefault("args", s.get("args") or {})
                return parsed
            # If not found, try to clean up the response
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.split('\n', 1)[-1]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            parsed = json.loads(cleaned_response.strip())
            if not isinstance(parsed, list):
                raise ValueError("Expected JSON array")
            return parsed
        except json.JSONDecodeError as e:
            return [{"description": f"Error parsing plan from LLM: {e}. Raw: {response[:200]}...", "tool": None, "args": {}}]
        except Exception as e:
            return [{"description": f"Plan error: {str(e)}", "tool": None, "args": {}}]

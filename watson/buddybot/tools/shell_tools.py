import subprocess

def execute_shell(command):
    try:
        # Warning: executing shell commands can be dangerous.
        # In a real app, you'd want more safety checks.
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

import os

def list_files(directory="."):
    try:
        return os.listdir(directory)
    except Exception as e:
        return str(e)

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(filepath, content):
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return str(e)

import os

def run_command(command: str):
    print(f"Running command: {command}")
    result = os.system(command)
    return result

def write_file(input_data: dict):
    """Write content to a file directly, avoiding shell quoting issues."""
    file_path = input_data.get("file")
    content = input_data.get("content")

    if not file_path or content is None:
        return "Error: Both file path and content are required"

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote content to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input and runs it in the shell. Returns the output of the command.",
    },
    "write_file": {
        "fn": write_file,
        "description": "Takes a dictionary with 'file' (path) and 'content' keys and writes the content directly to the file without shell quoting issues.",
    }
}
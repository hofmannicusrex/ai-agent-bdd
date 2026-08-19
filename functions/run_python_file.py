import os
import subprocess
from subprocess import CompletedProcess

# Function description to be used by the AI agent.
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs Python files that are located at a specified file path relative to the working directory. Optionally, arguments can be passed in as a list of strings.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "Any additional that need passed to the command. These arguments are specifed by the user",
                    "items": {
                        "type": "string",
                        "description": "A single additional argument to be passed to the command"
                    }
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Get the absolute paths of the "working directory" and the complete path to the file.
        # This is required in order to perform the downstream logic.
        working_dir_abs_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # Return an "error" string if the file path provided is outside of the working directory.
        if os.path.commonpath([working_dir_abs_path, abs_file_path]) != working_dir_abs_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

        # print("################################################")
        # print(f"The value of 'abs_file_path' is: {abs_file_path}")
        # print(f"Is 'abs_file_path' a file? {os.path.isfile(abs_file_path)}")
        # print("################################################")

        # Return an "error" string if the file path argument provided is not a file.
        if not os.path.isfile(abs_file_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"

        # Return an "error" string if the file name doesn't end with '.py'.
        if not abs_file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"

        # All checks have passed! Start building the command that will run the subprocess.
        command = ["python", abs_file_path]

        # Add any additional arguments the user provided to the command object.
        if args:
            for arg in args:
                command.extend(arg)

        # Run the subprocess, passing in any additional arguments the user provided.
        completed_subprocess: CompletedProcess[str] = subprocess.run(command, capture_output=True, timeout=30, text=True)

        # Build an output string based on the 'completed_subprocess' (CompletedProcess) object.
        command_output: str = "Command Output Summary:\n--------"

        # Non-zero exit code... should indicate an issue.
        if completed_subprocess.returncode != 0:
            command_output += f"\nProcess exited with code {completed_subprocess.returncode}"

        # No 'stdout' and no 'stderr' from the command.
        if not completed_subprocess.stdout and not completed_subprocess.stderr:
            command_output += "\nNo output produced"
        else:
            command_output += f"\nSTDOUT: {completed_subprocess.stdout}"
            command_output += f"\nSTDERR: {completed_subprocess.stderr}"

        # return "Succesfully reached the end of the function!"
        return command_output

    # Return any other errors as an "error string".
    except Exception as e:
        return f"Error: executing Python file: {e}"

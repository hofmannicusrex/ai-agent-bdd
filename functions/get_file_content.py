import os

from config import MAX_CHARS

# Function description to be used by the AI agent.
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a file at a specified file path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file, relative to the working directory",
                },
            },
        "required": ["file_path"]
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # Get the absolute paths of the "working directory" and the complete path to the file.
        # This is required in order to perform the downstream logic.
        working_dir_abs_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # Return an "error" string if the file path provided is outside of the working directory.
        if os.path.commonpath([working_dir_abs_path, abs_file_path]) != working_dir_abs_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        # Return an "error" string if the file path argument provided is not a file.
        if not os.path.isfile(abs_file_path):
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        # Read the maximum number of characters from the file.
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)

            # Tell the user that the file's contents were truncated if the file contains
            # more characters than the maximum number of characters allowed.
            if f.read(1):
                file_content += (
                    f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
                )

        return file_content

    # Return any other errors as an "error string".
    except Exception as e:
        return f"Error reading file \"{file_path}\": {e}"

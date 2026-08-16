import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Get the absolute paths of the "working directory" and the complete path to the file.
        # This is required in order to perform the downstream logic.
        working_dir_abs_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # Return an "error" string if the file path provided is outside of the working directory.
        if os.path.commonpath([working_dir_abs_path, abs_file_path]) != working_dir_abs_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        # Return an "error" string if the file path argument provided is not a file.
        if os.path.isdir(abs_file_path):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"

        # Write the content to the file.
        with open(abs_file_path, mode="w") as f:
            # Ensure all parent directories of the 'file_path' exist/get created.
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            f.write(content)
            # file_content = f.read(MAX_CHARS)

        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"

    # Return any other errors as an "error string".
    except Exception as e:
        return f"Error writing to file \"{file_path}\": {e}"

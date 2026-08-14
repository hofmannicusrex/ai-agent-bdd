import os
# import io  # Is this needed?
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        print(f"working_directory value is: {working_directory}")
        print(f"working_dir_abs_path value is: {working_dir_abs_path}")

        # Return an "error" string if the file path provided is outside of the working directory.
        # if os.path.commonpath([working_dir_abs_path, file_path]) != working_dir_abs_path:  # Errors due to "Can't mix absolute and relative paths"
        if os.path.commonpath([working_dir_abs_path, os.path.abspath(file_path)]) != working_dir_abs_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory."

        # Construct the complete path to the file.
        # file_path = os.path.join(working_dir_abs_path, file_path)  # Let's not change the value of the "file_path" parameter.
        path_to_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # Return an "error" string if the file path argument provided is not a file.
        if os.path.isdir(path_to_file):
            f"Error: File not found or is not a regular file: \"{file_path}\"."

        # Read the maximum number of characters from the file.
        # io.StringIO(path_to_file).read(MAX_CHARS)  # I think this is wrong?
        file_contents: str = open(path_to_file).read(MAX_CHARS)

        # Tell the user that the file's contents were truncated if the file contains
        # more characters than the maximum number of characters allowed.
        if open(path_to_file).read(1):
            file_contents += f"[... File \"{file_path}\" truncated at {MAX_CHARS} characters]"  # Should I be using "path_to_file" instead of "file_path" here? Instructions don't say so, but idk.
    except Exception as exception:
        # We need to return a string here so that the LLM can handle errors gracefully.
        return f"Error: {exception}"

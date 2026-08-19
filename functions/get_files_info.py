import os


# Function description to be used by the AI agent.
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # Retrieve the absolute path of the working directory.
        working_dir_abs_path = os.path.abspath(working_directory)

        # Construct the full path to the target directory.
        target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))

        # Check if the target directory falls within the absolute working directory.
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path

        # If the directory supplied by the user is not valid.
        if not valid_target_dir:
            # We need to return a string here so that the LLM can handle errors gracefully.
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory."

        if not os.path.isdir(target_dir):
            # We need to return a string here so that the LLM can handle errors gracefully.
            return f"Error: \"{directory}\" is not a directory."

        # The path provided by the user was valid, proceed to next steps.
        target_directory_contents = os.listdir(target_dir)

        # Create a list to store each item in the target directory.
        directory_items: list[str] = []

        for item in target_directory_contents:
            # First, construct each item's full path. This ensures the "os.path." calls work correctly.
            item_path = os.path.join(target_dir, item)

            # Capture information about each item.
            name = item
            size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)

            # Add the current item to the list.
            directory_items.append(f"- {name}: file_size={size} bytes, is_dir={is_directory}")

        # Join things together so each item is displayed on its own line.
        directory_contents_details = "\n".join(directory_items)

        return directory_contents_details

        # return f"Success: \"{directory}\" is within the working directory."  # No longer needed???
    except Exception as exception:
        # We need to return a string here so that the LLM can handle errors gracefully.
        return f"Error: {exception}"

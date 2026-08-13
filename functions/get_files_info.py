import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # Retrieve the absolute path of the working directory.
        working_dir_abs_path = os.path.abspath(working_directory)

        # Construct the full path to the target directory.
        target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))

        # Check if the target directory falls within the absolute working directory.
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path

        if not valid_target_dir:
            # raise Exception(f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory.")
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory."

        if not os.path.isdir(directory):
            # raise Exception(f"Error: \"{directory}\" is not a directory.")
            return f"Error: \"{directory}\" is not a directory."
        return f"Success: \"{directory}\" is within the working directory."
    except Exception as exception:
        return f"Error: {exception}"

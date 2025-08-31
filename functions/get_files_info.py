import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    relative_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(relative_path)

    # check if a path within bounds
    absolute_working_dir = os.path.abspath(working_directory)
    is_within_bounds = absolute_path.startswith(absolute_working_dir)

    if not is_within_bounds:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # check if the directory argument is valid
    valid_dir = os.path.isdir(absolute_path)
    if not valid_dir:
        return f'Error: "{directory}" is not a directory'

    # show contents of the directory in a formatted manner
    try:
        formatted_lines = []
        contents = os.listdir(absolute_path)
        for filename in contents:
            full_filename_path = os.path.join(absolute_path, filename)
            file_size = os.path.getsize(full_filename_path)
            is_dir = os.path.isdir(full_filename_path)
            formatted_lines.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")

        files_info = "\n".join(formatted_lines)
        return files_info
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

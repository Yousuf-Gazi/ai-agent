import os
from google.genai import types


def write_file(working_directory, file_path, content):
    relative_path = os.path.join(working_directory, file_path)
    target_absolute_file_path = os.path.abspath(relative_path)

    # check if file is within bounds
    absolute_working_dir = os.path.abspath(working_directory)
    common_path = os.path.commonpath([absolute_working_dir, target_absolute_file_path])
    is_within_bounds = common_path == absolute_working_dir

    if not is_within_bounds:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # directory creation logic
    file_path_exists = os.path.exists(target_absolute_file_path)
    is_directory = os.path.isdir(target_absolute_file_path)

    if file_path_exists and is_directory:
        return f'Error: "{file_path}" is a directory, not a file'

    if not file_path_exists:
        try:
            file_path_dir = os.path.dirname(target_absolute_file_path)
            os.makedirs(file_path_dir, exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    # write content in the file
    try:
        with open(target_absolute_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating directories if needed. The file must be within the permitted working directory bounds.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. Must be within the permitted working directory bounds.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)

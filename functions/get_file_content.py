import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    relative_path = os.path.join(working_directory, file_path)
    target_absolute_file_path = os.path.abspath(relative_path)

    # check if file_path is within bounds
    absolute_working_dir = os.path.abspath(working_directory)
    common_path = os.path.commonpath([absolute_working_dir, target_absolute_file_path])
    is_within_bounds = common_path == absolute_working_dir

    if not is_within_bounds:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # check if file_path is a file
    valid_file_path = os.path.isfile(target_absolute_file_path)
    if not valid_file_path:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # reading file and return its contents
    try:
        with open(target_absolute_file_path, "r", encoding="utf-8", errors="replace") as f:
            file_content_string = f.read(MAX_CHARS + 1)

            if len(file_content_string) > MAX_CHARS:
                truncated_content = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return truncated_content
            
            return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file, constrained to the working directory. Files are truncated if they exceed the maximum character limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. Must be within the permitted working directory bounds.",
            ),
        },
        required=["file_path"]
    ),
)

import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    relative_path = os.path.join(working_directory, file_path)
    target_absolute_path = os.path.abspath(relative_path)

    # check if file_path is within bounds
    absolute_working_dir = os.path.abspath(working_directory)
    common_path = os.path.commonpath([absolute_working_dir, target_absolute_path])
    within_bounds = common_path == absolute_working_dir

    if not within_bounds:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # check if the file_path exists
    file_path_exists = os.path.isfile(target_absolute_path)
    if not file_path_exists:
        return f'Error: File "{file_path}" not found.'

    # check if its a python file
    python_file = target_absolute_path.endswith(".py")
    if not python_file:
        return f'Error: "{file_path}" is not a Python file.'

    # run python file
    commands = ["python3", target_absolute_path]
    if args:
        commands.extend(args)

    try:
        result = subprocess.run(
            commands,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=absolute_working_dir,
            check=True,
        )

        if not result.stdout and not result.stderr:
            return "No output produced"

        # formatting output
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}, STDOUT: {e.stdout}, STDERR: {e.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output. The file must be within the permitted working directory bounds and have a .py extension.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. Must be a .py file within the permitted working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional command-line arguments to pass to the Python script as a list of strings.",
                ),
                description="Optional command-line arguments to pass to the Python script as a list of strings.",
                nullable=True
            ),
        },
        required=["file_path"]
    ),
)

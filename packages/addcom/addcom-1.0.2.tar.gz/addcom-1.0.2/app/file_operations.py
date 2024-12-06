import os
import tomllib
from rich.console import Console

# Console instance for warning outputs
warning_console = Console(stderr=True, soft_wrap=True, style="yellow")


def load_contents(file_path: str):
    """
    Read the contents of a file and return it. If the file is not found,
    print a message and return None
    """
    if not os.path.isfile(file_path):
        warning_console.print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, "r") as file:
            return file.read()

    except IOError as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")


def write_to_output_file(output: str, commented_content: str):
    """
    Append the commented content to the specified output file
    """
    try:
        with open(output, "a") as f:
            f.write(commented_content + "\n\n")

    except IOError as e:
        raise RuntimeError(f"Error writing to file {output}: {e}")


def find_toml():
    """
    Find TOML file in the user's home directory
    """
    home_dir = os.path.expanduser("~")

    for file in os.listdir(home_dir):
        if file == "addcom_config.toml":
            return os.path.join(home_dir, file)

    warning_console.print("Config file was not found")
    return None


def read_toml(file: str):
    """
    Read the contents of the TOML and parse them using tomlib
    """
    try:
        with open(file, "rb") as f:
            data = tomllib.load(f)
            return data

    except IOError as e:
        raise RuntimeError(f"Error reading TOML file {file}: {e}")


def get_config():
    """
    Retrieve configuration settings from TOML file
    """
    toml_file = find_toml()

    if toml_file:
        config_data = read_toml(toml_file)
        return config_data

    return None

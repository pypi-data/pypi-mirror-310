import typer
from .file_operations import load_contents, read_toml


def version_callback(provided: bool):
    """
    Print current tool version if a flag option was provided
    """
    if provided:
        project_data = read_toml("pyproject.toml")
        print(project_data["tool"]["poetry"]["version"])

        raise typer.Exit()


def context_callback(context_file: str) -> str:
    """
    Load contents of example file
    """
    if context_file:
        context_contents = load_contents(context_file)
        return context_contents

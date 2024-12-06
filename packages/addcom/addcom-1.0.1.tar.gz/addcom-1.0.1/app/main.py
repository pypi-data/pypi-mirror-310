import sys

import typer
from typing_extensions import Annotated
from typing import Optional

from rich import print
from rich.console import Console
from rich.markup import escape

from .callbacks import version_callback, context_callback
from .file_operations import load_contents, write_to_output_file, get_config
from .api import generate_comments


# Console instance for error output
error_console = Console(stderr=True, soft_wrap=True, style="red")

# Create Typer instance
app = typer.Typer()


@app.command()
def add_comments(
    file_paths: Annotated[
        list[str], typer.Argument(..., help="Paths to source code files to be commented")
    ],
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="See the current tool version",
            is_eager=True,
            callback=version_callback,
        ),
    ] = None,
    context: Annotated[
        Optional[str],
        typer.Option(
            "--context",
            "-c",
            help="Path to example file to provide context for the LLM",
            callback=context_callback,
        ),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option(
            "--output", "-o", help="Specify an output filename to save the commented code"
        ),
    ] = None,
    stream: Annotated[
        Optional[bool],
        typer.Option("--stream", "-s", help="Stream the response live as it updates"),
    ] = False,
    api_key: Annotated[
        Optional[str],
        typer.Option("--api-key", "-a", help="Provide API key for authentication"),
    ] = None,
    base_url: Annotated[
        Optional[str],
        typer.Option("--base-url", "-u", help="Specify base URL for the API"),
    ] = None,
    model: Annotated[
        Optional[str],
        typer.Option("--model", "-m", help="Specify a LLM to use for comment generation"),
    ] = None,
):
    """
    Add comments to each of the provided files.
    """

    try:
        # Get default settings from TOML file (if present in user's home dir)
        config_data = get_config()

        # CLI arguments take precedence over default settings
        if config_data is not None:
            context = context or config_data.get("context")
            api_key = api_key or config_data.get("api_key")
            stream = stream or config_data.get("stream", False)
            model = model or config_data.get("model")

        # Add comments to provided file(s)
        for file_path in file_paths:
            content = load_contents(file_path)

            if content:
                commented_content = generate_comments(
                    file_path, content, context, api_key, base_url, model, stream
                )

                if output:
                    write_to_output_file(output, commented_content)
                elif not stream:
                    print(f"--- {file_path} with added comments ---\n\n")
                    print(escape(commented_content) + "\n\n")

    except Exception as e:
        error_console.print(e)
        sys.exit(1)


if __name__ == "__main__":
    app()

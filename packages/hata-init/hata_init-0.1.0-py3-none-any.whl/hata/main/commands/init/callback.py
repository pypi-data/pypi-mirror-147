import pathlib as pt
import platform
from typing import List
import venv as ve

import typer

from .app_creator import AppCreator
from .utils import ConfigType

def callback(
    name: str = typer.Argument(
        ...,
        help="The name of the project, if the current working directory"
        "doesn't match the name then a project folder will also be created"
    ),
    plugin_folder: str = typer.Option(
        "plugin",
        help="The name of the folder in which your extensions are stored. By default './plugins'"
    ),
    config: ConfigType = typer.Option(
        "env",
        help="Where should the bot secrets be loaded from"
        " has five choices 'env', 'dotenv', 'toml', 'json' and 'python'\n"
        "env uses environment variables, dotenv uses the 3rd party library "
        "'python-dotenv' to load the environment variables from a .dotenv file. "
        "toml and json use the corresponding secret.toml and secret.json for loading secrets. "
        "python simply creates a secret.py file and imports it for configuration."
    ),
    bots: List[str] = typer.Option(None, help="The names of bots in the app."),
    venv: bool = typer.Option(
        False,
        help=f"Create a basic virtual venv named .venv/ with python {platform.python_version()}"
    )
):
    maker = AppCreator(name, pt.Path.cwd(), bots, plugin_folder, config)
    try:
        if venv:
            typer.echo("Creating venv")
            ve.create(maker.path / ".venv")

        maker.make_gitignore()
        maker.make_main()
        maker.make_readme()
    except Exception as err:
        typer.echo(typer.style("Failed", fg=typer.colors.BRIGHT_RED))
        raise err from None

    typer.echo(typer.style("Success!", fg=typer.colors.BRIGHT_GREEN))
    typer.Exit()

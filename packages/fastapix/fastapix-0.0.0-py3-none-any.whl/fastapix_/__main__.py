import logging
import platform

import typer
from rich.console import Console
from rich_click.typer import Typer

from fastapix_.logger import logger

__version__ = "0.0.0"

app = Typer(
    name="FastAPI X",
    help="Manage your FastAPI project.",
    no_args_is_help=True,
    invoke_without_command=True,
)


def version_callback(value: bool):
    if value:
        typer.echo(
            "Running FastAPI X {} with {} {} on {}.".format(
                __version__,
                platform.python_implementation(),
                platform.python_version(),
                platform.system(),
            )
        )
        raise typer.Exit(1)


def debug_callback(value: bool):
    if value:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")


@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        callback=debug_callback,
        is_eager=True,
        help="Enable debug mode.",
        hidden=True,
    ),
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    ctx.obj = {"console": Console()}


@app.command()
def template() -> None:
    """Generate a project using a template."""


@app.command()
def structure():
    """Set project structure."""


@app.command()
def info():
    """Information about FastAPI and underlying technologies."""


@app.command()
def lint():
    """Lint your FastAPI project with flake8-fastapi."""


if __name__ == "__main__":
    app()

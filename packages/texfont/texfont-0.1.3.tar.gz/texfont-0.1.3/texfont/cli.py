"""Console script for texfont."""

import typer
from rich.console import Console

from .font.install import install_fonts

app = typer.Typer()
console = Console()


@app.command()
def main(
        cmd: str = typer.Argument(..., help="The command to execute (e.g., 'install').")
):
    if cmd == "install":
        install_fonts()
    if cmd == "clean":
        print("clean")


if __name__ == "__main__":
    app()

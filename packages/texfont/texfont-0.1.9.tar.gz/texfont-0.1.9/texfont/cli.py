"""Console script for texfont."""
from typing import List

import typer
from rich.console import Console

from texfont.font.list import list_fonts
from .font.install import install_fonts, install_all_fonts

app = typer.Typer()
console = Console()


@app.command(name="install", help="Install specified fonts.")
def install_fonts_cli(names: List[str] = typer.Argument(None, help="Names of the fonts to process."),
                      install_all: bool = typer.Option(False, "--all", help="Install all available fonts."),
                      is_admin: bool = typer.Option(True, "--admin/--no-admin",
                                                    help="Install all fonts in admin mode."), ):
    if install_all:
        print("Installing all available fonts...")
        install_all_fonts(is_admin=is_admin)
        return

    install_fonts(names, is_admin=is_admin)


@app.command(name="list",
             help="List all available fonts. See https://github.com/google/fonts/tree/main/ofl and https://fonts.google.com/")
def list_fonts_cli(
        name: str = typer.Argument(None, help="Name of the font to list."),
        is_admin: bool = typer.Option(True, "--admin/--no-admin", help="Install all fonts in admin mode.")):
    list_fonts(search_content=name, is_admin=is_admin)


if __name__ == "__main__":
    app()

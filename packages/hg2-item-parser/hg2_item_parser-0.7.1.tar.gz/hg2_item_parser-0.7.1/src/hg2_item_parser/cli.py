import functools
from pathlib import Path
from typing import Annotated

import typer

from .item_parser import ItemParser

app = typer.Typer()

output_option = typer.Option(
    "--output",
    "-o",
    help="Path to the file where parsed items will be saved.",
)

data_dir_option = typer.Option(
    "--data-dir",
    "-d",
    help="Path to the directory where data files are located.",
)

item_id_argument = typer.Argument(
    help="Ingame item id",
)


def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.secho(e, fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    return wrapper


@app.command()
@handle_errors
def check(
    item_id: Annotated[int, item_id_argument],
    data_dir: Annotated[Path, data_dir_option] = Path("extracted"),
) -> None:
    """
    Parses and prints a single item by ID.
    """
    parser = ItemParser(data_dir)
    item = parser.parse_item(item_id)
    typer.echo(item)


@app.command()
@handle_errors
def parse(
    item_id: Annotated[int | None, item_id_argument] = None,
    item_range: Annotated[
        tuple[int, int] | None,
        typer.Option(
            "--range",
            "-r",
            help="Range of item IDs to parse (start and end, inclusive).",
        ),
    ] = None,
    output: Annotated[
        Path,
        output_option,
    ] = Path("parsed/items.txt"),
    data_dir: Annotated[
        Path,
        data_dir_option,
    ] = Path("extracted"),
) -> None:
    """
    Parses and writes a single item or a range of items by ID(s).
    """
    parser = ItemParser(data_dir)

    if item_id is not None:
        parser.parse_and_write_item(item_id, output)
    elif item_range is not None:
        parser.parse_and_write_items_from_to(*item_range, output, progressbar=True)
    else:
        typer.secho(
            "You must specify either an item ID or a range using --range[-r].",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)


def main() -> None:
    app()

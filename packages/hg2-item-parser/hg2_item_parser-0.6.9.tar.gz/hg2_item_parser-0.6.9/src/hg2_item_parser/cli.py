from pathlib import Path
from typing import Annotated

import typer

from .item_parser import ItemParser

app = typer.Typer()


@app.command(help="Prints an item to a console")
def check(
    item_id: int, data_dir: Annotated[Path, typer.Argument()] = Path("extracted")
) -> None:
    parser = ItemParser(data_dir)
    item = parser.parse_item(item_id)
    typer.echo(item)


@app.command(help="Parses items in range")
def parse_from_to(
    first_item_id: int,
    last_item_id: int,
    output: Annotated[Path, typer.Argument()] = Path("parsed/items.txt"),
    data_dir: Annotated[Path, typer.Argument()] = Path("extracted"),
) -> None:
    parser = ItemParser(data_dir)
    parser.parse_and_write_items_from_to(
        first_item_id, last_item_id, output, progressbar=True
    )


@app.command(help="Parses an item")
def parse(
    item_id: int,
    output: Annotated[Path, typer.Argument()] = Path("parsed/items.txt"),
    data_dir: Annotated[Path, typer.Argument()] = Path("extracted"),
) -> None:
    parser = ItemParser(data_dir)
    parser.parse_and_write_item(item_id, output)


def main() -> None:
    app()

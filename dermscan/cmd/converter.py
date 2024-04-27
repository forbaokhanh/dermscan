import csv
import json
import os
from typing import List, Any

import click

from dermscan.models import Ingredient
from dermscan.shared import success, bold_error, info


@click.command("tojson")
@click.option(
    "--from-path",
    "-f",
    "source_path",
    type=click.Path(exists=True),
    help="Path to the file to convert.",
)
def tojson(source_path: str):
    """Convert a txt or csv file to JSON."""
    path, extension = os.path.splitext(source_path)
    if extension not in [".txt", ".csv"]:
        click.echo(
            bold_error("Invalid file format.")
            + info(" Please provide a txt or csv file.")
        )
        return

    json_path = path + ".json"
    data = _read_contents(source_path, extension)
    with open(json_path, "w") as write_file:
        write_file.write(json.dumps(data, indent=4))
    click.echo(success("Successfully converted the file to JSON. {}".format(json_path)))


def _read_contents(source_path: str, extension: str) -> List[Any]:
    """Read the contents of the file and return a list of data (str or dict)."""
    if extension == ".txt":
        with open(source_path, "r") as file:
            data = [line.strip().lower() for line in file.readlines()]

    elif extension == ".csv":
        with open(source_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data = [
                Ingredient(
                    row["Name"].strip().lower(), row["Comedogenicity"], row["Irritancy"]
                ).as_dict()
                for row in reader
            ]
            data = sorted(
                data, key=lambda x: (x["comedogenicity"], x["irritancy"]), reverse=True
            )
    return data

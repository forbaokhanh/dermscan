import csv
import json
import os
from typing import List, Any

import click
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from dermscan.models import Ingredient
from dermscan.utils.printers import show_error, show_success

RESOURCES_PATH = os.path.expanduser("~/dev/dermscan/resources/")


@click.command("db-format")
def db_format():
    """Convert a txt or csv file to JSON."""
    home_path = RESOURCES_PATH
    filepath = inquirer.filepath(
        message="Enter the path to the resource file you'd like to convert to JSON:",
        default=home_path,
        validate=PathValidator(
            is_file=True,
            message="File must exist within the 'dermscan/resources/' directory.",
        ),
    ).execute()

    filename, extension = os.path.splitext(filepath)
    if extension not in [".txt", ".csv"]:
        show_error("Invalid file format. Please provide a txt or csv file.")
        return

    json_path = filename + ".json"
    data = _read_contents(filepath, extension)
    with open(json_path, "w") as write_file:
        write_file.write(json.dumps(data, indent=4))
    show_success("Successfully converted the file to JSON. {}".format(json_path))


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

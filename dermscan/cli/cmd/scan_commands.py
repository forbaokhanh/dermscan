import os

import click
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from dermscan.cli.cmd.input_commands import parse_ingredients
from dermscan.utils.printers import show_success

# Define the allowed file options
ALLOWED_FILES = ["acneclinic.json", "detailed.json", "original.json"]
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


@click.command(name="run")
def dermscan_run() -> None:
    """
    Search for ingredients in the database.
    """
    ingredients = parse_ingredients()
    show_success("Input ingredients parsed successfully.")

    home_path = os.path.expanduser("~/dev/dermscan/resources/")
    reference_path = inquirer.filepath(
        message="Enter the path to reference file. Use -g flag to search globally:",
        default=home_path,
        validate=PathValidator(
            is_file=True,
            message="File must exist within the 'dermscan/resources/' directory.",
        ),
    ).execute()

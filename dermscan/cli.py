import json
import os

import click
import pyperclip

from dermscan.models import StringDatabaseMatcher
from .cmd import tojson

# Define the allowed file options
ALLOWED_FILES = ["acneclinic.json", "detailed.json", "original.json"]
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


# Main entry point for CLI
@click.group()
def cli():
    """Main entry point for CLI."""
    pass


@cli.command(name="run")
@click.option(
    "--reference-path",
    "-r",
    type=click.Choice(ALLOWED_FILES),
    default="acneclinic.json",
    help="Path to the file containing the reference data (acneclinic.json, detailed.json, or original.json).",
)
def dermscan_run(reference_path: str) -> None:
    """
    Search for ingredients in the database.
    """
    # Construct the file path to the JSON file
    file_path = os.path.join(RESOURCES_DIR, reference_path)

    with open(file_path, "r") as file:
        data = json.load(file)

    matcher = StringDatabaseMatcher(data)

    lines = pyperclip.paste().split("\n")
    contents = [item.strip().lower() for line in lines for item in line.split(",")]
    matcher.report(contents)


# Add subcommands to the main CLI
cli.add_command(tojson)

if __name__ == "__main__":
    cli()

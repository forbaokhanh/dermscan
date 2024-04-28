import os
from typing import List

import click
from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator
from colorama import Fore

from dermscan.models.llm import LLM
from dermscan.models.parser import parse_html
from dermscan.models.scraper import UrlScraper
from dermscan.utils import inputs, info, bold_error


@click.command("parse")
@click.option(
    "--allow-global",
    "-g",
    is_flag=True,
    help="Allow searching through global paths for input files.",
    default=False,
)
def parse_ingredients(allow_global: bool = False) -> List[str]:
    """
    Parse the clipboard contents to extract list of items.

    Returns:
    List[str]: A list of cleaned and normalized strings.
    """
    input_method = inquirer.select(
        message="Select input method:",
        choices=["clipboard", "input file", "user input", "URL"],
        pointer="=>",
        show_cursor=True,
        cycle=True,
    ).execute()

    if input_method == "clipboard":
        return inputs.parse_clipboard()
    elif input_method == "input file":
        click.echo(
            info(
                "Note: The file must be located within the 'dermscan/inputs/' directory."
                + " Use -g flag to search globally."
            )
        )

        # Prompt the user to enter the file path within the 'dermscan/inputs/' directory.
        home_path = (
            os.path.expanduser("~")
            if allow_global
            else os.path.expanduser("~/dev/dermscan/inputs/")
        )
        file_path = inquirer.filepath(
            message="Enter the path to input file. Use -g flag to search globally:",
            default=home_path,
            validate=PathValidator(
                is_file=True,
                message="File must exist within the 'dermscan/inputs/' directory.",
            ),
        ).execute()

        return inputs.parse_file(file_path)
    elif input_method == "user input":
        user_input = inquirer.text(
            message="Enter the list of ingredients separated by commas:"
        ).execute()
        return inputs.parse_user_input(user_input)
    elif input_method == "URL":
        url = inquirer.text(message="Enter the URL to fetch the ingredients:").execute()
        click.echo(Fore.CYAN + f"Fetching remote URL data from {url}.")
        scraper = UrlScraper(url)
        click.echo(Fore.GREEN + f"Remote data has been loaded.")

        parser_choice = inquirer.select(
            message="Select which HTML parser to use:",
            choices=[
                Choice(value="llama2", name="Llama 2"),
                Choice(value="llama3", name="Llama 3"),
                Choice(value="default", name="Manual"),
            ],
            default="default",
        ).execute()

        if parser_choice == "default":
            try:
                ingredients = parse_html(scraper.html, scraper.domain)
                return ingredients
            except Exception:
                click.echo(bold_error("Failed to parse ingredients from the URL."))
                return []
        else:
            llm_parser = LLM(parser_choice)
            llm_parser.invoke(scraper.html)

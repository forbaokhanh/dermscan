import click

from dermscan.models.llm import LLM


@click.command("llm")
def llm_command():
    """
    Run the LLM model to generate a list of skincare ingredients from a given text.
    """
    llm = LLM()

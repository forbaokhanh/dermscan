import click

from dermscan.cli.cmd.file_commands import tojson
from dermscan.cli.cmd.input_commands import parse_ingredients
from dermscan.cli.cmd.llm_commands import llm_command
from dermscan.cli.cmd.scan_commands import dermscan_run


# Main entry point for CLI
@click.group()
def cli():
    """Main entry point for CLI."""
    pass


# Add subcommands to the main CLI
cli.add_command(tojson)
cli.add_command(dermscan_run)
cli.add_command(parse_ingredients)
cli.add_command(llm_command)

if __name__ == "__main__":
    cli()

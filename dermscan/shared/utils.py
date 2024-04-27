# Click Print Helper functions #######################
import click


def bold_error(message: str) -> str:
    """Return the message in bold red color."""
    return click.style(message, fg="red", bold=True)


def success(message: str) -> str:
    """Return the message in green color."""
    return click.style("✅ " + message, fg="green", bold=True)


def info(message: str) -> str:
    """Return the message in green color."""
    return click.style(message, fg="green")

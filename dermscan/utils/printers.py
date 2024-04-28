import click

# from rich import Console


def bold_error(message: str) -> str:
    """Return the message in bold red color."""
    return click.style(message, fg="red", bold=True)


def success(message: str) -> str:
    """Return the message in green color."""
    return click.style("✅ " + message, fg="green", bold=True)


def info(message: str) -> str:
    """Return the message in green color."""
    return click.style(message, fg="blue")


# def print_result(alerts: List[Ingredient], warnings: List[Match]) -> None:
#     """
#     Print the results of the scan.
#     TODO - Revisit this function to print the results using the rich library.
#     :param alerts:
#     :param warnings:
#     :return:
#     """
#     console = Console()
#     if not alerts and not warnings:
#         console.print("✅ Product is completely clear!", style="bold green")
#     elif alerts:
#         # sort the alerts in order of comedogenic rating
#         alerts.sort(key=lambda x: x.comedogenicity, reverse=True)
#
#         console.print("🚨 Alerts 🚨", style="bold red")
#         for alert in alerts:
#             console.print(f"- {alert.name} [bold red]{alert.comedogenicity}[/bold red]")
#     elif warnings:
#         warnings.sort(key=lambda x: x.matched_ingredient.comedogenicity, reverse=True)
#
#         console.print("⚠️ Warnings ⚠️")
#         for warning in warnings:
#             # TODO - Print the warning with the comedogenicity rating of the matched ingredient
#             console.print(warning)
#     return

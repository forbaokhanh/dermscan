from typing import List
from urllib.parse import urlparse

from rich import print
from rich.console import Console

from src.script import Ingredient, MatchedIngredient


def ensure_list(var):
    if isinstance(var, list):
        return var
    elif isinstance(var, str):
        return [x.strip().strip(".") for x in var.split(",")]
    else:
        raise TypeError(f"Unsupported type: {type(var)}")


def is_url(string: str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def print_result(alerts: List[Ingredient], warnings: List[MatchedIngredient]) -> None:
    console = Console()
    if not alerts and not warnings:
        console.print("✅ Product is completely clear!", style="bold green")
    elif alerts:
        # sort the alerts in order of comedogenic rating
        alerts.sort(key=lambda x: x.comedogenicity, reverse=True)

        console.print("🚨 Alerts 🚨", style="bold red")
        for alert in alerts:
            console.print(f"- {alert.name} [bold red]{alert.comedogenicity}[/bold red]")
    elif warnings:
        warnings.sort(key=lambda x: x.matched_ingredient.comedogenicity, reverse=True)

        console.print("⚠️ Warnings ⚠️")
        for warning in warnings:
            console.print(warning.format_warning())
    return

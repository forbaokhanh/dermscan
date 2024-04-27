from typing import List

from rich.console import Console

from dermscan.models import Ingredient, Match


def print_result(alerts: List[Ingredient], warnings: List[Match]) -> None:
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

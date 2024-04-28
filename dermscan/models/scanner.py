from typing import List, Callable

import click
from fuzzywuzzy import process

from dermscan.models import Match
from dermscan.utils import success, info
from dermscan.utils.printers import show_error
from dermscan.utils.scorer import custom_scorer


class ReferenceScanner:
    def __init__(
        self,
        references: List[str],
        scorer: Callable[[str, List[str]], int] = custom_scorer,
    ):
        self.references = references
        self.scorer = scorer

    def scan(self, skincare_ingredients: List[str]) -> List[Match]:
        results = []

        for ingredient in skincare_ingredients:
            similarity_score, best_match = process.extractOne(
                ingredient, self.references, scorer=self.scorer
            )
            if similarity_score == 100:
                results.append(Match(ingredient, best_match))
        return results

    def run(self, skincare_ingredients: List[str]) -> None:
        results = self.scan(skincare_ingredients)
        if not results or len(results) == 0:
            click.echo(
                success("No matches found in the database. Your product is safe!")
            )
            return

        show_error("Matches found in the database:")
        for result in results:
            click.echo(info(str(result)))

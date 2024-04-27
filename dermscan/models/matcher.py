from abc import abstractmethod, ABC
from typing import List, Union

import click
from fuzzywuzzy import process

from dermscan.models import Match, Ingredient
from dermscan.models.scorer import custom_scorer
from dermscan.shared import bold_error, success, info


class AbstractIngredientMatcher(ABC):
    def __init__(self, database: List[Union[str, Ingredient]]):
        self.database = database
        self.references = [
            ingredient.name if isinstance(ingredient, Ingredient) else ingredient
            for ingredient in database
        ]

    @abstractmethod
    def search(self, candidates: List[str]) -> List[Match]:
        pass


class StringDatabaseMatcher(AbstractIngredientMatcher):
    def search(self, skincare_ingredients: List[str]) -> List[Match]:
        results = []

        for ingredient in skincare_ingredients:
            similarity_score, best_match = process.extractOne(
                ingredient, self.references, scorer=custom_scorer
            )
            if similarity_score == 100:
                results.append(Match(ingredient, best_match))
        return results

    def report(self, skincare_ingredients: List[str]) -> None:
        results = self.search(skincare_ingredients)
        if not results or len(results) == 0:
            click.echo(
                success("No matches found in the database. Your product is safe!")
            )
            return

        click.echo(bold_error("Matches found in the database:"))
        for result in results:
            click.echo(info(str(result)))


class IngredientDatabaseMatcher(AbstractIngredientMatcher):
    def search(self, candidates: List[str]) -> List[Match]:
        """TODO: Implement this method."""
        return []

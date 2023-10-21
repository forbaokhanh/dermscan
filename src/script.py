from thefuzz import fuzz


class Ingredient:
    def __init__(self, name, comedogenicity, irritancy):
        self.name = name
        self.comedogenicity = comedogenicity
        self.irritancy = irritancy


class MatchedIngredient:
    def __init__(self, name: str, matched_ingredient: Ingredient):
        self.name = name
        self.matched_ingredient = matched_ingredient

    def proximity(self) -> float:
        return fuzz.partial_token_sort_ratio(self.name, self.matched_ingredient.name)

    def format_warning(self):
        return (
            f"- [bold bright_cyan]{self.name}[/bold bright_cyan]\n"
            f"   [i magenta]{self.matched_ingredient.name}[/i magenta] is"
            f" [bold bright_yellow]{self.matched_ingredient.comedogenicity}[/bold bright_yellow]"
        )

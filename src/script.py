from thefuzz import fuzz


class Ingredient:
    def __init__(self, name, comedogenicity, irritancy):
        self.name = name
        self.comedogenicity = comedogenicity
        self.irritancy = irritancy

    def score_symbol(self):
        symbols = {5: "5️⃣", 4: "4️⃣", 3: "3️⃣", 2: "2️⃣", 1: "1️⃣"}
        return symbols[self.comedogenicity]

    def __str__(self):
        return f"{self.name} is a {self.score_symbol()}"

    def __repr__(self):
        return f"""Ingredient(Name: {self.name}, Comedogenicity: {self.comedogenicity}, Irritancy: {self.irritancy})"""


class MatchedIngredient:
    def __init__(self, name: str, matched_ingredient: Ingredient):
        self.name = name
        self.matched_ingredient = matched_ingredient
        self.comedogenicity = matched_ingredient.comedogenicity

    def proximity(self) -> float:
        return fuzz.partial_token_sort_ratio(self.name, self.matched_ingredient.name)

    def __str__(self):
        return (f"{self.name} ({self.proximity()} prox.)\n"
                f"~ {self.matched_ingredient}")

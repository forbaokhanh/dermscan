class Match:
    def __init__(self, ingredient: str, best_match: str):
        self.ingredient = ingredient
        self.best_match = best_match

    def __str__(self):
        return f"[Original] {self.ingredient} -> [Similar] {self.best_match}"

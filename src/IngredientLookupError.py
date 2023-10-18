class IngredientLookupError(LookupError):
    """
    Raised when unable to find the ingredient list on a webpage.
    """
    def __init__(self, source: str, message: str = "Could not find ingredients."):
        full_message = f"{message} Source: {source}"
        super().__init__(full_message)
        self.source = source

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import pyperclip
from thefuzz import fuzz, process

from src.script import Ingredient, MatchedIngredient
from src.url_parser import fetch_ingredients_from_url
from src.utils import ensure_list, is_url, print_result

DATA_FOLDER = Path(__file__).parent.parent / "data"
CSV_FILEPATH = str(DATA_FOLDER / "product_info.csv")


def parse_input() -> List[str]:
    """
    Defines all possible input to comparison logic.
    Currently, we assume either a URL or ingredient contents were present
    in the clipboard.

    :return: list of ingredients relevant to the product under question.
    Normalize all ingredient entries to be lower case.
    """
    contents = pyperclip.paste()

    list_raw = ensure_list(contents)
    if is_url(contents):
        list_raw = fetch_ingredients_from_url(contents)
    return [x.lower() for x in list_raw]


def load_cache(filepath: str) -> Dict[str, Ingredient]:
    """
    Load ingredient data from a CSV file into a dictionary.

    This function reads a CSV file specified by `filepath` and populates a
    dictionary where the keys are ingredient names and the values are
    `Ingredient` objects. The function assumes that all ingredient
    names in the file are unique; if not, an assertion error will be raised.

    Parameters:
    -----------
    filepath : str
        The file path to the CSV file containing ingredient data.

    Returns:
    --------
    Dict[str, Ingredient]
        A dictionary containing ingredient names as keys and `Ingredient` objects as values.

    Raises:
    -------
    AssertionError
        If duplicate ingredient names are found in the CSV file.

    Example:
    --------
    >>> load_cache("ingredient_data.csv")
    {'Water': <Ingredient object>, ...}
    """
    df = pd.read_csv(filepath, sep=",")
    ingredients = {}

    for index, row in df.iterrows():
        ingredient = Ingredient(row["Name"], int(row["Comedogenicity"]), int(row["Irritancy"]))
        assert ingredient.name not in ingredients
        ingredients[ingredient.name] = ingredient
    return ingredients


def compare(
    ingredients: List[str], reference: Dict[str, Ingredient]
) -> Tuple[List[Ingredient], List[MatchedIngredient]]:
    reference_names = reference.keys()
    alert_worthy = []
    warning_worthy = []

    for entry in ingredients[: len(ingredients) // 2]:
        entry = entry.title()
        match, similarity = process.extractOne(
            entry, reference_names, scorer=fuzz.partial_token_sort_ratio
        )
        matched_ingredient = reference[match]
        comedogenicity = reference[match].comedogenicity

        # Condition for 100% similarity
        if similarity == 100:
            if comedogenicity >= 4:
                alert_worthy.append(matched_ingredient)
            elif comedogenicity == 3:
                warning_worthy.append(MatchedIngredient(entry, matched_ingredient))

        # Condition for similarity between 80 and 100 and high comedogenicity
        elif 80 < similarity < 100 and comedogenicity >= 3:
            warning_worthy.append(MatchedIngredient(entry, matched_ingredient))

    return alert_worthy, warning_worthy


if __name__ == "__main__":
    product_ingredients = parse_input()

    comedogenic_references = load_cache(CSV_FILEPATH)

    alerts, warnings = compare(product_ingredients, comedogenic_references)
    print_result(alerts, warnings)

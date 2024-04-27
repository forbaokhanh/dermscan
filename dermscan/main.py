import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pyperclip
from thefuzz import fuzz, process

from dermscan.url_parser import fetch_ingredients_from_url
from dermscan.utils import ensure_list, is_url, print_result

if getattr(sys, "frozen", False):
    # Running as compiled
    BASE_DIR = Path(sys._MEIPASS)
    # sys._MEIPASS -> Attribute set by PyInstaller when your application is bundled into a single executable.
    # It provides the path to a temporary folder that PyInstaller creates to store your script and all its dependencies.
else:
    # Running as script,
    # Assuming this file is under dermscan/main.py and the datafiles are under data/*.csv
    BASE_DIR = Path(__file__).parent.parent

DATA_FOLDER = BASE_DIR / "data"
CSV_FILEPATH = str(DATA_FOLDER / "detailed.csv")


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


def compare(
    ingredients: List[str], reference: Dict[str, Ingredient]
) -> Tuple[List[Ingredient], List[MatchedIngredient]]:
    """
    Compare the list of ingredients to the reference data.
    :param ingredients:
    :param reference:
    :return:
    """
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

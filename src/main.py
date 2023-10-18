from typing import List
import difflib
import os

import pyperclip

from src.url_parser import fetch_ingredients_from_url
from src.utils import is_url, ensure_list

INGREDIENTS_TO_CHECK_FILE_NAME = "../check.txt"


# def get_ingredients_from_text_file() -> List[str]:
#     with open(INGREDIENTS_TO_CHECK_FILE_NAME) as f:
#         ingredients = f.readlines()
#
#     return [x.strip().lower() for x in ingredients[0].split(',')]
#

def load_bad_ingredients() -> List[str]:
    """
    Locates on disk and loads a list of known comedogenic ingredients.
    The current reference file is called 'list_bad.txt' and it's placed in the root folder.
    The contents of that file are organized in a new line.

    :return: list of ingredients that are known to be comedogenic in lowercase.
    """
    file_path = os.path.join(os.getcwd(), 'list_bad.txt')
    with open(file_path) as f:
        bad_ingredients = f.readlines()
    return [x.strip().lower() for x in bad_ingredients]


def compare(ingredients: List[str], reference: List[str]) -> None:
    """
    Compares a list of ingredients against a list of comedogenic data to find close matches.

    The function iterates over each ingredient in the `ingredients` list and searches for close matches
    within the `reference` list using difflib's get_close_matches function. If a close match is found,
    the ingredient, its index in the list, and the close match are printed to the console.

    Parameters:
    - ingredients (List[str]): A list of ingredient names to compare.
    - reference (List[str]): A list of comedogenic data against which to compare the ingredients.

    Returns:
    - None: The function prints the matching data to the console and returns None.

    Example:
    >>> compare(['Acetone', 'Almond oil'], ['Acetone (0)*', 'Almond oil (1-2)*'])
    Acetone | 0 out of 2 ingredient
    ['Acetone (0)*']

    Almond oil | 1 out of 2 ingredient
    ['Almond oil (1-2)*']
    """
    n = len(ingredients)
    for index, ingredient in enumerate(ingredients):
        close_options = difflib.get_close_matches(ingredient, reference, n=1, cutoff=0.8)
        if len(close_options) > 0:
            print('{ingredient} | {index} out of {total} ingredient'.format(ingredient=ingredient.capitalize(),
                                                                            index=index, total=n))
            print('{close_options}\n'.format(close_options=close_options))
    return


def parse_input() -> List[str]:
    contents = pyperclip.paste()
    if is_url(contents):
        return fetch_ingredients_from_url(contents)
    return ensure_list(contents)


if __name__ == '__main__':
    comedogenic_data = load_bad_ingredients()
    product_ingredients = parse_input()

    compare(product_ingredients, comedogenic_data)

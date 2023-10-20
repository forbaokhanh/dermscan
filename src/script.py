from typing import Tuple, Dict
from rich import pretty, print
import pandas as pd
import re


class Ingredient:
    def __init__(self, name):
        self.name = name
        self.rating_info = {}

    def set_rating(self, rating, concentration: float = 1.0):
        self.rating_info[concentration] = rating

    def get_rating(self, concentration: float = 1.0):
        return self.rating_info[concentration]

    def __repr__(self):
        return f"""Ingredient(Name: {self.name}, Ratings: {self.rating_info})"""


def parse_concentration(input_str: str) -> Tuple[str, float]:
    # Use regex to find the postfix that matches the pattern (10%)
    match = re.search(r'\((\d+)%\)$', input_str)
    if match:
        # Extract the percentage value and convert it to a float
        percentage = float(match.group(1)) / 100

        # Extract the prefix by removing the postfix from the input string
        prefix = input_str[:match.start()].strip()

        return prefix, percentage
    return input_str.strip(), 1.0


def parse_rating(input_str: str) -> int:
    """
    Hacky solution.
    :param input_str: a string formatted like (1) or (0-5)
    :return: the rating approximation integer, in case of presented range, take the maximum
    """
    return int(input_str[-2])


def parse_entry(entry: str) -> Ingredient:
    # Use regex to find the postfix that matches the pattern (1) or (0-5).
    # The digits are always within the range 0-5 (inclusive), and the format allows either:
    # - A single digit (e.g., (1))
    # - Two digits separated by a single dash (e.g., (3-4))
    match = re.search(r'\((\d-?\d?)\)$', entry)

    if match:
        postfix = match.group(0)  # The whole match including the parenthesis
        rating = parse_rating(postfix)

        # Remove the postfix from the original entry to get the first part
        first_part = entry.replace(postfix, '').strip()

        # Handle cases for elements that present with different concentrations
        first_part, concentration = parse_concentration(first_part)

        ingredient = Ingredient(first_part)
        ingredient.set_rating(rating, concentration)
        return ingredient

    else:
        raise Exception(f"Couldn't find a valid postfix, missing comedogenic rating info for {entry}")


def process_raw_csv_file(filepath: str) -> Dict[str, Ingredient]:
    df = pd.read_csv(filepath, sep=",")

    ingredients = {}

    # Iterating over each cell
    for index, row in df.iterrows():
        for col in df.columns:
            cell_value = row[col]
            if isinstance(cell_value, str):
                ingredient = parse_entry(cell_value)
                ingredients[ingredient.name] = ingredient
    return ingredients


if __name__ == "__main__":
    pretty.install()

    # Define the path to the CSV file
    file_path = "./data/stuff.csv"
    cache = process_raw_csv_file(file_path)
    print(cache)

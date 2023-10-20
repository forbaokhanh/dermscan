from typing import Tuple, Optional
import pandas as pd
import re
import math

# Define the path to the CSV file
file_path = "./data/stuff.csv"


def parse_entry(entry: str) -> Tuple[int, str]:
    """
    Parse an entry string to extract the name and the maximum rating value.

    Parameters:
    - entry (str): The entry string to parse. Should be in the format 'Name (Rating)'.
      Special characters like '*' and '^' are ignored. Rating can be a single integer or a range (e.g., 0-2).

    Returns:
    - Tuple[int, str]: A tuple containing two elements:
        1. The maximum rating as an integer. If the rating is a range (e.g., 0-2), the maximum value is returned.
        2. The name as a sanitized string, with leading and trailing whitespaces removed.

    Raises:
    - Exception: If the entry string doesn't match the expected format, an exception is raised with a descriptive message.

    Example:
    >>> parse_entry("John Doe (2-5)")
    (5, "John Doe")

    >>> parse_entry("Jane^ Doe* (3)")
    (3, "Jane Doe")

    >>> parse_entry("Invalid Entry")
    Exception: Couldn't parse entry Invalid Entry
    """
    # Skip if entry is None or nan
    if entry is None or (isinstance(entry, float) and math.isnan(entry)):
        return None, None

    if not isinstance(entry, str):
        raise Exception(f"Expected a string or bytes-like object. Got {type(entry)}")

    # Remove characters like '*', '^' from the entry
    sanitized_entry = re.sub(r"[\*\^]", "", entry)

    # Extract name and rating using regular expression
    match = re.match(r"^(.+)\s?\(([0-9\-]+)\)$", sanitized_entry)

    if match:
        name, rating = match.groups()

        # Check if rating has a range (e.g., 0-2)
        if "-" in rating:
            min_rating, max_rating = map(int, rating.split("-"))
            max_rating = max(min_rating, max_rating)  # Choose the maximum value
        else:
            max_rating = int(rating)

        return max_rating, name.strip()

    else:
        raise Exception("Couldn't parse entry {}".format(entry))


if __name__ == "__main__":
    # Read the CSV file into a Pandas DataFrame
    try:
        df = pd.read_csv(file_path, sep=",")
        db = {}

        # Iterating over each cell
        for index, row in df.iterrows():
            for col in df.columns:
                cell_value = row[col]
                rating, name = parse_entry(cell_value)
                if rating is None:
                    continue
                if rating not in db:
                    db[rating] = []
                db[rating].append(name)

        print(db)

    except FileNotFoundError:
        print(f"File not found at {file_path}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    # Display the first few rows of the DataFrame
    print(df.head())
    print(df.info())

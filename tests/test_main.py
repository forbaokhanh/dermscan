from pathlib import Path

import pyperclip
import pytest

from dermscan.main import CSV_FILEPATH, compare, load_cache, parse_input
from dermscan.utils import print_result


@pytest.fixture
def comedogenic_references():
    return load_cache(CSV_FILEPATH)


def test_empty(comedogenic_references):
    ingredients = [""]
    compare(ingredients, comedogenic_references)


def test_present(comedogenic_references):
    olaplex_filepath = Path(__file__).parent / "test_data" / "olaplex.txt"

    with open(olaplex_filepath, "r") as file:
        contents = file.readline()
        pyperclip.copy(contents)

    ingredients = parse_input()
    alerts, warnings = compare(ingredients, comedogenic_references)
    print_result(alerts, warnings)

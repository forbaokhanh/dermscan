from typing import List
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from collections import deque
from difflib import Differ, SequenceMatcher
import difflib
import requests
import json

BAD_INGREDIENT_FILE_NAME = "list_bad.txt"
INGREDIENTS_TO_CHECK_FILE_NAME = "check.txt"
SEARCH_KEY = "ingredientDesc"


def check_ingredients(url: str=None) -> None:
    bad_ingredients = load_bad_ingredients()
    if not url:
        ingredients = get_ingredients_from_text_file()
    else:
        ingredients = get_ingredients_from_url(url)
    n = len(ingredients)
    for index, ingredient in enumerate(ingredients):
        close_options = difflib.get_close_matches(ingredient, bad_ingredients, n=1, cutoff=0.8)
        if len(close_options) > 0:
            print('{ingredient} | {index} out of {total} ingredient'.format(ingredient=ingredient.capitalize(), index=index, total=n))
            print('{close_options}\n'.format(close_options=close_options))
    return


def get_ingredients_from_url(url: str) -> List[str]:
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36 "
    }
    try:
        session = HTMLSession()
        response = session.get(url, headers=headers)
        print("Received a {} status code.".format(response.status_code))
        soup = BeautifulSoup(response.text, "html.parser")
        script = soup.find("script", id="linkStore")
        search_graph = json.loads(script.getText())
        return bfs_for_ingredients(search_graph)
    except requests.exceptions.RequestException as e:
        print(e)


def bfs_for_ingredients(graph: {}) -> List[str]:
    queue = deque([graph])
    while queue:
        # only put maps in the queue
        obj = queue.popleft()
        for key, value in obj.items():
            if key == SEARCH_KEY:
                return cleanup_ingredients(value)
            if isinstance(value, dict):
                queue.append(value)
            elif isinstance(value, list):
                for item in obj:
                    if isinstance(item, dict):
                        queue.append(value)
    raise Exception("not able to find ingredients")


def cleanup_ingredients(text: str) -> List[str]:
    return [x.strip().lower() for x in text.split("<br>")[0].replace('/', ',').split(',')]


def get_ingredients_from_text_file() -> List[str]:
    with open(INGREDIENTS_TO_CHECK_FILE_NAME) as f:
        ingredients = f.readlines()

    return [x.strip().lower() for x in ingredients[0].split(',')]


def load_bad_ingredients() -> List[str]:
    with open(BAD_INGREDIENT_FILE_NAME) as f:
        bad_ingredients = f.readlines()
    return [x.strip().lower() for x in bad_ingredients]


if __name__ == '__main__':
    from_url = input("Do you want to supply a URL? (y/n): ")
    if from_url.lower() in ("y", "yes"):
        url = input("Please enter the url: ")

    check_ingredients(url)

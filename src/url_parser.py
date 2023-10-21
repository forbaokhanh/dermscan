# Standard library imports
from time import sleep
from typing import List

import requests
# Third-party imports
from bs4 import BeautifulSoup

# Local application imports
from src.IngredientLookupError import IngredientLookupError


def make_request_with_retries(
    url: str, timeout: int = 5, retries: int = 2, backoff_factor: float = 0.3
) -> str:
    """
    Makes an HTTP GET request with retries and backoff.

    Parameters:
    - url (str): The URL to fetch.
    - timeout (int): The maximum seconds to wait for a URL fetch.
    - retries (int): Number of retries. Set to 1 for at least one call.
    - backoff_factor (float): Sleep time factor for exponential backoff.

    Returns:
    - str: HTML content.
    """
    exceptions = []
    for i in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            exceptions.append(e)

        sleep(backoff_factor * (2**i))

    raise Exception(
        f"Failed to retrieve URL after {retries} retries with {timeout} timeout. Exceptions: {exceptions}"
    )


def parse_ingredients(ingredients_str: str) -> List[str]:
    """
    Parse a comma-separated string of ingredients into a list.

    Parameters:
    - ingredients_str (str): Comma-separated ingredients.

    Returns:
    - List[str]: List of ingredients.
    """
    return [x.strip() for x in ingredients_str.split(",")]


def scrape_sephora(html: str) -> List[str]:
    """
    Scrape the ingredients from Sephora product HTML.

    Parameters:
    - html (str): The HTML content of the Sephora product page.

    Returns:
    - List[str]: List of ingredients if found, otherwise None.
    """
    soup = BeautifulSoup(html, "html.parser")
    ingredients_div = soup.find("div", {"id": "ingredients"})

    if ingredients_div:
        raw_text = ingredients_div.text.strip()
        # Splitting the text by <br><br> to get paragraphs
        paragraphs = raw_text.split("<br><br>")

        # Take the last paragraph if more than one, otherwise take the single paragraph
        relevant_paragraph = paragraphs[-1] if len(paragraphs) > 1 else paragraphs[0]

        # Converting this to an array of strings, separated by commas
        ingredients_array = relevant_paragraph.split(", ")
        return ingredients_array
    return []


def scrape_ulta(html_content: str) -> list[str]:
    """
    Scrape the ingredient list from an Ulta product page.

    Parameters:
    - html_content (str): HTML content of the Ulta product page.

    Returns:
    - list[str]: List of ingredients, each as a separate string.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    ingredients_section = soup.find("details", {"aria-controls": "Ingredients"})

    if ingredients_section:
        p_tag = ingredients_section.find("p")
        if p_tag:
            ingredients_text = p_tag.get_text()
            return [i.strip() for i in ingredients_text.split(",") if i.strip()]

    return []


def scrape_amazon(html: str) -> List[str]:
    """
    Scrape Amazon's HTML for ingredients.

    Parameters:
    - html (str): HTML content of the page.

    Returns:
    - List[str]: List of ingredients.
    """
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("div", {"class": "a-section content"})
    if section:
        p_tags = section.find_all("p")
        for p in p_tags:
            if "Active Ingredients:" in p.text or "Inactive Ingredients:" in p.text:
                # Extract text and clean it
                ingredients_text = p.text.replace("Active Ingredients:", "").replace(
                    "Inactive Ingredients:", ""
                )
                return parse_ingredients(ingredients_text)
    return []


def generic_scrape(html: str) -> List[str]:
    """
    Fallback scraper for HTML of unknown sites.

    Parameters:
    - html (str): HTML content of the page.

    Returns:
    - List[str]: List of ingredients.
    """
    likely_keywords = ["ingredients:", "contains:", "ingredient list:"]
    soup = BeautifulSoup(html, "html.parser")

    for tag in ["p", "div", "li", "span"]:
        for elem in soup.find_all(tag):
            if any(keyword in elem.text.lower() for keyword in likely_keywords):
                return parse_ingredients(elem.text)
    return []


def fetch_ingredients_from_url(url: str) -> list[str]:
    """
    Fetch the list of ingredients from a given URL of Sephora, Ulta, or Amazon.
    Raises IngredientLookupError if ingredients are not found.

    Parameters:
    - url (str): The URL of the product.

    Returns:
    - list[str]: List of ingredients.
    """
    html = make_request_with_retries(url, retries=1)

    if "sephora.com" in url:
        source = "Sephora"
        ingredients = scrape_sephora(html)
    elif "ulta.com" in url:
        source = "Ulta"
        ingredients = scrape_ulta(html)
    elif "amazon.com" in url:
        source = "Amazon"
        ingredients = scrape_amazon(html)
    else:
        source = "Generic"
        ingredients = generic_scrape(html)

    if not ingredients:
        raise IngredientLookupError(source, f"Could not find ingredients on {source}.")

    return ingredients

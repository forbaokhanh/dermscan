from typing import List

from bs4 import BeautifulSoup

from dermscan.utils import inputs


def parse_html(html: str, domain: str) -> List[str]:
    """
    Parse the HTML content of a page to extract ingredients.

    Parameters:
    - html (str): The HTML content of the page.
    - domain (str): The domain of the page.

    Returns:
    - List[str]: List of ingredients.
    """
    if "sephora" in domain:
        return parse_sephora(html)
    elif "ulta" in domain:
        return parse_ulta(html)
    elif "amazon" in domain:
        return parse_amazon(html)
    else:
        return generic_parse(html)


def parse_sephora(html: str) -> List[str]:
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
        ingredients_array = inputs.parse_string(relevant_paragraph)
        return ingredients_array
    raise ValueError("No ingredients found on the Sephora page.")


def parse_ulta(html_content: str) -> List[str]:
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
            return inputs.parse_string(ingredients_text)

    raise ValueError("No ingredients found on the Ulta page.")


def parse_amazon(html: str) -> List[str]:
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
                return inputs.parse_string(ingredients_text)
    raise ValueError("No ingredients found on the Amazon page.")


def generic_parse(html: str) -> List[str]:
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
                return inputs.parse_string(elem.text)
    raise ValueError("No ingredients found on the page.")

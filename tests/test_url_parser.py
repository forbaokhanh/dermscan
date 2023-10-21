import pytest

from src.url_parser import IngredientLookupError, fetch_ingredients_from_url

# Define URLs for Sephora, Ulta, and Amazon products that are known to have ingredients
SEPHORA_URL = "https://www.sephora.com/product/euk-134-0-1-P442833?skuId=2210656"  # Replace with an actual URL
ULTA_URL = "https://www.ulta.com/p/brilliant-gloss-glass-hair-anti-frizz-serum-pimprod2034432?sku=2600787"  # Replace with an actual URL
AMAZON_URL = "https://www.amazon.com/dp/B002ZNJYRA/ref=sspa_dk_offsite_brave_1?aaxitk=9c33c153d99a33b717c46eeaa875335e&th=1"  # Replace with an actual URL
GENERIC_URL = "https://helloseen.com/products/seen-shampoo?variant=40416510672979"  # Replace with an actual URL


def test_fetch_ingredients_from_sephora_url():
    print("here")
    # ingredients = fetch_ingredients_from_url(SEPHORA_URL)
    try:
        ingredients = fetch_ingredients_from_url(SEPHORA_URL)
        assert ingredients  # Check if the list is non-empty
        assert isinstance(ingredients, list)
    except IngredientLookupError:
        pytest.fail("IngredientLookupError raised")


def test_fetch_ingredients_from_ulta_url():
    try:
        ingredients = fetch_ingredients_from_url(ULTA_URL)
        assert ingredients  # Check if the list is non-empty
        assert isinstance(ingredients, list)
    except IngredientLookupError:
        pytest.fail("IngredientLookupError raised")


def test_fetch_ingredients_from_amazon_url():
    try:
        ingredients = fetch_ingredients_from_url(AMAZON_URL)
        assert ingredients  # Check if the list is non-empty
        assert isinstance(ingredients, list)
    except IngredientLookupError:
        pytest.fail("IngredientLookupError raised")


# def test_fetch_ingredients_from_generic_url():
#     try:
#         ingredients = fetch_ingredients_from_url(GENERIC_URL)
#         assert ingredients  # Check if the list is non-empty
#         assert isinstance(ingredients, list)
#     except IngredientLookupError:
#         pytest.fail("IngredientLookupError raised")


def test_fetch_ingredients_from_invalid_url():
    with pytest.raises(IngredientLookupError):
        fetch_ingredients_from_url("https://www.nonexistent.com")

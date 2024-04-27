from typing import List, Dict, Tuple
from fuzzywuzzy import fuzz, process

from dermscan.models import Ingredient


def search_lists(
    candidates: List[str],
    database: List[str]
):
    """
    Compare the list of candidate ingredients to the reference data.
    All inputs have been normalized to lower case.
    First, compare on token sort ratio, then on partial token sort ratio.

    :param candidates: List of candidate ingredient names
    :param database: List of reference ingredient names
    :return: List of tuples containing the candidate, the best match from the database, and the partial token sort ratio score
    """
    results = []
    threshold_token_sort = 80  # Define a threshold for the token sort ratio
    threshold_partial_token_sort = 90  # Define a higher threshold for the partial token sort ratio

    for candidate in candidates:
        # First pass: using token sort ratio
        # Find the best match using token sort ratio
        best_match, best_token_sort_score = process.extractOne(candidate, database, scorer=fuzz.token_sort_ratio)

        # Proceed only if the score from the first pass is above the threshold
        if best_token_sort_score >= threshold_token_sort:
            # Second pass: using partial token sort ratio
            # Calculate the partial token sort ratio with the best match from the first pass
            partial_token_sort_score = fuzz.partial_token_sort_ratio(candidate, best_match)

            # Only accept matches that meet the second threshold
            if partial_token_sort_score >= threshold_partial_token_sort:
                # Append the candidate, the best match, and the partial token sort ratio score to results
                results.append((candidate, best_match, partial_token_sort_score))

    return results


def search_data(
    candidates: List[str],
    reference: Dict[str, Ingredient]
) -> Tuple[List[Ingredient], List[MatchedIngredient]]:
    """
    Compare the list of ingredients to the reference data.
    :param candidates: list of ingredients to compare. Typically belonging to a product.
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
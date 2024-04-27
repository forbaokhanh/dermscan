# Define the custom scorer function
from fuzzywuzzy import fuzz


def custom_scorer(query, choices):
    """
    Custom scorer function to calculate similarity scores using different ratios.
    We will use this function to find the best match for a given query in a list of choices.

    :param query: str, the query string to find the best match for
    :param choices: list of str, the list of choices to search for the best match
    :return: int, str, the similarity score and the best match found
    """
    for choice in choices:
        # Calculate similarity scores using different ratios
        ratio_score = fuzz.ratio(query.lower(), choice.lower())
        if ratio_score == 100:
            return 100

        partial_ratio_score = fuzz.partial_ratio(query.lower(), choice.lower())
        if partial_ratio_score == 100:
            return 100

        token_sort_ratio_score = fuzz.token_sort_ratio(query.lower(), choice.lower())
        if token_sort_ratio_score == 100:
            return 100

        partial_token_sort_ratio_score = fuzz.partial_token_sort_ratio(
            query.lower(), choice.lower()
        )
        if partial_token_sort_ratio_score == 100:
            return 100

        token_set_ratio_score = fuzz.token_set_ratio(query.lower(), choice.lower())
        if token_set_ratio_score == 100:
            return 100

    # If no perfect match is found, return 0
    return 0

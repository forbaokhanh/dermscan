import logging
from time import sleep
from urllib.parse import urlparse

import requests
from colorama import init, Fore
from tqdm import tqdm


class UrlScraper:
    def __init__(self, url, retries=3, backoff_factor=0.3, timeout=5):
        init(autoreset=True)
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.html = self.make_request_with_retries(
            retries=retries, backoff_factor=backoff_factor, timeout=timeout
        )
        self.domain = self._extract_base_domain()

    def make_request_with_retries(
        self, timeout: int = 5, retries: int = 3, backoff_factor: float = 0.3
    ) -> str:
        """
        Makes an HTTP GET request with retries and exponential backoff.

        Parameters:
        - url (str): The URL to fetch.
        - timeout (int): The maximum seconds to wait for a URL fetch.
        - retries (int): Number of retries for the request.
        - backoff_factor (float): Multiplier for exponential backoff.

        Returns:
        - str: HTML content of the page.

        Raises:
        - requests.RequestException: If the request fails after retries.
        """
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        with tqdm(
            total=retries,
            desc="Fetching URL",
            bar_format="{l_bar}{bar}{r_bar}",
            colour="blue",
        ) as pbar:
            for attempt in range(retries):
                try:
                    response = session.get(self.url, timeout=timeout)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    print(
                        Fore.YELLOW
                        + f"Successfully fetched data on attempt {attempt+1}"
                    )
                    return response.text
                except requests.RequestException as e:
                    wait_time = backoff_factor * (2**attempt)
                    self.logger.warning(
                        Fore.RED
                        + f"Request failed: {e}. Retrying in {wait_time:.2f} seconds..."
                    )
                    sleep(wait_time)
                    pbar.update(1)  # Update the progress bar per attempt
            session.close()
            raise requests.RequestException(
                Fore.RED + f"Failed to retrieve URL after {retries} attempts."
            )

    def _extract_base_domain(self) -> str:
        """
        Extract the base domain from a URL, stripping away any subdomains.

        Args:
        url (str): The URL from which to extract the base domain.

        Returns:
        str: The base domain of the URL.
        """
        domain = urlparse(self.url).netloc
        parts = domain.split(".")
        # Ensure we capture top-level domains like '.co.uk'
        if len(parts) > 2 and len(parts[-2]) <= 3:
            base_domain = ".".join(parts[-3:])
        else:
            base_domain = ".".join(parts[-2:])
        return base_domain

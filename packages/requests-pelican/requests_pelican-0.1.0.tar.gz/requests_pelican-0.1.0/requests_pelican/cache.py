"""Response caching.
"""

import requests_cache
from urllib3.util import parse_url

from .config import (
    PELICAN_CONFIGURATION_PATH,
)

PATHS_TO_CACHE = {
    PELICAN_CONFIGURATION_PATH,
}


def response_cache_filter(response):
    """Returns `True` if a response should be cached.

    This only caches responses from Pelican configuration endpoints.
    """
    print(response.url)
    url = parse_url(response.url)
    print(url.path)
    print(url.path in PATHS_TO_CACHE)
    return url.path in PATHS_TO_CACHE


requests_cache.install_cache(
    cache_name="requests-pelican-cache",
    backend="memory",
    filter_fn=response_cache_filter,
)

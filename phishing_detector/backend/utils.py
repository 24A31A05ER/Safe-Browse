import numpy as np
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    return np.array([
        len(url),                              # URL length
        1 if parsed.scheme == "https" else 0,  # HTTPS
        url.count("."),                        # dots
        url.count("-"),                        # hyphen count
        url.count("@"),                        # @ symbol
        1 if "login" in url else 0,
        1 if "bank" in url else 0,
        1 if "verify" in url else 0
    ]).reshape(1, -1)
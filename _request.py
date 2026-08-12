from time import perf_counter

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from payload import SEARCH_URL, FORM_URL

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
session.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=10))

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def fetch_details_consultation(url):
    start = perf_counter()
    response = session.get(url, headers={"User-Agent": USER_AGENT})
    end = perf_counter()
    print(f"Sent details consultation GET request: {end - start}")
    return response


def post_search(data, label):
    start = perf_counter()
    response = session.post(
        SEARCH_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        data=data,
    )
    end = perf_counter()
    print(f"Sent consultations POST request [{label}]: {end - start}")
    return response


def open_search_form():
    start = perf_counter()
    response = session.get(FORM_URL, headers={"User-Agent": USER_AGENT})
    end = perf_counter()
    print(f"Sent search form GET request: {end - start}")
    return response

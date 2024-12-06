import re

import json

from os import environ

BASE_URL = environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
API_KEY = "Token123"
MODEL_ID = "nexus-tool-use-20240816"


def convert_exception_str_to_regex(s: str) -> None:
    """
    Convenience utility for exception tests.
    """
    print(s)
    json.dump(re.escape(s), open("temp.json", "w"))

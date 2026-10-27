import re


def parse_number(value: str) -> float:
    return float(re.sub(r"\s+", "", value.replace(",", ".")))

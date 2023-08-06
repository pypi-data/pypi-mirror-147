"""Divide numbers."""
from typing import Union


def divide(x: Union[int, float], y: Union[int, float]) -> float:
    """Return x*y."""
    return float(x)/float(y)


if __name__ == "__main__":
    print(divide(1, 2))

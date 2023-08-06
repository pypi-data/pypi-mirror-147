"""Multiply numbers."""
from typing import Union


def multiply(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """Return x*y."""
    return x*y


if __name__ == "__main__":
    print(multiply(1, 2))

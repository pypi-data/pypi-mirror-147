"""Substract numbers."""
from typing import Union


def subtract(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """Return x-y."""
    return x-y


if __name__ == "__main__":
    print(subtract(1, 2))

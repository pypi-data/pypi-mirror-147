from algebrapackrpe.add import add
from algebrapackrpe.subtract import subtract
from algebrapackrpe import extras


if __name__ == "__main__":
    print(add(1, 2))
    print(subtract(1, 2))
    print(extras.multiply(1, 2))
    print(extras.divide(1, 2))

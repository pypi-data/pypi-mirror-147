class Wip():
    def print_it(self) -> None:
        print("itsa me mario")


def wet() -> None:
    print("beep boop")


def wat() -> None:
    "WEEE"
    print("testing, 1, 2, 3")


def wut(text: str, woop: bool = False) -> None:
    """ Super docstring test

    Args:
        text (str): The text to print
        woop (boolean, optional): Default false
    """
    print(text)
    print(woop)


def _hidden() -> None:
    print("secret")

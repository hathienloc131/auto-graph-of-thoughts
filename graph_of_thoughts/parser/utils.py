from typing import Dict, List


def string_to_list(string: str) -> List[int]:
    """
    Helper function to convert a list encoded inside a string into a Python
    list object of string elements.

    `Input`:

    - string: `<str>` Input string containing a list.

    `Output`:
    - `<List[str]>`: List of string elements.

    `Raises`:
    - `AssertionError`: If input string does not contain a list.
    """

    assert string[0] == "[" and string[-1] == "]", "String is not a list."
    return [int(num) for num in string[1:-1].split(",")]



"""
    Some function for improve or test whether the final solution matches ground truth.
"""
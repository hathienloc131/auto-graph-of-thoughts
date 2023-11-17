from __future__ import annotations
import logging
from typing import Iterator, Dict, Optional
import itertools

class Thought:
    """
    Represents an LLM thought with its state, constructed by the parser, and various flags.
    """

    _ids: Iterator[int] = itertools.count(0)

    def __init__(self) -> None:
        pass

from __future__ import annotations
import logging
from typing import Iterator, Dict, Optional
from typing_extensions import Self
import itertools


class Thought:
    """
    Represents an LLM thought with its state, constructed by the parser, and various flags.
    """

    _ids: Iterator[int] = itertools.count(0)

    def __init__(self, state: Optional[Dict] = None) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self.id: int = next(Thought._ids)
        self.state: Dict = state

        self._score: float = 0.0
        self._valid: bool = False
        self._solved: bool = False
        self.scored: bool = False
        self.validated: bool = False
        self.compared_to_ground_truth: bool = False

    @staticmethod
    def from_thought(thought: Self) -> Self:
        """
        Creates a new thought from an existing one.
        
        `Input`:

        - thought: `<Thought>` An instance of a Thought to clone.
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<Thought>`: A new Thought instance with properties copied from the input thought.
        """
        new_thought = Thought(thought.state)
        new_thought.score = thought.score
        new_thought.valid = thought.valid
        new_thought.solved = thought.solved
        new_thought.scored = thought.scored
        new_thought.validated = thought.validated
        new_thought.compared_to_ground_truth = thought.compared_to_ground_truth
        return new_thought

    @property
    def valid(self) -> bool:
        return self._valid

    @valid.setter
    def valid(self, valid: bool) -> None:
        self.validated = True
        self._valid = valid

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, new_score: float) -> None:
        self.scored = True
        self._score = new_score

    @property
    def solved(self) -> bool:
        return self._solved

    @solved.setter
    def solved(self, solved: bool) -> None:
        self.compared_to_ground_truth = True
        self._solved = solved
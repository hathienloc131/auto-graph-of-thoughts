from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


class Judge(ABC):
    """
    Abstract base class that defines the interface for all prompters.
    Prompters are used to generate the prompts for the language models.
    """

    @abstractmethod
    def ranking(self, score_prompt, current_task, attempts, num_choices = 1) -> tuple[str, str]:
        """
        Ranking the attempt answers of current task
        """
        pass
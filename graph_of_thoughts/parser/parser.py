from abc import ABC, abstractmethod
from typing import Dict, List, Union
import logging

from . import utils


class Parser(ABC):
    """
    Abstract base class that defines the interface for all parsers.
    Parsers are used to parse the responses from the language models.
    """
    
    def parse_split_answer(self, split_config: Dict, state: Dict, texts: List[str]) -> List[Dict]:
        """
        Parse the response from the language model for a split prompt.
        
        `Input`:

        - split_config: `<Dict>` The Split Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<List[Dict]>`: List of states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        pass


    def parse_generate_answer(self, gen_config: Dict, state: Dict, texts: List[str]) -> List[Dict]:
        """
        Parse the response from the language model for a generation prompt.
        
        `Input`:

        - gen_config: `<Dict>` The Generation Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<List[Dict]>`: List of states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        pass


    def parse_aggregate_answer(self, agg_config: Dict, states: List[Dict], texts: List[str]) -> Union[Dict, List[Dict]]:
        """
        Parse the response from the language model for a aggregation prompt.
        
        `Input`:

        - agg_config: `<Dict>` The Aggregate Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<Union[Dict, List[Dict]]>`: states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        pass
        

    def parse_improve_answer(self, state: Dict, texts: List[str]) -> Dict:
        pass
    


from typing import Dict, List
from graph_of_thoughts.thoughts import OperationType, Operation, Split, Generate, Improve, Aggregate
from .tokenizer import Tokenizer

class Drawer():
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer :Tokenizer = tokenizer


    def decode(self, sequence: List[int])->List[Operation]:
        list_operation = []

        #pop start and end token
        sequence.pop(0)
        sequence.pop(-1)

        for token in sequence:
            list_operation.append(self._idx2operation(token))

        return list_operation


    def _idx2operation(self, token: int) -> Operation:
        operation_info = self.tokenizer(token)
        assert operation_info is not None, "Token is not in the dictionary"
        return operation_info
        



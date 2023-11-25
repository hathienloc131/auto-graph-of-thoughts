from __future__ import annotations
import logging
from enum import Enum
from typing import List, Iterator, Dict, Callable, Union
from abc import ABC, abstractmethod
import itertools

from graph_of_thoughts.thoughts.thought import Thought


class OperationType(Enum):
    """
    Enum to represent different operation types that can be used as unique identifiers.
    """

    split: int = 0
    generate: int = 1
    improve: int = 2
    aggregate: int = 3


class Operation(ABC):
    """
    Abstract base class that defines the interface for all operations.
    """

    _ids: Iterator[int] = itertools.count(0)
    operation_type: OperationType = None
    operation_name: str = None


    def __init__(self) -> None:
        self.id: int = next(Operation._ids)
        self.predecessors: List[Operation] = []
        self.successors: List[Operation] = []
        self.executed: bool = False


    def can_be_executed(self) -> bool:
        return all(predecessor.executed for predecessor in self.predecessors)


    def get_previous_thoughts(self) -> List[Thought]:
        previous_thoughts: List[Thought] = [
            thought
            for predecessor in self.predecessors
            for thought in predecessor.get_thoughts()
        ]

        return previous_thoughts


    def add_predecessor(self, operation: Operation) -> None:
        self.predecessors.append(operation)
        operation.successors.append(self)


    def add_successor(self, operation: Operation) -> None:
        self.successors.append(operation)
        operation.predecessors.append(self)


    def execute(self, **kwargs) -> None:
        for i in range(len(self.predecessors)):
            if not self.predecessors[i].executed:
                self.predecessors[i].execute()

        self._execute(**kwargs)
        self.executed = True


    def _execute(self, **kwargs) -> None:
        print(self)

    # @abstractmethod
    # def get_thoughts(self) -> List[Thought]:
    #     pass

class Split(Operation):
    """
    Operation to split thoughts.
    """
    operation_type: OperationType = OperationType.split
    operation_name: str = "SPLIT"


    def __init__(self, num_split:int = 2) -> None:

        super().__init__()
        
        if num_split < 2:
            raise ValueError(f"num_split must greater than 1, but found {num_split}")
        
        self.num_split = num_split
        
        self.operation_name += f" {self.num_split}"


    def __repr__(self) -> str:
        return f"""Split Operation\nID:{self.id}\nNo. Split: {self.num_split};"""
    
class Generate(Operation):
    """
    Operation to generate thoughts.
    """
    operation_type: OperationType = OperationType.generate
    operation_name: str = "GENERATE"


    def __init__(self, num_try:int = 1, num_choice:int = 1) -> None:

        super().__init__()
        if num_choice > num_try:
            raise ValueError(f"num_choice must less than num_try, but found num_choice({num_choice}) > num_try({num_try})")
        
        if num_try < 1 or num_choice < 1:
            raise ValueError(f"num_try and num_choice must be positive")
        
        self.num_try = num_try
        self.num_choice = num_choice

        self.operation_name += f" {self.num_try} {self.num_choice}"


    def __repr__(self) -> str:
        return f"""Generate Operation\nID:{self.id}\nNo. Try: {self.num_try}\nNo. Choice: {self.num_choice};"""
    
class Improve(Generate):
    """
    Operation to Improve thoughts.
    """
    operation_type: OperationType = OperationType.improve
    operation_name: str = "IMPROVE"


    def __init__(self, num_try:int = 1, num_choice:int = 1) -> None:
        super().__init__(num_try, num_choice)

    def __repr__(self) -> str:
        return f"""Improve Operation\nID:{self.id}\nNo. Try: {self.num_try}\nNo. Choice: {self.num_choice};"""
    
class Aggregate(Operation):
    """
    Operation to Aggregate thoughts.
    """
    operation_type: OperationType = OperationType.aggregate
    operation_name: str = "AGGREGATE"


    def __init__(self, num_try:int = 1) -> None:
        super().__init__()
        if num_try < 1:
            raise ValueError(f"num_try must be positive")
        
        self.num_try = num_try

        self.operation_name += f" {self.num_try}"


    def __repr__(self) -> str:
        return f"""Aggregate Operation\nID:{self.id}\nNo. Try: {self.num_try};"""
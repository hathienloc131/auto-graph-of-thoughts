import json
import logging
from typing import List
from graph_of_thoughts.language_model import AbstractLanguageModel
from graph_of_thoughts.thoughts import GraphOfOperations, Thought
from graph_of_thoughts.prompter import Prompter
from graph_of_thoughts.parser import Parser


class Controller:
    """
    Controller class to manage the execution flow of the Graph of Operations,
    generating the Graph Reasoning State.
    This involves language models, graph operations, prompting, and parsing.
    """

    def __init__(
        self,
        lm: AbstractLanguageModel,
        graph: GraphOfOperations,
        prompter: Prompter,
        parser: Parser,
        problem_parameters: dict,
    ) -> None:
        """
        Initialize the Controller instance with the language model,
        operations graph, prompter, parser, and problem parameters.

        `Input`:
        - lm: `<AbstractLanguageModel>` An instance of the AbstractLanguageModel.
        - graph: `<OperationsGraph>` The Graph of Operations to be executed.
        - prompter: `<Prompter>` An instance of the Prompter class, used to generate prompts.
        - parser: `<Parser>` An instance of the Parser class, used to parse responses.
        - problem_parameters: `<dict>` Initial parameters/state of the problem.
        """
        self.lm = lm
        self.graph = graph
        self.prompter = prompter
        self.parser = parser
        self.problem_parameters = problem_parameters
        self.run_executed = False

    def run(self) -> None:
        """
        Run the controller and execute the operations from the Graph of
        Operations based on their readiness.
        Ensures the program is in a valid state before execution.

        `Raise`:
        - AssertionError: If the Graph of Operation has no roots.
        - AssertionError: If the successor of an operation is not in the Graph of Operations.
        """
        assert self.graph.roots is not None, "The operations graph has no root"

        execution_queue = [operation for operation in self.graph.operations if operation.can_be_executed()]

        while len(execution_queue) > 0:
            current_operation = execution_queue.pop(0)
            current_operation.execute(self.lm, self.prompter, self.parser, **self.problem_parameters)
            for operation in current_operation.successors:
                assert (
                    operation in self.graph.operations
                ), "The successor of an operation is not in the operations graph"
                if operation.can_be_executed():
                    execution_queue.append(operation)
        self.run_executed = True

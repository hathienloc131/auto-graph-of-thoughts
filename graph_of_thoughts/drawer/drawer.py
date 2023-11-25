from typing import Dict, List
from graph_of_thoughts.thoughts import GraphOfOperations, OperationFactory, OperationType, Operation, Split, Generate, Improve, Aggregate
from .tokenizer import Tokenizer

class Drawer():
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer:Tokenizer = tokenizer
        self.operation_factory:OperationFactory = OperationFactory()


    def decode(self, sequence: List[int])->List[Operation]:
        list_operation = []

        #Pop start and end token
        sequence.pop(0)
        sequence.pop(-1)

        for token in sequence:
            list_operation.append(self._idx2operation(token))

        return list_operation


    def degraph(self, sequence: List[int], is_visualize: bool = True) -> GraphOfOperations:
        """
            From Sequence of Token return Graph of Operations

            `input`:
                - sequence: List[int]

            `output`:
                - graph: GraphOfOperation
        """
        #Decode sequence of token
        decoded_operations = self.decode(sequence)

        graph = GraphOfOperations(is_visualize=is_visualize)
        for operation in decoded_operations:
            if len(graph.roots) == 0 or operation["type"] == OperationType.aggregate:
                graph.append_operation(self.operation_factory.create_operation(**operation))

                continue
            
            #Waitlist of Thoughts
            wait_thoughts: List[Operation] = []


            for i in range(len(graph.leaves)):
                if graph.leaves[i].operation_type == OperationType.split:
                    split_node: Split = graph.leaves[i]
                    for _ in range(split_node.num_split):
                        thought = self.operation_factory.create_operation(**operation)
                        thought.add_predecessor(split_node)

                        #Add this Thought into Waitlist
                        wait_thoughts.append(thought)
                else:
                    thought = self.operation_factory.create_operation(**operation)
                    thought.add_predecessor(graph.leaves[i])

                    #Add this Thought into Waitlist
                    wait_thoughts.append(thought)
            
            #Add Thought into Graph
            for i in range(len(wait_thoughts)):
                graph.add_operation(wait_thoughts[i])
        
        return graph


    def _idx2operation(self, token: int) -> Operation:
        operation_info = self.tokenizer(token)
        assert operation_info is not None, "Token is not in the dictionary"
        return operation_info
        



from typing import Dict, List
from graph_of_thoughts.thoughts import GraphOfOperations, OperationFactory, OperationType, Operation, Split
from .tokenizer import Tokenizer

class Drawer():
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer:Tokenizer = tokenizer
        self.operation_factory:OperationFactory = OperationFactory()


    def decode(self, sequence: List[int])->List[Operation]:
        list_operation = []

        #Pop start and end token

        for token in sequence[1:-1]:
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
        for operation_info in decoded_operations:
            if len(graph.roots) == 0 or operation_info["type"] == OperationType.aggregate:
                graph.append_operation(self.operation_factory.create_operation(**operation_info))

                continue
            
            #Waitlist of Operation
            wait_oprs: List[Operation] = []


            for i in range(len(graph.leaves)):
                if graph.leaves[i].operation_type == OperationType.split:
                    split_node: Split = graph.leaves[i]
                    
                    for j in range(split_node.num_split):
                        operation_info["part"] = j
                        opr = self.operation_factory.create_operation(**operation_info)
                        opr.add_predecessor(split_node)

                        #Add this Operation into Waitlist
                        wait_oprs.append(opr)
                else:
                    opr = self.operation_factory.create_operation(**operation_info)
                    opr.add_predecessor(graph.leaves[i])

                    #Add this Operation into Waitlist
                    wait_oprs.append(opr)
            
            #Add Thought into Graph
            for i in range(len(wait_oprs)):
                graph.add_operation(wait_oprs[i])
        
        return graph


    def _idx2operation(self, token: int) -> Operation:
        operation_info = self.tokenizer(token)
        assert operation_info is not None, "Token is not in the dictionary"
        return operation_info
        



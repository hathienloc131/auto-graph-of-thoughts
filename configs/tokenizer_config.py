from enum import Enum
from graph_of_thoughts.thoughts import OperationType
class RangeStrategy(Enum):
    """
    Enum representing the range strategy to generate list of operations
    """
    step = 0, # example n = 1, (1, 2, 3, 4, 5...) 
    power = 1 # example (2, 4, 8, 16, 32 ...)
    combine = 2 # example combine step n = 1 and power (1, 2, 3, 4, 5, 8, 16, 32 ...). The power range starts at (n*5)

TOKENIZER_CONFIG = {
    OperationType.split: {
        "start_num_split": 2,
        "end_num_split": 16,
        "range_strategy": RangeStrategy.combine,
        # if you use a power range strategy just ignore the n
        # else it define the step when perform step range strategy
        "n" : 1 
    },
    OperationType.improve: {
        "start_num_try": 1,
        "end_num_try": 16,
        "range_strategy": RangeStrategy.combine,
        "n" : 1 
    },
    OperationType.generate: {
        "start_num_try": 1,
        "end_num_try": 16,
        "range_strategy": RangeStrategy.combine,
        "n" : 1 
    },
    OperationType.aggregate: {
        "start_num_try": 1,
        "end_num_try": 16,
        "range_strategy": RangeStrategy.combine,
        "n" : 1 
    }
}
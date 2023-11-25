from graph_of_thoughts.thoughts import OperationType
from configs.tokenizer_config import TOKENIZER_CONFIG, RangeStrategy
from typing import Dict, List
import numpy as np
class Tokenizer():
    def __init__(self):
        self.length = 0
        self.dictionary = self._generate_dictionary()

    def __call__(self, key):
        if key < self.length:
            return self.dictionary[key]
        return None
    def _generate_dictionary(self):
        """
        Generate dictionary from the tokenizer configuration
        """
        dictionary = {}
        dictionary[0] = {"type": len(OperationType) + 1}
        dictionary[1] = {"type": len(OperationType) + 2}    

        index = 2

        for key, value in TOKENIZER_CONFIG.items():
            if isinstance(key, OperationType):
                list_choices = self._process_operation(key, value)
                for choice in list_choices:
                    
                    dictionary[index] = {"type": key, "num_split": choice} if key == OperationType.split else {"type": key, "num_try": choice, "num_choice": 1}
                    index += 1
            else:
                raise TypeError("Invalid operation type: {}".format(key))
        self.length = index
        return dictionary
    
    def _process_operation(self, operation_type: OperationType, config: Dict) -> List:
        start_range = config["start_num_split"] if operation_type == OperationType.split else config["start_num_try"]
        end_range = config["end_num_split"] if operation_type == OperationType.split else config["end_num_try"]
        return self._generate_range(config["range_strategy"], start_range, end_range, config["n"]).tolist()

    def _generate_range(self, strategy: RangeStrategy, start: int, end: int, n: int = 1) -> List:
        assert start < end, "Start range should be less than end range"
        assert n >= 1, "n step should be greater than or equal to 1"
        assert isinstance(strategy, RangeStrategy), "strategy should be in RangeStrategy"
        if strategy == RangeStrategy.step:
            return self._process_range_step(start, end, n)
        elif strategy == RangeStrategy.power:
            return self._process_range_power(start, end)
        else:
            return self._process_range_combine(start, end, n)

    def _process_range_step(self, start: int, end: int, n: int):
        return np.arange(start, end, n,  dtype=int)
    
    def _process_range_power(self, start: int, end: int):
        start_idx = int(np.ceil(np.log2(start)))
        end_idx = int(np.log2(end))
        list_range = np.arange(start_idx, end_idx + 1, step=1, dtype=int)
        power_range = np.power(list_range, 2)
        return power_range

    def _process_range_combine(self, start: int, end: int, n: int):
        first_end = int(start + n*5)
        first_array = self._process_range_step(start, first_end, n)
        if first_end <= end:
            second_array = self._process_range_power(first_end, end)
            final_array = np.concatenate([first_array, second_array])
            return final_array
        return first_array
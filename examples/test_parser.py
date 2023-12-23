from graph_of_thoughts.parser import SortingParser
from graph_of_thoughts.thoughts import Split

def run():
    parser = SortingParser()
    split_opr = Split(4)
    print(parser.parse_split_answer(split_opr.__dict__, {
        "state": f"Sort this list using merge sort algorithm\nInput",
        "current": "[9, 6, 7, 7, 2, 0, 2, 2, 3, 5, 0, 9, 2, 2, 4, 4, 5, 2, 5, 1, 2, 8, 3, 8, 3, 9, 6, 0, 4, 2, 2, 3]",
        },
        ["""{"0": [9, 6, 7, 7, 2, 0, 2, 2], "1": [3, 5, 0, 9, 2, 2, 4, 4], "2": [5, 2, 5, 1, 2, 8, 3, 8], "3": [3, 9, 6, 0, 4, 2, 2, 3]}"""]
    ))

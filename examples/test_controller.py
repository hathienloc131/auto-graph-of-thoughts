from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.parser import SortingParser


def run():
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()
    list = """9 + 4 + 5 - 1 - 9 + 0 + 3 + 5 - 9 + 2 - 1 - 3"""
    main_task = f"Calculation the expression and only answer the number: {list}"
    prompter = LanguageModelPrompter(lm, main_task)

    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 4, 9, 23, END_TOKEN]

    graph:GraphOfOperations = drawer.degraph(sequence, is_visualize=True)
    # graph.visualize()

    executor = Controller(
        lm,
        graph,
        prompter,
        SortingParser(),
        {
            "state": f"START",
            "current": "START",
            "phase": 0,
        },
    )

    executor.run()

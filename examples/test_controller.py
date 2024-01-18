from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.parser import SortingParser


def run():
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()
    list = """Two friends plan to walk along a 43-km trail, starting at opposite ends of the trail at the same time. If Friend P's rate is 15% faster than Friend Q's, how many kilometers will Friend P have walked when they pass each other?\n[ "A)21", "B)21.5", "C)22", "D)22.5", "E)23" ]"""
    main_task = f"Read the questions carefully and choose the correct option {list}"
    prompter = LanguageModelPrompter(lm, main_task)

    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 16, END_TOKEN]

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

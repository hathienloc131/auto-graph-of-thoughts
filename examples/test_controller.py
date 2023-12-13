from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.parser import Parser


def run():
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()
    prompter = LanguageModelPrompter(lm, "Sort this list using merge sort algorithm")

    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 4, 17, 26, END_TOKEN]

    graph:GraphOfOperations = drawer.degraph(sequence, is_visualize=True)

    executor = Controller(
        lm,
        graph,
        prompter,
        Parser(),
        {
            "state": f"Sort this list using merge sort algorithm\nInput",
            "original": ["Let's", "Start"],
            "current": "",
            "phase": 0,
        },
    )

    executor.run()

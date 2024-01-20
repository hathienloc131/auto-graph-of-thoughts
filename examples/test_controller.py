from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.judge import LanguageModelJudge
from graph_of_thoughts.parser import SortingParser



def run():
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()
    list = "[9, 6, 7, 7, 2, 0, 2, 2, 3, 5, 0, 9, 2, 2, 4, 4, 5, 2, 5, 1, 2, 8, 3, 8, 3, 9, 6, 0, 4, 2, 2, 3]"
    main_task = f"Sort this list {list}"
    prompter = LanguageModelPrompter(lm, main_task)
    judge = LanguageModelJudge(lm)


    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 4, 17, 23, END_TOKEN]

    graph:GraphOfOperations = drawer.degraph(sequence, is_visualize=True)
    # graph.visualize()

    executor = Controller(
        lm,
        graph,
        prompter,
        SortingParser(),
        judge,
        {
            "state": f"START",
            "current": "START",
            "phase": 0,
        },
    )

    executor.run()

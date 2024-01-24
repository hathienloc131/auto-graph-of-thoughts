import pandas as pd

from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.judge import LanguageModelJudge
from graph_of_thoughts.parser import SortingParser

def main_task(list: str):
    return f"Sort this list {list}"

def run(file_name: str):
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()

    df = pd.read_csv(file_name)

    prompter = LanguageModelPrompter(lm)
    judge = LanguageModelJudge(lm)

    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    sequence = [START_TOKEN, 4, 20, 27, END_TOKEN]

    
    # graph.visualize()

    for ind in df.index:
        try:
            graph:GraphOfOperations = drawer.degraph(sequence, is_visualize=True)
            executor = Controller(
                lm,
                graph,
                prompter,
                SortingParser(),
                judge,
                {
                    "state": f"START",
                    "current": "START",
                    "origin": main_task(df["Unsorted"][ind]),
                    "phase": 0,
                },
            )
            executor.run()
            print(df["Sorted"][ind])
            print("-------------------------------------------------------------------------")
        except Exception as e:
            print(ind, f"meet {e}")
    

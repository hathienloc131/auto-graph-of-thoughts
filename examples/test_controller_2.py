import pandas as pd
import numpy as np
from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT, ChatGemini
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.judge import LanguageModelJudge
from graph_of_thoughts.parser import SortingParser
from graph_of_thoughts.error_utils import error_score_keyword_counting

def main_task(paragraph: str):
    return f"Calculate the frequency of each country's appearance in the paragraph: '{paragraph}'"


def run(file_name: str, length: int):
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    lm = ChatGPT()

    df = pd.read_csv(file_name)

    prompter = LanguageModelPrompter(lm)
    judge = LanguageModelJudge(lm)
    # print(tokenizer.dictionary)
    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    # sequence = [START_TOKEN, 7, 17, 24, END_TOKEN] # 128
    # sequence = [START_TOKEN, 4, 17, 24, END_TOKEN] # 64

    sequence = [START_TOKEN, 2, 17, 24, END_TOKEN] # 32
    # sequence = [START_TOKEN, 17, END_TOKEN]

    error_score_list = []
    # graph.visualize()
    
    for ind in df.index:
        try:
            print(f"Attempt {ind}: \n")
            graph:GraphOfOperations = drawer.degraph(sequence, is_visualize=False)
            executor = Controller(
                lm,
                graph,
                prompter,
                SortingParser(),
                judge,
                {
                    "state": f"START",
                    "current": f'Paragraph: "{df['Text'][ind]}"',
                    "origin": main_task(df['Text'][ind]),
                    "phase": 0,
                },
            )
            executor.run()
            thought = executor.get_final_thoughts()[0][0].state["current"]
            print(thought)
            # error_s = error_score_keyword_counting(thought, df["INTERSECTION"][ind])
            # print(f"error score {ind}: {error_s}")
            # error_score_list.append(min(error_s, length))
            print("\n-------------------------------------------------------------------------\n")
        except Exception as e:
            print(ind, f"meet {e}")
        break
    print(error_score_list)
    print(np.mean(error_score_list))
    

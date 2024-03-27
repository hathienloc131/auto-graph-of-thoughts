import pandas as pd
import numpy as np
from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT, ChatGemini
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.judge import LanguageModelJudge
from graph_of_thoughts.parser import SortingParser
from graph_of_thoughts.error_utils import error_score_doc_merge

def main_task(problem, doc1, doc2, doc3, doc4):
    return f"""{problem}\nDocument 1: "{doc1}"\nDocument 2: "{doc2}"\nDocument 3: "{doc3}"\nDocument 4: "{doc4}"\n"""


def run(file_name: str, length: int):
    tokenizer = Tokenizer()
    drawer = Drawer(tokenizer)
    # print(tokenizer.dictionary)
    # exit()
    lm = ChatGemini()
    # lm_judge = ChatGPT()

    df = pd.read_csv(file_name)

    prompter = LanguageModelPrompter(lm, json_format = False)
    judge = LanguageModelJudge(lm)
    START_TOKEN = tokenizer(0)
    END_TOKEN = tokenizer(1)

    # sequence = [START_TOKEN, 7, 17, 24, END_TOKEN] # 128
    sequence = [START_TOKEN, 46, 60, END_TOKEN] # 64

    # sequence = [START_TOKEN, 2, 17, 24, END_TOKEN] # 32
    # sequence = [START_TOKEN, 17, END_TOKEN]

    error_score_list = []
    
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
                    "current": f"""Document 1: "{df['document1'][ind]}"\nDocument 2: "{df['document2'][ind]}"\nDocument 3: "{df['document3'][ind]}"\nDocument 4: "{df['document4'][ind]}"\n""",
                    "origin": main_task(df["problem"][ind],df["document1"][ind],df["document2"][ind],df["document3"][ind],df["document4"][ind]),
                    "phase": 0,
                },
            )
            executor.run()
            thought = executor.get_final_thoughts()[0][0].state["current"]
            error_s = error_score_doc_merge(lm,thought, df["document1"][ind],df["document2"][ind],df["document3"][ind],df["document4"][ind])
            error_score_list.append(error_s)
            print(f"error score {ind}: {error_s}")
            print("\n-------------------------------------------------------------------------\n")
        except Exception as e:
            print(ind, f"meet {e}")
    print(error_score_list)
    print(np.mean(error_score_list))
    

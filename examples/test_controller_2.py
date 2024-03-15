import pandas as pd
import numpy as np
from graph_of_thoughts.thoughts import OperationType, GraphOfOperations
from graph_of_thoughts.drawer import Tokenizer, Drawer, Controller
from graph_of_thoughts.language_model import ChatGPT, ChatGemini
from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.judge import LanguageModelJudge
from graph_of_thoughts.parser import SortingParser

def main_task(list: str):
    return f"Sorting this list {list}"

def parse_list(str_list):

    start_list = str_list.find('[') if str_list.find('[') != -1 else 0
    end_list = str_list.find(']') if str_list.find(']') != -1 else len(str_list)
    list = str_list[start_list: end_list].replace(' ', '').split(',')
    real_list = []
    for x in list:
        try:
            if x.isdigit():
                real_list.append(int(x))
        except:
            continue
    return real_list


def error_score(current_list, correct_list):
    current_list = parse_list(current_list)
    correct_list = parse_list(correct_list)
    num_errors = 0
    for i in range(10):
        num_errors += abs(
            sum([1 for num in current_list if num == i])
            - sum([1 for num in correct_list if num == i])
        )
    num_errors += sum(
        [1 for num1, num2 in zip(current_list, current_list[1:]) if num1 > num2]
    )

    return num_errors
    

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

    # sequence = [START_TOKEN, 7, 17, 24, 10, END_TOKEN]
    sequence = [START_TOKEN, 7, 17, 24, END_TOKEN]


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
                    "current": f"{df['Unsorted'][ind]}",
                    "origin": main_task(df['Unsorted'][ind]),
                    "phase": 0,
                },
            )
            executor.run()
            thought = executor.get_final_thoughts()[0][0].state["current"]
  
            error_s = error_score(thought, df["Sorted"][ind])
            print(f"error score {ind}: {error_s}")
            error_score_list.append(min(error_s, length))
            print("\n-------------------------------------------------------------------------\n")
        except Exception as e:
            print(ind, f"meet {e}")
    print(error_score_list)
    print(np.mean(error_score_list))
    

# %%
import re
from graph_of_thoughts.language_model import ChatGPT, ChatGemini
import pandas as pd
import numpy as np
from graph_of_thoughts.error_utils import error_score_doc_merge

# %%
with open("./output/new_version/gpt_35_1.0_temperature_doc_merge.log", encoding='utf8') as file:
    data = file.read()

# %%
data = data.split("</S>")

# %%
final_answer = []

# %%
for st in data:
    final_answer.append(st[st.find("Here is the summary NDA <S>:"):].replace("Here is the summary NDA <S>:\n<S>",""))

# %%
df = pd.read_csv('./datasets/doc_merge/documents.csv')
error_score_list = []
lm = ChatGPT()
for ind in df.index:
    try:
        print(f"Attempt {ind}: \n")
    
        thought = final_answer[ind]
        error_s = error_score_doc_merge(lm,thought, df["document1"][ind],df["document2"][ind],df["document3"][ind],df["document4"][ind])
        error_score_list.append(error_s)
        print(f"error score {ind}: {error_s}")
        print("\n-------------------------------------------------------------------------\n")
    except Exception as e:
        print(ind, f"meet {e}")
print(error_score_list)
print(np.mean(error_score_list))



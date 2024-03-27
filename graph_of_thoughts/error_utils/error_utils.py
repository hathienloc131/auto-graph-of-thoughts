from collections import Counter
import json
import numpy as np
def parse_list(str_list):

    start_list = str_list.find('[') if str_list.find('[') != -1 else 0
    end_list = str_list.find(']') if str_list.find(']') != -1 else len(str_list)
    list = str_list[start_list: end_list].replace(' ', '').replace("[", "").replace("]", "").replace("{", "").replace("}", "").split(',')
    real_list = []
    for x in list:
        try:
            if x.isdigit():
                real_list.append(int(x))
        except:
            continue
    return real_list

def string_to_list(str_list):

    assert str_list[0] == "[" and str_list[-1] == "]", "str_list is not a list."
    return [
        item.strip().replace("'", "").replace('"', "")
        for item in str_list[1:-1].split(", ")
    ]

def parse_set(str_set):

    start_set = str_set.find('[') if str_set.find('[') != -1 else 0
    end_set = str_set.find(']') if str_set.find(']') != -1 else len(str_set)
    set = str_set[start_set: end_set].replace(' ', '').replace("[", "").replace("]", "").split(',')
    real_set = {}
    for x in set:
        try:
            if x.isdigit():
                real_set.add(int(x))
        except:
            continue
    return real_set


def error_score_sorting(current_list, correct_list):
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

def error_score_intersection(current_set, correct_set):
    current_set = parse_list(current_set)
    correct_set = parse_list(correct_set)
    print(current_set, correct_set)
    common = sorted(correct_set)
    llm_solution = sorted(current_set)
    num_errors = 0
    common_idx = 0
    llm_idx = 0
    while common_idx < len(common) and llm_idx < len(llm_solution):
        if common[common_idx] == llm_solution[llm_idx]:
            common_idx += 1
            llm_idx += 1
        elif common[common_idx] < llm_solution[llm_idx]:
            common_idx += 1
            num_errors += 1
        elif common[common_idx] > llm_solution[llm_idx]:
            llm_idx += 1
            num_errors += 1
    num_errors += len(common) - common_idx + len(llm_solution) - llm_idx
    return num_errors

    
def error_score_keyword_counting(current_answer, correct_list):
    current_freq_dict = json.loads(current_answer)
    correct_freq_dict = dict(Counter((string_to_list(correct_list))))
    print(current_freq_dict, correct_freq_dict)
    countries_not_in_current = set(correct_freq_dict.keys()) - set(
        current_freq_dict.keys()
    )
    countries_not_in_correct = set(current_freq_dict.keys()) - set(
        correct_freq_dict.keys()
    )
    # count the number of errors
    num_errors = 0
    for country in countries_not_in_current:
        num_errors += abs(correct_freq_dict[country])
    for country in countries_not_in_correct:
        num_errors += abs(current_freq_dict[country])
    for country in set(correct_freq_dict.keys()) & set(current_freq_dict.keys()):
        num_errors += abs(correct_freq_dict[country] - current_freq_dict[country])
    return num_errors

SCORE_PROMPT = """
The following NDA <S> merges NDAs <Doc1> - <Doc4>.
Please score the merged NDA <S> in terms of how much redundant information is contained, independent of the original NDAs, as well as how much information is retained from the original NDAs.
A score of 10 for redundancy implies that absolutely no information is redundant, while a score of 0 implies that at least half of the information is redundant (so everything is at least mentioned twice). The higher the better.
A score of 10 for retained information implies that all information from the original NDAs is retained, while a score of 0 implies that no information is retained. The higher the better.
You may provide reasoning for your scoring, but the final score for redundancy should be between the tags <Redundancy> and </Redundancy>, and the final score for retained information should be between the tags <Retained> and </Retained>.

Here are NDAs <Doc1> - <Doc4>:

<Doc1>
{doc1}
</Doc1>

<Doc2>
{doc2}
</Doc2>

<Doc3>
{doc3}
</Doc3>

<Doc4>
{doc4}
</Doc4>

Here is the summary NDA <S>:
<S>
{s}
</S>
Example scoring:
<Redundancy>score</Redundancy>
<Retained>score</Retained>
Reasoning for above scoring...

Scoring:"""    

def error_score_doc_merge(lm, current_answer, doc1, doc2, doc3, doc4):
    current_prompt = SCORE_PROMPT.format(doc1 = doc1, doc2 = doc2, doc3 = doc3, doc4 = doc4, s=current_answer)
    print(current_prompt)
    num_errors = lm.get_response_texts(
                lm.query(current_prompt, num_responses=3, system_prompt="You are a helpfull assistant."))
    print("answer score:", num_errors)

    redundancy = []
    retained = []
    for error in num_errors:
        redundancy.append(int(error[error.find("<Redundancy>"):error.find("</Redundancy>")].replace("<Redundancy>","").replace("</Redundancy>","")))
        retained.append(int(error[error.find("<Retained>"):error.find("</Retained>")].replace("<Retained>","").replace("</Retained>", "")))
    num_errors = round(2/(1/(np.mean(retained)) + 1/(np.mean(redundancy))), 4)
    return num_errors
    
#6.5 9 8.5
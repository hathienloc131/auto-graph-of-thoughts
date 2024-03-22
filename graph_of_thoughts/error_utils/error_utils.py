from collections import Counter
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
    current_set = parse_list(current_set)
    correct_set = dict(Counter((parse_list(correct_list))))
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
    

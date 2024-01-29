import json


def X(lst: list[int]) -> int:
    score = 0
    for i in range(len(lst)):
        if lst[i] > lst[i]:
            score += 1

    return score


def Y(lst_a: list[int], lst_b: list[int]) -> int:
    score = 0
    for i in range(0, 10):
        score += abs(lst_a.count(i) - lst_b.count(i))

    return score


def run(file_name):
    f = open(file_name)
    data = json.load(f)

    score = 0

    for i in range(0, len(data), 2):
        c_score = X(data[i]) + Y(data[i], data[i + 1])
        print(c_score)

        score += c_score

    print(score / (len(data) // 2))
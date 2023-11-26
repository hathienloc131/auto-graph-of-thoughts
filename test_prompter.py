from graph_of_thoughts.prompter import LanguageModelPrompter
from graph_of_thoughts.language_model import ChatGPT
lm = ChatGPT()
prompter = LanguageModelPrompter(lm, "Sort this list using merge sort algorithm")
list = "[5,6,1,5,6,3,9,1,2,0,1,2,9,4,7,8]"
num_split = 4
print(f"Sort this list using merge sort algorithm {list}")
split_promtp = prompter.split_prompt({"state": f"{list}", "num_split": num_split})[0]
split_promtp = f"<Instruction>{split_promtp} Only output the {num_split} results, seperate with \\n without any addtional text or thoughts.</Instruction>\nInput: {list}\nOutput:"
split_result = lm.get_response_texts(lm.query(split_promtp))[0]
print(f"{split_promtp} {split_result}")
next_input = split_result.split("\n")
result = ""
_generate_prompt = ""
for input in next_input:
    raw_generate_prompt = prompter.generate_prompt({"state": f"{list} -> {input}"})
    generate_prompt = f"<Instruction>{raw_generate_prompt} Only output the result without any addtional text or thoughts.</Instruction>\nInput: {input}\nOutput: "
    _generate_prompt += raw_generate_prompt[0] + "|"
    print(generate_prompt)
    generate_result = lm.get_response_texts(lm.query(generate_prompt))[0]
    result += generate_result + ","
    print(generate_result)
aggregate_prompt = prompter.aggregate_prompt({"state": f"{next_input}->{result}"})
aggregate_prompt = f"<Instruction>{aggregate_prompt} Only output the result without any addtional text or thoughts.</Instruction>\nInput: {result}\nOutput: "
print(aggregate_prompt)
aggregate_result = lm.get_response_texts(lm.query(aggregate_prompt))[0]
print(aggregate_result)



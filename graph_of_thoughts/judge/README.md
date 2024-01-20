# 1. Prompt format

We create the prompt following this format where:
- **Raw Prompt** is the description of the current task (generated using **Prompter**)
- **Input**: Input of the current task.

1. **Split Prompt Format**: **num_split** is the additional information about the number of results.
```
<Instruction>
{Raw Prompt}
Only output the {num_split} results in format json {"0":..., "1": ...} without any addtional text or thoughts.
</Instruciton>
Input: {input}
Output:
```
2. **Other Prompts Format**: 
```
<Instruction>
{Raw Prompt}
Only output the result in format json {"0":...} without any addtional text or thoughts.
</Instruciton>
Input: {input}
Output:
```
---
Example split prompt for sorting task:
```
<Instruction>
Please split the list into four equal parts. 
Only output the 4 results in format json {"0":..., "1": ...} without any addtional text or thoughts.
</Instruciton>
Input: [0, 2, 3, 5, 1, 1, 9, 2, 5, 0, 2, 4]
Output:
```
# 2. How to make prompt for current operation?
1. Generate a raw prompt using **Prompter.type_prompt** (type of the current operation)
    ```python
    from graph_of_thoughts.prompter import LanguageModelPrompter
    from graph_of_thoughts.language_model import ChatGPT
    problem_description = "Sort this list using merge sort algorithm"
    lm = ChatGPT()
    prompter = LanguageModelPrompter(lm, problem_description)
    prompt_raw = prompter.split_prompt({"state": f"Sort this list using merge sort algorithm\nInput", "num_split": num_split})

    ```

2. Format raw prompt and input following the above format
    ```python
    prompt = f"""<Instruction>{prompt_raw} \nOnly output the {num_split} results in format json 
    {{\"0\":..., \"1\": ...}} without any addtional text or thoughts.</Instruction>
    Input: {list}
    Output:"""
    ```
from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter():

    def __init__(self, lm: AbstractLanguageModel, problem_description: str) -> None:
        super().__init__()
        self.lm = lm
        self.problem_description = problem_description

    def split_prompt(self, state_dicts: Dict, **kwargs) -> str:
        system_prompt = """You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task, just generate only split prompt."""
        query = f"""<Description>Generate a split prompt that will divide the previous task into exactly same {state_dicts['num_split']} part.</Description>
        Previous Task: {state_dicts["state"]}
        Split Prompt: """
        split_prompt_raw = "JUST USE IT FOR TESTING PROMPTER"#self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]

        split_prompt = f"""<Instruction>{split_prompt_raw} \nOnly output the {state_dicts['num_split']} results in format json {{\"0\":..., \"1\": ...}} without any addtional text or thoughts.</Instruction>\nInput: {state_dicts["current"]}\nOutput:"""

        return split_prompt
    
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        system_prompt = """You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task, just generate only the prompt."""
        query = f"""
        <Description>Generate a prompt that will perform the a next task after doing previous task.</Description>
        Previous Task: {state_dicts["state"]}
        Prompt: """
        generate_prompt_raw = "JUST USE IT FOR TESTING PROMPTER"#self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]

        generate_prompt = f"""<Instruction>{generate_prompt_raw} \nOnly output the result in format json {{\"0\":}} without any addtional text or thoughts.</Instruction>\nInput: {state_dicts["current"]}\nOutput:"""

        return generate_prompt
    
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        system_prompt = "You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task,, just generate only the aggregate prompt."
        query = f"""
        <Description>Generate a prompt that aggregate all results from the previous task into the main task.</Description>
        Previous Task: {state_dicts[0]["state"]}
        Aggregate Prompt: """
        aggregate_prompt_raw = "JUST USE IT FOR TESTING PROMPTER"#self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]

        aggregate_prompt = f"""<Instruction>{aggregate_prompt_raw} \nOnly output the result in format json {{\"0\":}} without any addtional text or thoughts.</Instruction>\nInput: {state_dicts[0]["current"]}\nOutput:"""

        return  aggregate_prompt
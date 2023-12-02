from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter():

    def __init__(self, lm: AbstractLanguageModel, problem_description: str) -> None:
        super().__init__()
        self.lm = lm
        self.problem_description = problem_description

    def split_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = """You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task, just generate only split prompt."""
        query = f"""
        <Description>Generate a split prompt that will divide the previous task into exactly same {state_dicts['num_split']} part.</Description>
        Previous Task: {state_dicts["state"]}
        Split Prompt: """
        split_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]

        return split_prompt_raw
    
    def generate_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = """You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task, just generate only the prompt."""
        query = f"""
        <Description>Generate a prompt that will perform the a next task after doing previous task.</Description>
        Previous Task: {state_dicts["state"]}
        Prompt: """
        generate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]


        return generate_prompt_raw
    
    def aggregate_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = "You are helpful prompt engineer. Do not solve the previous task directly or mention the previous task,, just generate only the aggregate prompt."
        query = f"""
        <Description>Generate a prompt that aggregate all results from the previous task into the main task.</Description>
        Previous Task: {state_dicts["state"]}
        Aggregate Prompt: """
        aggregate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))[0]


        return  aggregate_prompt_raw
from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter():

    def __init__(self, lm: AbstractLanguageModel, problem_description: str, system_prompt="You are a knowledgeable guide who can help you solve the task step by step. Answer clearly in at most 5 sentences.", json_format=True) -> None:
        super().__init__()
        self.lm = lm
        self.problem_description = problem_description
        self.system_prompt = system_prompt
        self.json_prompt = f' in json format with index, example {{"0":...,"1":...}}' if json_format else ', each answer in |answer| and seperated by \\t '

    def split_prompt(self, state_dicts: Dict, **kwargs) -> str:
        query = f"""<Description>Please give me a single NEXT STEP to divide the CURRENT STEP into exactly {state_dicts["num_split"]} subtasks to solve the MAIN TASK.</Description>\nMAIN TASK: {self.problem_description}\nCURRENT STEP: {state_dicts["state"]}\nNEXT STEP:"""
        split_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1))[0]

        split_prompt = f"""<Instruction>{split_prompt_raw} \nAnswer each subtask seperately{self.json_prompt}without any addtional text or thoughts.</Instruction>\nInput: {state_dicts["current"]}\nAnswer:"""

        return split_prompt
    
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        query = f"""<Description>Please give me the NEXT STEP to solve the MAIN TASK after completing the CURRENT STEP.</Description>\nMAIN TASK: {self.problem_description}\nCURRENT STEP: {state_dicts["state"]}\nNEXT STEP:"""
        generate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1))[0]
        
        generate_prompt = f"""<Instruction>{generate_prompt_raw} \nOnly answer the result{self.json_prompt}without any addtional text or thoughts.</Instruction>\nInput: {state_dicts["current"]}\nAnswer:"""

        return generate_prompt
    
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        query = f"""<Description>Please give me a single NEXT STEP to aggregate or combine into FINAL RESULT to solve the MAIN TASK by using all results from CURRENT STEPS.</Description>\nMAIN TASK: {self.problem_description}\nCURRENT STEPS: {state_dicts["state"]}\nFINAL RESULT:"""
        aggregate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1))[0]

        aggregate_prompt = f"""<Instruction>{aggregate_prompt_raw} \nOnly answer the result{self.json_prompt}without any addtional text or thoughts.</Instruction>\nInput: {state_dicts["current"]}\nAnswer:"""

        return  aggregate_prompt
    

   
    def improve_prompt(self, state_dicts: Dict, **kwargs) -> str:
        query = f"""<Description>Give me a single STEP to improve the result from the CURRENT TASK by checking for errors and correct them if it exists.</Description>\nCURRENT TASK: {state_dicts["state"]}\nSTEP:"""
        improve_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1))[0]

        improve_prompt = f"""<Instruction>{improve_prompt_raw} \nOnly answer the result{self.json_prompt}without any addtional text or thoughts. If nothing is wrong, return the original input. </Instruction>\nInput: {state_dicts["current"]}\nAnswer:"""

        return  improve_prompt
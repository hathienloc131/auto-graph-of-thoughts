from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter(Prompter):

    def __init__(self, lm: AbstractLanguageModel, system_prompt="""You are a helpful guide that guides the user by instructing them on the NEXT TASK based on the PREVIOUS TASK and RESULT OF PREVIOUS TASK. \n NEXT TASK must meet the given DESCRIPTION. \n  If the PREVIOUS TASK is START, it mean that you have just start to instruct user. \n Only answering NEXT TASK without any additional text.""", json_format=True) -> None:
        super().__init__()
        self.lm = lm
        self.system_prompt = system_prompt

    def split_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""<Description>Give me a NEXT TASK that must divide or split PREVIOUS TASK knowing RESULT OF PREVIOUS TASK into exactly the same {state_dicts["num_split"]} subtasks. </Description> \n PROBLEM: {state_dicts["origin"]} \n PREVIOUS TASK: {state_dicts["state"]} \n RESULT OF PREVIOUS TASK: {state_dicts["current"]} \n NEXT TASK:"""

        split_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]

        split_prompt = f"""<Instruction>{split_prompt_raw}</Instruction> \n INPUT: {state_dicts["current"]} \n PROBLEM: {state_dicts["origin"]} \n OUTPUT:"""
        return split_prompt_raw, split_prompt
    
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""<Description>Give me ONLY the TASK that use exactly RESULT OF PREVIOUS TASK to get closer PROBLEM after have finished necessary information in PREVIOUS TASK.</Description> \n PROBLEM: {state_dicts["origin"]} \n PREVIOUS TASK: {state_dicts["state"]} \n RESULT OF PREVIOUS TASK: {state_dicts["current"]} \n TASK:"""
        generate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        
        generate_prompt = f"""<Instruction>{generate_prompt_raw} </Instruction> \n INPUT: {state_dicts["current"]} \n PROBLEM: {state_dicts["origin"]} \n OUTPUT:"""
        return generate_prompt_raw, generate_prompt
    
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""<Description>Please give me ONLY a single NEXT TASK that must aggregate or combine into final result to solve the PROBLEM by using all results from PREVIOUS TASKS.</Description> \n PROBLEM: {state_dicts["origin"]} \n PREVIOUS TASK: {state_dicts["state"]} \n RESULT OF PREVIOUS TASK: {state_dicts["current"]} \n NEXT TASK:"""
        aggregate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]

        aggregate_prompt = f"""<Instruction>{aggregate_prompt_raw} </Instruction> \n INPUT: {state_dicts["current"]} \n PROBLEM: {state_dicts["origin"]} \n OUTPUT:"""

        return  aggregate_prompt_raw, aggregate_prompt
    

   
    def improve_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""<Description>Give me ONLY a single TASK to improve the result from the PREVIOUS TASK by describing how to check error of RESULT OF PREVIOUS TASK and correct them if it exists.</Description> \n PROBLEM: {state_dicts["origin"]} \n PREVIOUS TASK: {state_dicts["state"]} \n RESULT OF PREVIOUS TASK: {state_dicts["current"]} \n NEXT TASK:"""
        improve_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]

        improve_prompt = f"""<Instruction>{improve_prompt_raw} </Instruction> \n INPUT: {state_dicts["current"]} \n PROBLEM: {state_dicts["origin"]} \n OUTPUT:"""

        return  improve_prompt_raw, improve_prompt
    
    def score_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""<Description>Give me a list of SCORING CRITERIA used to evaluate the correctness of answer based on PREVIOUS TASK. List each criteria in the new line</Description> \n PREVIOUS TASK: {state_dicts["state"]} \n SCORING CRITERIA:"""
        score_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]

        return  score_prompt_raw
        
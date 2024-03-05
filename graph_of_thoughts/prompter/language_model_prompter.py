from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter(Prompter):

    def __init__(self, lm: AbstractLanguageModel, system_prompt="""You are a helpful guide that guides the user by providing instructions for the NEXT TASK based on the PREVIOUS TASK and its result. The NEXT TASK must meet the given description. If the PREVIOUS TASK is START, this means you are beginning the instruction process. Only provide the NEXT TASK, without additional text.""", json_format=True) -> None:
        super().__init__()
        self.lm = lm
        self.system_prompt = system_prompt
        self.step_system_prompt="""You are a helpful guide that instructs user step by step to perform their TASK knowing INPUT."""


    def split_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""Give me a NEXT TASK that divides the PREVIOUS TASK into {state_dicts["num_split"]} equal subtasks, taking into account the RESULT OF PREVIOUS TASK.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""

        split_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        step = self.step_prompt(split_prompt_raw, state_dicts["current"])
        split_prompt = f"""Do exactly INSTRUCTION: {split_prompt_raw} \n{step}\nOnly output {state_dicts["num_split"]} final results without any additional text or thought!\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(split_prompt)

        return split_prompt_raw, split_prompt
    
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""After completing the PREVIOUS TASK, give me the required TASK that use only RESULT OF PREVIOUS TASK to progress towards solving the PROBLEM.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nTASK:"""
        generate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        step = self.step_prompt(generate_prompt_raw, state_dicts["current"])
        generate_prompt = f"""INSTRUCTION: {generate_prompt_raw} \n{step}\nOnly output final result without any additional text or thought!\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(generate_prompt)
        return generate_prompt_raw, generate_prompt
    
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""Please give me ONLY a single NEXT TASK that aggregate or combine or merge all its RESULT OF PREVIOUS TASK into final result from PREVIOUS TASKS to solve the PROBLEM.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""
        aggregate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        step = self.step_prompt(aggregate_prompt_raw, state_dicts["current"])
        aggregate_prompt = f"""INSTRUCTION: {aggregate_prompt_raw} \n{step}\nOnly output final result without any additional text or thought!\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(aggregate_prompt)
        return  aggregate_prompt_raw, aggregate_prompt
    

   
    def improve_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        # query = f"""<Description>Give me ONLY a single TASK to improve the result OF PREVIOUS TASK from the PREVIOUS TASK by describing how to check error of RESULT OF PREVIOUS TASK and correct them if it exists.</Description> \nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""
        improve_prompt_raw = self.score_prompt(state_dicts)

        improve_prompt = f"""Answer only OUTPUT is the same as INPUT by correcting any error appeared in INPUT when processing from TASK without any additional text based on this list CRITERIA. If there is error, fix it in output. If there is no error, just answer orignal INPUT. CRITERIA: {improve_prompt_raw}.\nTASK: {state_dicts["state"]} \nINPUT: {state_dicts["current"]} \nOUTPUT:"""

        return  improve_prompt_raw, improve_prompt
    
    def score_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""INSTRUCTION: Give me a list of SCORING CRITERIA used to evaluate the correctness of answer based on PREVIOUS TASK.\nPREVIOUS TASK: {state_dicts["state"]} \nSCORING CRITERIA:"""
        score_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]

        return  score_prompt_raw
        
    def step_prompt(self, task, input):
        query = f"""Give me step by step to perform TASK on INPUT.\nTASK: {task}\nINPUT: {input}\nSTEP:"""
        step = self.lm.get_response_texts(self.lm.query(query, 1, self.step_system_prompt))[0]
        return step
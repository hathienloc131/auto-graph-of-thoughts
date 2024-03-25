from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter(Prompter):

    def __init__(self, lm: AbstractLanguageModel, system_prompt="""You are a helpful guide that guides the user by providing instructions for the NEXT TASK based on the PREVIOUS TASK and RESULT OF PREVIOUS TASK.\nThe NEXT TASK must meet the given description.\nIf the PREVIOUS TASK is START, this means you are beginning the instruction process.\nDo not mention RESULT OF PREVIOUS TASK in NEXT TASK.\nOnly output NEXT TASK without additional text or thought.""", json_format=True) -> None:
        super().__init__()
        self.lm = lm
        self.system_prompt = system_prompt
        self.json_format = json_format
        self.step_system_prompt="""You are a helpful guide that instructs user step by step to perform their TASK and knowing its INPUT."""
        self.score_system_prompt="""You are a helpful guide that give user a list of required CRITERIA to evaluate the correctness of their TASK."""
        self.error_system_prompt="""You are a helpful guide that indicates any errors in user OUTPUT after the user performs their TASK on that INPUT. You should indacate details error as possible including where the error occurred, what caused the error, and how to fix the error."""


    def split_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""Give me a NEXT TASK that divides the PREVIOUS TASK into {state_dicts["num_split"]} equal subtasks, taking into account the RESULT OF PREVIOUS TASK.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""

        split_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        step = self.step_prompt(split_prompt_raw, state_dicts["current"], {state_dicts["origin"]})
        split_prompt = f"""Do exactly INSTRUCTION: {split_prompt_raw} \n{step}\nOnly output {state_dicts["num_split"]} final results without any additional text or thought!\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(step)

        return split_prompt_raw, split_prompt
    
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""After completing the PREVIOUS TASK, give me the required NEXT TASK that use only RESULT OF PREVIOUS TASK as INPUT to progress towards solving the PROBLEM.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]}\nRESULT OF PREVIOUS TASK: {state_dicts["current"]}\nNEXT TASK:"""
        generate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        step = self.step_prompt(generate_prompt_raw, state_dicts["current"], {state_dicts["origin"]})
        generate_prompt = f"""INSTRUCTION: {generate_prompt_raw} \n{step}\nOnly output final result without any additional text or thought!{" Answer in JSON format" if self.json_format else ""}\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(step)
        return generate_prompt_raw, generate_prompt
    
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""Please give me ONLY a single NEXT TASK that combine or integrate all its RESULT OF PREVIOUS TASK into a single result from PREVIOUS TASKS to solve the PROBLEM.\nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""
        aggregate_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        print(query)
        step = self.step_prompt(aggregate_prompt_raw, state_dicts["current"], {state_dicts["origin"]})
        aggregate_prompt = f"""INSTRUCTION: {aggregate_prompt_raw} \n{step}\nOnly output final result without any additional text or thought!{" Answer in JSON format" if self.json_format else ""}\nINPUT: {state_dicts["current"]}\nOUTPUT:"""
        print(aggregate_prompt)
        print(step)
        
        return  aggregate_prompt_raw, aggregate_prompt
    

   
    def improve_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        # query = f"""<Description>Give me ONLY a single TASK to improve the result OF PREVIOUS TASK from the PREVIOUS TASK by describing how to check error of RESULT OF PREVIOUS TASK and correct them if it exists.</Description> \nPROBLEM: {state_dicts["origin"]} \nPREVIOUS TASK: {state_dicts["state"]} \nRESULT OF PREVIOUS TASK: {state_dicts["current"]} \nNEXT TASK:"""
        improve_prompt_raw = self.score_prompt(state_dicts)
    
        improve_prompt = f"""INSTRUCTION: Use CRITERIA to indacate the error. Then give me the FINAL OUTPUT, that fix all error appearing in OUTPUT after performing TASK on its INPUT.\nOnly output final result without any additional text or thought!\nCRITERIA: {improve_prompt_raw}\nTASK: {state_dicts['state']}\nINPUT: {state_dicts['previous']}\nOUTPUT: {state_dicts['current']}\nFINAL OUTPUT:"""
        print(improve_prompt)
        return  improve_prompt_raw, improve_prompt
    
    def error_prompt(self, input, output, task):
        query = f"""Give me a list of all errors if exists in OUTPUT after performing TASK on INPUT.\nTASK: {task}\nINPUT: {input}\nOUTPUT: {output}\nERROR:"""
        error = self.lm.get_response_texts(self.lm.query(query, 1, self.error_system_prompt))[0]
        return error
    
    def score_prompt(self, state_dicts: Dict, **kwargs) -> tuple[str, str]:
        query = f"""Give me a list of SCORING CRITERIA used to evaluate the correctness of answer when performing TASK.\nOnly output SCORING CRITERIA without any additional text or thought!.\nTASK: {state_dicts["state"]}\nSCORING CRITERIA:"""
        score_prompt_raw = self.lm.get_response_texts(self.lm.query(query, 1, self.score_system_prompt))[0]

        return  score_prompt_raw
        
    def step_prompt(self, task, input, problem):
        query = f"""Give me step by step to perform TASK on INPUT to progress towards solving the PROBLEM. Double check to correct any error in each step.\nPROBLEM: {problem}\nTASK: {task}\nINPUT: {input}\nSTEP:"""
        step = self.lm.get_response_texts(self.lm.query(query, 1, self.step_system_prompt))[0]
        return step
from typing import Dict, List
from .prompter import Prompter
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelPrompter():

    def __init__(self, lm: AbstractLanguageModel, problem_description: str) -> None:
        super().__init__()
        self.lm = lm
        self.problem_description = problem_description

    def split_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = "You are responsible for generate a split prompt that split the current task into {} exactly same sub-tasks based on the previous state given by user. Just generate only split prompt.".format(state_dicts['num_split'])
        query = f"""Previous state: {state_dicts["state"]}\Split Prompt: """

        return self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))
    
    def generate_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = "You are responsible for generate a prompt that perform the next task that solve the problem based on the output of the previous state given by user. Just generate only the prompt."
        query = f"""Previous state: {state_dicts["state"]}\Generate Prompt: """

        return self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))
    
    def aggregate_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        system_prompt = "You are responsible for generate aggregate prompt that aggregate all the results from the sub-task into main task based on the output of the previous state given by user. Just generate only the aggregate prompt."
        query = f"""Previous state: {state_dicts["state"]}\Aggregate Prompt: """

        return self.lm.get_response_texts(self.lm.query(query, 1, self.problem_description + system_prompt))
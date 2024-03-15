import json
from typing import Dict, List, Union

from .parser import Parser
from . import utils


class SortingParser(Parser):
    """
    Sorting Parsers are used to parse the responses from the language models. To help the GoT to solve sorting problem.
    """
    
    def parse_split_answer(self, split_config: Dict, state: Dict, texts: List[str]) -> List[Dict]:
        """
        Parse the response from the language model for a split prompt.
        
        `Input`:
        - split_config: `<Dict>` The Split Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<List[Dict]>`: List of states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        new_states = []
        text = texts[0]
        # We expect a json which contains the four lists named "<S>" and end with "<\S>"
        # cut everything until the opening bracket and everything after the closing bracket
        try:

            _texts = text.split("\n")
            for part, ans in enumerate(_texts):
                new_state = state.copy()
                new_state["previous"] = new_state["current"]
                new_state["current"] =f"{str(part + 1)}: {ans}"
                new_state["part"] = int(part)
                new_states.append(new_state)
            
            return new_states
        except Exception as e:
            raise Exception(f"Could not parse step answer: {text}. Encountered exception: {e}")
        
    

    def parse_generate_answer(self, gen_config: Dict, state: Dict, texts: List[str]) -> List[Dict]:
        """
        Parse the response from the language model for a generation prompt.
        
        `Input`:
        - gen_config: `<Dict>` The Generation Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<List[Dict]>`: List of states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        new_states = []
        for text in texts:
            # We expect a json which contains the four lists named "List 1" to "List 4"
            # cut everything until the opening bracket and everything after the closing bracket
            try:
                new_state = state.copy()
                new_state["previous"] = new_state["current"]
                new_state["current"] = text
                new_states.append(new_state)
            except Exception as e:
                raise Exception(f"Could not parse step answer: {text}. Encountered exception: {e}")
        return new_states
    

    def parse_aggregate_answer(self, agg_config: Dict, states: List[Dict], texts: List[str]) -> Union[Dict, List[Dict]]:
        """
        Parse the response from the language model for a aggregation prompt.
        
        `Input`:
        - agg_config: `<Dict>` The Aggregate Operation's Config used to check number of response
        - states: `List<Dict>` The thought states used to generate the prompt.
        - texts: `List<str>` The responses to the prompt from the language model.

        `Output`:
        - `<Union[Dict, List[Dict]]>`: states after parsed

        `Raises`:
        - `AssertionError`: If states don't have enough response.
        """
        assert len(states) > agg_config[""], "Expected more states for aggregation answer."
        new_states = []
        for text in texts:
            answers = text.strip().split("\n")
            if any(["Output" in answer for answer in answers]):
                # cut elements until last output is found
                for answer in reversed(answers):
                    if "Output" in answer:
                        answers = answers[answers.index(answer) :]
                        break

            answers_stripped = [
                answer for answer in answers if "[" in answer and "]" in answer
            ]
            if len(answers_stripped) == 0:
                for answer in answers:
                    answer = "[" + answer + "]"
                    try:
                        answer_converted = utils.string_to_list(answer)
                        if len(answer_converted) > 0:
                            answers_stripped.append(answer)
                    except:
                        pass
            if len(answers_stripped) == 0:
                raise Exception(
                    f"Could not parse aggregation answer: {text}. Returning empty list."
                )
            else:
                answer = [
                    answer[answer.index("[") : answer.index("]") + 1]
                    for answer in answers_stripped
                ][0]
            states = sorted(states, key=lambda x: x["part"])
            merged_unsorted_sublists = (
                states[0]["unsorted_sublist"][:-1]
                + ", "
                + states[1]["unsorted_sublist"][1:]
            )
            new_state = states[0].copy()
            new_state["current"] = answer
            new_state["unsorted_sublist"] = merged_unsorted_sublists
            new_states.append(new_state)
        return new_states


    def parse_improve_answer(self, state: Dict, texts: List[str]) -> Dict:
        pass
    
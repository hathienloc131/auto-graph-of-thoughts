from typing import Dict, List
from .judge import Judge
from graph_of_thoughts.language_model import AbstractLanguageModel

class LanguageModelJudge(Judge):

    def __init__(self, lm: AbstractLanguageModel, system_prompt="""You are good at judgement. Answer the list of rank of CANDIDATE OUTPUTS based on SCORING CRITERIA and CURRENT TASK. Answer the brief reason in few words at the first line. Answer the list of rank in the end line with this format, example: [3, 2, 0, 1, 4], the first number is the best candidate answer and the last number is the worst candidate answer.""") -> None:
        super().__init__()
        self.lm = lm
        self.system_prompt = system_prompt

    def ranking(self, score_prompt, current_task, candidate, num_choices = 1) -> tuple[str, str]:
        assert num_choices <= len(candidate), 'num_choices must be less than or equal candidate'
        candidate_answer = "\n".join([f"Candidate {e}. {answer}" for e, answer in enumerate(candidate)])
        query = f"""<SCORING CRITERIA>{score_prompt}</SCORING CRITERIA> \n CURRENT TASK:{current_task} {candidate_answer}\n ANSWER:"""
        ranking_answer = self.lm.get_response_texts(self.lm.query(query, 1, self.system_prompt))[0]
        try:
            ranking_answer = ranking_answer.split('\n')[-1]
            rank_list = self.extract_list(ranking_answer)

            answer = [candidate[r] for r in rank_list[:num_choices]]
        except Exception as e:
            answer = [candidate[0]]
        
        return answer

    def extract_list(self, ranking_answer):
        start_list = ranking_answer.find('[')
        end_list = ranking_answer.find(']')
        if start_list == -1 or end_list == -1:
            raise ValueError('Could not extract list from ranking answer')
        
        rank_list = []
        list = ranking_answer[start_list:end_list + 1].split(',')
        for num in list:
            try:
                rank_list.append(int(num))
            except:
                continue
        if len(rank_list) == 0:
            rank_list = [0]
        return rank_list
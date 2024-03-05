# Copyright (c) 2023 ETH Zurich.
#                    All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# main author: Nils Blach

import backoff
import openai
import os
import random
import time
import google.generativeai as genai
from typing import List, Dict, Union
from multiprocessing.pool import ThreadPool
from .abstract_language_model import AbstractLanguageModel
from configs.gemini_key import GEMINI_API_KEY

class ChatGemini(AbstractLanguageModel):
    def __init__(
        self, model_name: str = "chat-gemini", cache: bool = False
    ) -> None:
        """
       
        :param config_path: Path to the configuration file. Defaults to "".
        :type config_path: str
        :param model_name: Name of the model, default is 'chatgpt'. Used to select the correct configuration.
        :type model_name: str
        :param cache: Flag to determine whether to cache responses. Defaults to False.
        :type cache: bool
        """
        super().__init__(model_name, cache)
        self.config: Dict = self.config[model_name]
        # The model_id is the id of the model that is used for chatgpt, i.e. gpt-4, gpt-3.5-turbo, etc.
        self.model_id: str = self.config["model_id"]
        # The prompt_token_cost and response_token_cost are the costs for 1000 prompt tokens and 1000 response tokens respectively.
        self.prompt_token_cost: float = self.config["prompt_token_cost"]
        self.response_token_cost: float = self.config["response_token_cost"]
        # The temperature of a model is defined as the randomness of the model's output.
        self.temperature: float = self.config["temperature"]
        # The maximum number of tokens to generate in the chat completion.
        self.max_tokens: int = self.config["max_tokens"]
        # The stop sequence is a sequence of tokens that the model will stop generating at (it will not generate the stop sequence).
        self.stop: Union[str, List[str]] = self.config["stop"]

        self.api_key: str = GEMINI_API_KEY
        if self.api_key == "":
            raise ValueError("OPENAI_API_KEY is not set")
        genai.configure(api_key = self.api_key)
        self.client = genai.GenerativeModel(self.model_id)

        self.system_prompt = """You are helpful assistant. Your goal is to perform actions precisely as the user's INSTRUCTION describe, transforming their INPUT into the desired OUTPUT.\nTo do this, you need to analyze the PROBLEM they present but do not solve it directly.\nInstead, you use the PROBLEM to understand what changes need to be made to the INPUT."""

    def query(self, query: str, num_responses: int = 1, system_prompt: str = None) -> Dict:
        """
        Query the OpenAI model for responses.

        :param query: The query to be posed to the language model.
        :type query: str
        :param num_responses: Number of desired responses, default is 1.
        :type num_responses: int
        :return: Response(s) from the OpenAI model.
        :rtype: Dict
        """
        message = ""
        if system_prompt is None:
            system_prompt = self.system_prompt

        message += f"{system_prompt}.\n\n{query}"
        if self.cache and query in self.respone_cache:
            return self.respone_cache[query]

        if num_responses == 1:
            response = [self.chat(message, num_responses)]
        else:
            response = []
            next_try = num_responses
            total_num_attempts = num_responses
            while num_responses > 0 and total_num_attempts > 0:
                try:
                    assert next_try > 0
                    res = self.chat(message, next_try)
                    response.append(res)
                    num_responses -= next_try
                    next_try = min(num_responses, next_try)
                except Exception as e:
                    next_try = (next_try + 1) // 2
                    time.sleep(random.randint(1, 3))
                    total_num_attempts -= 1

        if self.cache:
            self.respone_cache[query] = response
        return response

    @backoff.on_exception(
        backoff.expo, openai.OpenAIError, max_time=10, max_tries=6
    )
    def chat(self, messages: str, num_responses: int = 1) -> Dict:
        """
        Send chat messages to the OpenAI model and retrieves the model's response.
        Implements backoff on OpenAI error.

        :param messages: A list of message dictionaries for the chat.
        :type messages: str
        :param num_responses: Number of desired responses, default is 1.
        :type num_responses: int
        :return: The OpenAI model's response.
        :rtype: Dict
        """        
        config = genai.GenerationConfig(candidate_count=1, 
                                        max_output_tokens=self.max_tokens,
                                        temperature=self.temperature, 
                                        stop_sequences=self.stop)

        with ThreadPool() as pool:
            response = pool.starmap(self.generate_chat, [(messages, config) for _ in range(num_responses)])
        return response
    
    def generate_chat(self, chat, config):
        return self.client.generate_content(chat, generation_config=config).text

    def get_response_texts(self, query_response) -> List[str]:
        return query_response[0]
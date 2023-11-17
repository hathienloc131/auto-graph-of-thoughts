from graph_of_thoughts.language_model import ChatGPT

lm = ChatGPT()
responses = lm.query("Give me a name", num_responses=2)
print(responses)
print(lm.get_response_texts(responses))
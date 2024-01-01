# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
import requests
from llama import Llama
from updated_strategy import update_rl_strategy 

# Function to get user query from Django app
def get_chatbot_query(django_endpoint: str) -> str:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        return response.json().get('query')
    else:
        raise Exception("Failed to get query from Django chatbot app")

def assess_value(
    ckpt_dir: str,
    tokenizer_path: str,
    django_endpoint: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    """
    Assess the 'value' of the current position in a task using the LLaMA model.
    Args as described.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    user_query = get_chatbot_query(django_endpoint)

    # Call the function to get the updated strategy
    strategy_dict = update_rl_strategy(ckpt_dir, tokenizer_path, django_endpoint)
    strategy = strategy_dict["updated_rl_strategy"]  # Access the updated strategy

    # Initialize the LLaMA model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Custom prompt based on user query and strategy
    prompt = f"<Assessing_Value>\nYou, as the language model, evaluate the 'value' of your current position in a task. In summarization, you gauge the relevance and importance of information. For search and Q&A, you estimate the accuracy and usefulness of potential answers. In creative writing, you weigh the effectiveness of narrative elements, and in coding, you consider the functionality and efficiency of code structures. Just like a gamer assessing their standing in a game, you ask yourself: How good is the current position?— Current task: {user_query}. Strategy: {strategy}."

    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    value_assessment = response[0]['generation']

    return {"value_assessment": value_assessment}

if __name__ == "__main__":
    fire.Fire(assess_value)


# Code Summary:
# Predicting Outcomes: As the language model updates its strategy, it enters a phase akin to a skilled gamer predicting the next turns in a complex 
# strategy game. It assesses three key elements akin to game dynamics:

# Evaluating the Position (Value): Just as a gamer evaluates their current standing in a game, the model assesses the 'value' of the current situation.
# In terms of summarization, it gauges the relevance and importance of information. For search and Q&A, it estimates the accuracy and usefulness of 
# potential answers. In creative writing, it weighs the effectiveness of narrative elements, and in coding, it considers the functionality and efficiency
# of code structures.


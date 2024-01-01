# Copyright (c) Enyimba AI, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Apache License.

import fire
import requests
from llama.llama import Llama
from typing import Dict

# Importing the functions from other modules
from language_tree_search import generate_branches as get_branches_info
from updated_strategy import update_rl_strategy
from value import assess_value

# Function to get user query from Django app
def get_user_query(django_endpoint: str) -> str:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        return response.json().get('query')
    else:
        raise Exception("Failed to get query from Django app")

def determine_best_move(
    reward_endpoint: str,
    ckpt_dir: str,
    tokenizer_path: str,
    django_endpoint: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
) -> Dict:
    """
    Determine the optimal action or move for the given task.
    Args as described.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    user_query = get_user_query(django_endpoint)

    # Defer the import of reward_signal
    try:
        from reward import evaluate_reward   # Import inside the function
        reward_signal_dict = evaluate_reward(reward_endpoint, ckpt_dir, tokenizer_path, django_endpoint)
        reward_signal_value = reward_signal_dict["reward_signal"]  # Fetch the reward signal
    except Exception as e:
        reward_signal_value = None  # Default to None if there's an issue

    branches_info = get_branches_info(ckpt_dir, tokenizer_path, django_endpoint)
    strategy_dict = update_rl_strategy(ckpt_dir, tokenizer_path, django_endpoint) if reward_signal_value else "default_strategy"
    strategy = strategy_dict["updated_rl_strategy"] if reward_signal_value else strategy_dict
    value_dict = assess_value(ckpt_dir, tokenizer_path, django_endpoint)
    value = value_dict["value_assessment"]

    # Initialize the LLaMA model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Custom prompt based on inputs
    prompt = f"<Choosing_Best_Move>\nUser Query: {user_query}\nBranches Info: {branches_info}\nUpdated Strategy: {strategy}\nValue Assessment: {value}\n\nWhich action is the best to take?
                Acting as the language model, you determine the 'policy' - the best course of action for your current task. You might decide which key points to include in a summary, which sources to pull from in a search, the most engaging 
                direction for a creative piece, the most helpful answer in Q&A, or the most suitable code in a programming task. This mirrors a player selecting the optimal action in a game. You contemplate: Which action is the best to take?"

    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    best_move = response[0]['generation']

    return {"best_move": best_move}

if __name__ == "__main__":
    fire.Fire(determine_best_move)



# Code Summary:
# Predicting Outcomes: As the language model updates its strategy, it enters a phase akin to a skilled gamer predicting the next turns in a complex 
# strategy game. It assesses three key elements akin to game dynamics:

# Choosing the Best Move (Policy): This mirrors a player selecting the optimal action in a game. The model determines the 'policy' - the best course 
# of action. For example, it might decide which key points to include in a summary, which sources to pull from in a search, the most engaging direction 
# for a creative piece, the most helpful answer in Q&A, or the most suitable code in a programming task.





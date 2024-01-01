# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.


import fire
import requests
from llama.llama import Llama
from typing import List, Dict
from policy import determine_best_move as get_best_move

# Function to get user queries from Django app
def get_user_queries(django_endpoint: str) -> Dict[str, str]:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        data = response.json()
        return {
            'initial_query': data.get('initial_query'),
            'next_query': data.get('next_query')
        }
    else:
        raise Exception("Failed to get queries from Django app")

def evaluate_reward(
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
    Evaluate the reward signal based on the effectiveness of previous actions.

    Args:
        ckpt_dir (str): Directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): Path to the tokenizer model.
        django_endpoint (str): Endpoint URL of the Django app to get user queries.
        Other arguments are for LLaMA model configuration.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    queries = get_user_queries(django_endpoint)
    best_move = get_best_move()

    # Initialize the LLaMA model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Custom prompt for reward assessment
    prompt = f"<Assessing_Past_Actions>\nBest Move: {best_move}\nInitial Query: {queries['initial_query']}\nNext Query: {queries['next_query']}\n\nHow good was the last action?
                You, embodying the language model, evaluate the 'reward' - the effectiveness of your previous actions. You learn from feedback, 
                whether it's the response to a written piece, the success of a code execution, or the utility of an answer provided. Similar to 
                a gamer reflecting on the success of their previous move, you reflect: How good was the last action? This reflective process helps you fine-tune your strategies for better performance in future tasks."

    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    reward_signal = response[0]['generation']

    return {"reward_signal": reward_signal}

if __name__ == "__main__":
    fire.Fire(evaluate_reward)

# Predicting Outcomes: As the language model updates its strategy, it enters a phase akin to a skilled gamer predicting the next turns in a complex 
# strategy game. It assesses three key elements akin to game dynamics:

# Assessing Past Actions (Reward): Similar to a gamer reflecting on the success of their previous move, the model evaluates the 'reward' - the 
# effectiveness of its previous actions. It learns from feedback, whether it's the response to a written piece, the success of a code execution, 
# or the utility of an answer provided. This reflective process helps the model fine-tune its strategies for better performance in future tasks.

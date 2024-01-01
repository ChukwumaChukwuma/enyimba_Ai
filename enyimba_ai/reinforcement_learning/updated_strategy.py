# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
import requests
from llama import Llama
from typing import Dict

# Importing the previous strategy
from hidden_strategy import generate_hidden_state_strategy

# Function to get user query from Django app
def get_chatbot_query(django_endpoint: str) -> str:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        return response.json().get('query')
    else:
        raise Exception("Failed to get query from Django chatbot app")

def update_rl_strategy(
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
    Update the Reinforcement Learning Strategy using the LLaMA model.

    Args:
        ckpt_dir (str): Directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): Path to the tokenizer model.
        django_endpoint (str): Endpoint URL of the Django app to get user queries.
        Other arguments are for LLaMA model configuration.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    user_query = get_chatbot_query(django_endpoint)
    hidden_state_strategy = generate_hidden_state_strategy(ckpt_dir, tokenizer_path, django_endpoint)

    # Initialize the LLaMA model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Custom prompt based on user query and hidden state strategy
    prompt = f"<Updating_the_Strategy>\nYou, acting as the language model, continuously refine your approach in this stage, akin to a chess player contemplating their next move. 
               With each new piece of information, question, or problem you encounter, you recalculate, asking yourself,—If I respond or proceed in this way, what outcome will I achieve?
               This dynamic thinking process is integral to your functionality, whether it's crafting an answer, generating creative content, optimizing a code solution, or collaborating on a writing task. Just as a chess player adapts their strategy with each move of their opponent, you adjust your internal strategy — your 'hidden state' — to better align with the evolving requirements of the task at hand. Your ongoing recalibration is crucial for delivering precise summaries, accurate search results, engaging writing, insightful Q&As, and efficient coding outputs. Now here is Current task: {user_query}. Here is the Previous strategy: {hidden_state_strategy}."

    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    updated_rl_strategy = response[0]['generation']

    return {"updated_rl_strategy": updated_rl_strategy}

if __name__ == "__main__":
    fire.Fire(update_rl_strategy)


# Code Summary:
    
# Updating the Strategy: In this stage, akin to a chess player contemplating their next move, the language model continuously refines its approach.
#
# With each new piece of information, question, or problem it encounters, the model recalculates, asking itself, "If I respond or proceed in this way, 
#
# what outcome will I achieve?" This dynamic thinking process is integral to its functionality, whether it's crafting an answer, generating creative 
#
# content, optimizing a code solution, or collaborating on a writing task. Just as a chess player adapts their strategy with each move of their opponent, 
#
# the language model adjusts its internal strategy — its 'hidden state' — to better align with the evolving requirements of the task at hand. This ongoing 
#
# recalibration is crucial for delivering precise summaries, accurate search results, engaging writing, insightful Q&As, and efficient coding outputs.

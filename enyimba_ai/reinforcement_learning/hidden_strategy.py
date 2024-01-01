# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
import requests
from llama.llama import Llama
from typing import List, Dict

# Function to get user query from Django app
def get_user_query(django_endpoint: str) -> str:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        return response.json().get('query')
    else:
        raise Exception("Failed to get query from Django app")

def generate_hidden_state_strategy(
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
    Generate the Hidden State Strategy using the LLaMA model.

    Args:
        ckpt_dir (str): Directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): Path to the tokenizer model.
        django_endpoint (str): Endpoint URL of the Django app to get user queries.
        Other arguments are for LLaMA model configuration.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    user_query = get_user_query(django_endpoint)

    # Initialize the LLaMA model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Custom prompt based on user query
    prompt = f"<Observation_Phase>\n{user_query}\n\n<Hidden_State_Strategy> <Observation_Phase>
             You begin by scanning the task at hand, just like a player observes a chessboard or a game screen. Whether you're understanding a question, identifying key elements in a text, or recognizing code structure, this is your initial assessment phase, akin to sizing up a game environment.
             <Hidden_State_Strategy>
             Following your observation, you formulate a 'hidden state,' similar to a player's internal strategy during a game. This is where you process your observations, drawing on your extensive training to predict the best course of action. Like a chess player contemplating their next move or a gamer devising a plan of attack, you organize your knowledge and experience to generate responses, write creatively, solve coding problems, and more."

    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    hidden_state_strategy = response[0]['generation']

    return {"hidden_state_strategy": hidden_state_strategy}

if __name__ == "__main__":
    fire.Fire(generate_hidden_state_strategy)

# Code Summary:
    
# Observation Phase: Just as a player observes a chessboard or a game screen, the language model begins by scanning the task at hand. 
# Whether it's understanding a question, identifying key elements in a text, or recognizing code structure, this is the model's initial 
# assessment phase, akin to sizing up a game environment.

# Hidden State Strategy: Following the observation, the model formulates a 'hidden state,' akin to a player's internal strategy during a game.
# This is where the model processes its observations, drawing on its extensive training to predict the best course of action. Like a chess 
# player contemplating their next move or a gamer devising a plan of attack, the model organizes its knowledge and experience to generate 
# responses, write creatively, solve coding problems, and more.


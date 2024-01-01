# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
import requests
from llama import Llama
from typing import Dict
from hidden_strategy import generate_hidden_state_strategy
from value import assess_value

# Function to get user query from Django app
def get_user_query(django_endpoint: str) -> str:
    response = requests.get(django_endpoint)
    if response.status_code == 200:
        return response.json().get('query')
    else:
        raise Exception("Failed to get query from Django app")

def generate_branches(
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
    Generate countless branches representing potential actions or decisions.
    Args as described.
    """
    django_endpoint = 'http://localhost:8000/get-user-query/'
    user_query = get_user_query(django_endpoint)

    # Call the functions to get strategies and values
    strategy_dict = generate_hidden_state_strategy(ckpt_dir, tokenizer_path, django_endpoint)
    strategy = strategy_dict["hidden_state_strategy"]
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
    prompt = f"<The_Investigation_Tree>\n{user_query}\n<Hidden_State_Strategy>{strategy}\n<Value_Assessment>{value}\n<The_Investigation_Tree>
                You, as the language model, visualize your tasks as a vast tree of countless branches, each representing a potential action or decision. In summarization, each branch is a key point; in search, a relevant source; in writing, a plot twist; in Q&A, an answer possibility; and in coding, a programming approach. Each branch holds statistics: frequency of use, effectiveness, predicted optimal choice, outcome quality, and the subsequent chain of events.
                <Three_Core_Investigative_Steps>
                Selection (The Detective's Pathfinding): Starting at the tree's base (the current task state), you ascend, selecting branches based on their stats. You balance well-trodden, successful paths (known strategies) with unexplored ones (novel approaches), like a detective pathfinding.
                Expansion (Exploring the Unknown): Upon reaching a novel branch (an unencountered scenario), you employ predictive capabilities (akin to a detective's intuition) to hypothesize potential outcomes, incorporating this new 'clue' into your tree.
                Backup (Refining Insights): After exploring a branch, you revisit and update the stats for each decision made, refining your strategy with newfound insights, much like a detective reassessing their leads.
                <Adapting_to_Varied_Cases>
                For straightforward tasks (like simple Q&A or basic coding), you assess outcomes in binary terms (correct/incorrect). For more complex tasks (like nuanced writing or advanced coding), you apply intricate criteria to evaluate the efficacy of each decision.
                <Modulating_for_Diverse_Magnitudes>
                When dealing with tasks varying in scope or complexity (like generating a short poem versus a detailed technical article), you adjust your evaluation scale, ensuring appropriate context sensitivity.
                Thus, you operate like a highly skilled detective, navigating through an intricate landscape of possibilities, learning from each step, and progressively enhancing your predictive prowess for a wide array of tasks."


    # Generate response
    response = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    branches_info = response[0]['generation']

    return {"branches": branches_info}

if __name__ == "__main__":
    fire.Fire(generate_branches)


# The Investigation Tree:
#
# Visualize the model's tasks as a vast tree of countless branches, each representing a potential action or decision. 
# In summarization, each branch could be a key point; in search, a relevant source; in writing, a plot twist; 
# in Q&A, an answer possibility; and in coding, a programming approach.
#
# Each branch holds statistics: frequency of use, effectiveness, predicted optimal choice, outcome quality, 
# and the subsequent chain of events.
#
# Three Core Investigative Steps:
#
# Selection (The Detective's Pathfinding): The model, like a detective, begins at the tree's base (the current task state) 
# and ascends, selecting branches based on their stats. It balances well-trodden, successful paths (known strategies) 
# with unexplored ones (novel approaches).
#
# Expansion (Exploring the Unknown): Reaching a novel branch (an unencountered scenario), the model employs its predictive 
# capabilities (akin to a detective's intuition) to hypothesize potential outcomes and incorporates this new 'clue' into its tree.
#
# Backup (Refining Insights): After delving into a branch, the model revisits and updates the stats for each decision made, 
# refining its strategy with newfound insights, much like a detective reassessing their leads.
#
# Adapting to Varied Cases:
#
# For straightforward tasks (like simple Q&A or basic coding), it assesses outcomes in binary terms (correct/incorrect).
# For complex tasks (like nuanced writing or advanced coding), it applies more intricate criteria to evaluate the efficacy 
# of each decision.
#
# Modulating for Diverse Magnitudes:
#
# When dealing with tasks varying greatly in scope or complexity (like generating a short poem versus a detailed technical article), 
# the model adjusts its evaluation scale, ensuring appropriate context sensitivity.
#
# Thus, the language model operates like a highly skilled detective, navigating through an intricate landscape of possibilities, 
# learning from each step, and progressively enhancing its predictive prowess for a wide array of tasks.

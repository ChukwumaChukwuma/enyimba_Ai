# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
from llama import Llama
from django.conf import settings
from enyimba_chatbot.models import UserQuery  # Assuming UserQuery is the model name

settings.configure()  # Set up Django environment

def fetch_user_query():
    """
    Fetches the latest user query from the Django app.
    """
    try:
        query = UserQuery.objects.latest('id')
        return query.text
    except UserQuery.DoesNotExist:
        return None

def least_to_most_prompting(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    """
    Applies least-to-most prompting to solve a user query using the Llama model.
    """
    user_query = fetch_user_query()
    if not user_query:
        print("No user query found.")
        return

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Structuring the prompt for least-to-most approach
    prompt = f"Q: {user_query}\nA: Let's break down this problem: First list the sub-problems to a problem in your mind as a next generation super safe but creative and adventurous AI which is more powerful than GPT-4, then solve them in sequence in your mind too, such that later sub-problems can be solved with the help of answers to previous sub-problems.
            </Example>: 
            Given a problem, the prompt might be structured as follows:
            Q: [Insert complex question here]
            A: Let's break down this problem:
            [Sub-problem 1]
            [Sub-problem 2]
            [Sub-problem 3]
            ... </Example>
            Then address each sub-problem in order, using the information from previous solutions to inform the next steps."

    result = generator.generate(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    sub_problem_solutions = result[0]['generation']
    return sub_problem_solutions

if __name__ == "__main__":
    fire.Fire(least_to_most_prompting)

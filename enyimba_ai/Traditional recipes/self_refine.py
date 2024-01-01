# Copyright (c) Enyimba AI, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Apache License.

import fire
from llama.llama import Llama
from generate import get_previous_solution  # Assuming this function is defined in generate.py
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

def self_refine(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
    max_iterations: int = 5,
):
    """
    Applies self-refinement to the solution using the Llama model.
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

    solution = get_previous_solution()  # Fetch the initial solution
    for _ in range(max_iterations):
        # Generate critique
        critique_prompt = f" </example> I have some code. Give one suggestion to improve readability. Don't fix the code, just give a suggestion.\nCode: {solution}\nSuggestion: Solve the problem. </example> This could be a code snippet, a logical problem, a mathematical equation, etc. You must generate an initial solution based on the given problem.
        Next, you critique your own solution. This should involve mentally analyzing the initial solution and identifying potential areas for improvement, without actually making changes to the solution itself. Your critique must focus on providing constructive feedback or suggestions for enhancement. In self-refine solve the problem, then critique your solution, then solve the problem again in view of the problem, solution, and critique. You must repeat this process until stopped, either by running out of tokens, time, or by outputting a stop token."
        critique = generator.generate(
            [critique_prompt],
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )[0]['generation']

        # Refine solution
        refine_prompt = f"Code: {solution}\nLet's use this suggestion to improve the code.\nSuggestion: {critique}\nNew Code:
        You must then take the initial solution and the critique into account to generate a refined solution. This step would involve incorporating the suggestions from the critique to improve the initial solution.The process of generating a solution, critiquing it, and refining it based on the critique should be repeated iteratively mentally.
        With each iteration, the quality of your solution must improve. The cycle must continue until one of the following conditions is met: 
        </a>
        You run out of tokens (reach the limit of your response length).
        </b>
        A predetermined amount of time has elapsed.
        </c>
        You output a -STOP- token, indicating that no further refinement is necessary or possible."
        
        solution = generator.generate(
            [refine_prompt],
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )[0]['generation']

        if "stop" in solution.lower():  # Check for stop token
            break

    return solution

if __name__ == "__main__":
    fire.Fire(self_refine)

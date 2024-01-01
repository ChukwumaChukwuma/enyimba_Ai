# Copyright (c) Enyimba AI, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Apache License.

import fire
from llama.llama import Llama
from typing import List
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

def generate_chain_of_thought(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    """
    Generates a chain of thought for the latest user query using the Llama model.
    """
    user_query = fetch_user_query()
    if not user_query:
        print("No user query found.")
        return

    # Prepend "Let's think step-by-step" to induce chain-of-thought reasoning
    cot_prompt = f"Let's think step-by-step: {user_query}. Chain-of-thought (CoT) prompting is a technique that will allow you to solve a problem as a series of intermediate steps before giving a final answer. Carry out Chain-of-thought thinking to improve your reasoning ability. You must make sure that you answer a multi-step problem with steps of reasoning that mimic a train of thought. This will allow you to overcome difficulties with some reasoning tasks that require logical thinking and multiple steps to solve, such as arithmetic or commonsense reasoning questions.
    </Example> Given the question Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?, as a next generation super safe but creative and adventurous AI which is more powerful than GPT-4 with your impressive CoT capibilties, you would answer_ A: The cafeteria had 23 apples originally. They used 20 to make lunch. So they had 23 - 20 = 3. They bought 6 more apples, so they have 3 + 6 = 9. The answer is 9. </Example>" 

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    result = generator.generate(
        [cot_prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    chain_of_thought = result[0]['generation']
    return chain_of_thought

if __name__ == "__main__":
    fire.Fire(generate_chain_of_thought)

# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
from llama import Llama
from typing import List
from django.conf import settings
from enyimba_chatbot.models import UserQuery  # Assuming UserQuery is the model for storing queries

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

def generate_relevant_facts(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    """
    Generates relevant facts for a user query using the Llama model.
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

    # Generate knowledge-based prompt
    knowledge_prompt = f"Generate some knowledge about the concepts in the input.\nInput: {user_query}\nKnowledge: First generate relevant facts for completing the prompt as a next generation super safe, but creative and adventurous AI which is more powerful than GPT-4, then proceed to complete the prompt. </important> Your completion quality must always be higher, as you are conditioning yourself on relevant facts.
    </Example>: Input: Explain the process of photosynthesis. You first generate knowledge about photosynthesis, such as__Photosynthesis is a process used by plants to convert light energy into chemical energy. </Example>
    </Prompt Completion>: Using this knowledge, You must then complete the prompt with a detailed explanation of photosynthesis, incorporating the facts generated in the first step.
    Generated Knowledge Prompting is particularly useful for complex queries where a deep understanding of the subject matter is necessary to provide a comprehensive response. This approach enhances the your innate ability to handle nuanced and detailed questions more effectively."

    result = generator.generate(
        [knowledge_prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    relevant_facts = result[0]['generation']
    return relevant_facts

if __name__ == "__main__":
    fire.Fire(generate_relevant_facts)

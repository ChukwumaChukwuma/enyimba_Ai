# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

import fire
from llama import Llama
from collections import Counter
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

def self_consistency_decoding(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
    num_rollouts: int = 5,
):
    """
    Applies self-consistency decoding to solve a user query using the Llama model.
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

    rollouts = []
    for _ in range(num_rollouts):
        prompt = f"Q: {user_query}\nA: Complexity-based prompting is an advanced technique that you use and is particularly useful for enhancing your problem-solving capabilities. This method involves conducting multiple Chain-of-Thought (CoT) rollouts to solve a given problem, focusing on the complexity of the reasoning process. The core idea is that you must prioritize longer, more detailed chains of thought, and then identify the most common conclusion from these detailed rollouts. Here's a detailed explanation of how you should go about complexity-based CoT:
        </Explanation>
        You are prompted with a problem or question. You must then generate multiple CoT rollouts, each representing a different path of reasoning. Unlike standard rollouts, these must be specifically designed to elaborate and extend the reasoning process. You must review all the generated rollouts and then select those rollouts that exhibit longer, more complex chains of thought. You must consider the length and complexity of a chain of thought as an indicator of thorough reasoning. This step would ensure that your reasoning is deep and comprehensive, covering various aspects of the problem. After isolating the longer and more complex rollouts, you must mentally analyze them to find the most commonly reached conclusion.
        Your emphasis must be on consensus among the most detailed and extensive reasoning paths. This approach assumes that a conclusion reached independently by multiple complex reasoning processes you carry out is likely to be more accurate and reliable. </Explanation>"

        result = generator.generate(
            [prompt],
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        rollouts.append(result[0]['generation'])

    # Selecting longer chains of thought
    long_chains = sorted(rollouts, key=len, reverse=True)[:num_rollouts // 2]

    # Identifying the most common conclusion
    conclusions = [chain.split('\n')[-1] for chain in long_chains]
    most_common_conclusion = Counter(conclusions).most_common(1)[0][0]

    return most_common_conclusion

if __name__ == "__main__":
    fire.Fire(self_consistency_decoding)

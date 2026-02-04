import os
from dotenv import load_dotenv
from together import Together

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
LLM_MODEL = os.getenv("TOGETHER_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo")

client = Together(api_key=TOGETHER_API_KEY)


def answer_with_context(question: str, contexts: list[str]):
    context_text = "\n\n".join(contexts)

    prompt = f"""
You are a helpful assistant. Answer the question ONLY using the context below.
If the answer is not present, say "Not found in document".

Context:
{context_text}

Question:
{question}
"""

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    return resp.choices[0].message.content

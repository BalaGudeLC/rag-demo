import os
import time
from dotenv import load_dotenv
from together import Together

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMBED_MODEL = os.getenv("TOGETHER_EMBED_MODEL", "BAAI/bge-base-en-v1.5")

client = Together(api_key=TOGETHER_API_KEY)


def get_embedding(text: str):
    last_err = None

    for attempt in range(5):
        try:
            resp = client.embeddings.create(
                model=EMBED_MODEL,
                input=[text]
            )
            return resp.data[0].embedding

        except Exception as e:
            last_err = e
            wait = attempt + 1
            print(f"[WARN] Embedding failed (attempt {attempt+1}/5). Retrying in {wait}s. Error: {e}")
            time.sleep(wait)

    raise last_err

import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = os.getenv("QDRANT_COLLECTION", "terms_demo")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def init_collection(vector_size: int):
    if not client.collection_exists(COLLECTION):
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        print(f"[INFO] Created collection: {COLLECTION}")


def store_chunk(text: str, vector: list):
    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": text},
            )
        ],
    )


def search_similar(query_vector: list, limit: int = 3):
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=limit,
        with_payload=True,
    ).points

    return [
        {
            "score": r.score,
            "text": r.payload.get("text", "")
        }
        for r in results
    ]

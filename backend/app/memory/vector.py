from app.memory.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FaissStore


class VectorMemory:

    def __init__(self):
        self.embedder = EmbeddingModel()
        self.store = FaissStore()

    def add_memory(
        self,
        text: str,
        role: str = "user",
    ):

        vector = self.embedder.encode(text)

        self.store.add(
            vector,
            {
                "text": text,
                "role": role,
            },
        )

    def search(
        self,
        query: str,
        k: int = 5,
    ):

        vector = self.embedder.encode(query)

        return self.store.search(
            vector,
            k,
        )

    def clear(self):
        self.store.clear()

    def count(self):
        return self.store.count()
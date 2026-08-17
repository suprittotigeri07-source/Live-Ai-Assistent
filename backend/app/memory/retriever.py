from app.memory.vector import VectorMemory


class MemoryRetriever:

    def __init__(self):
        self.memory = VectorMemory()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        results = self.memory.search(
            query,
            k,
        )

        memories = []

        for item in results:

            metadata = item["metadata"]

            memories.append(
                metadata["text"]
            )

        return memories
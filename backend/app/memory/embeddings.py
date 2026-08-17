from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

    def encode(self, text: str):
        return self.model.encode(
            text,
            convert_to_numpy=True
        )
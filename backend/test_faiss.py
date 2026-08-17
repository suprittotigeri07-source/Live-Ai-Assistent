from app.memory.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FaissStore

embedder = EmbeddingModel()

store = FaissStore()

store.add(
    embedder.encode("My name is Suprit."),
    "My name is Suprit."
)

store.add(
    embedder.encode("I am building an AI Assistant."),
    "I am building an AI Assistant."
)

store.add(
    embedder.encode("I like PostgreSQL."),
    "I like PostgreSQL."
)

query = embedder.encode("Who am I?")

results = store.search(query)

print(results)
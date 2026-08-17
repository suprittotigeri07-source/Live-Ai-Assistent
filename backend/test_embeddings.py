from app.memory.embeddings import EmbeddingModel

model = EmbeddingModel()

vector = model.encode("Hello World")

print(type(vector))
print(len(vector))
print(vector[:10])
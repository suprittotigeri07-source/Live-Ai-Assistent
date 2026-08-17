import os
import pickle
import faiss
import numpy as np


class FaissStore:
    """
    FAISS Vector Store
    Stores embeddings and their metadata.
    """

    INDEX_DIR = "app/vectorstore/index"
    INDEX_FILE = os.path.join(INDEX_DIR, "memory.index")
    METADATA_FILE = os.path.join(INDEX_DIR, "metadata.pkl")

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

        os.makedirs(self.INDEX_DIR, exist_ok=True)

        self._load_or_create()

    def _load_or_create(self):
        """
        Load an existing FAISS index.
        If it doesn't exist or is corrupted, create a new one.
        """

        try:
            if (
                os.path.exists(self.INDEX_FILE)
                and os.path.exists(self.METADATA_FILE)
            ):
                self.index = faiss.read_index(self.INDEX_FILE)

                with open(self.METADATA_FILE, "rb") as f:
                    self.metadata = pickle.load(f)

                print(
                    f"Loaded FAISS index ({self.index.ntotal} vectors)"
                )

            else:
                raise FileNotFoundError

        except Exception as e:
            print(f"Creating new FAISS index ({e})")

            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

            self.save()

    def add(self, vector, metadata):
        """
        Add a vector and its metadata.
        """

        vector = np.asarray(vector, dtype=np.float32).reshape(1, -1)

        self.index.add(vector)

        self.metadata.append(metadata)

        self.save()

    def search(self, vector, k: int = 5):
        """
        Search for the k nearest vectors.
        Returns metadata and similarity distance.
        """

        if self.index.ntotal == 0:
            return []

        vector = np.asarray(vector, dtype=np.float32).reshape(1, -1)

        k = min(k, self.index.ntotal)

        distances, indices = self.index.search(vector, k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            results.append(
                {
                    "distance": float(distance),
                    "metadata": self.metadata[idx],
                }
            )

        return results

    def save(self):
        """
        Save FAISS index and metadata.
        """

        faiss.write_index(
            self.index,
            self.INDEX_FILE,
        )

        with open(self.METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def clear(self):
        """
        Delete all stored vectors.
        """

        self.index = faiss.IndexFlatL2(self.dimension)

        self.metadata = []

        self.save()

    def count(self):
        """
        Number of stored vectors.
        """

        return self.index.ntotal
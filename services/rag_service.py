import os

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DB_PATH


class RAGService:

    def __init__(self):

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        self.collection = self.client.get_or_create_collection(
            name="meeting_history"
        )

        if self.collection.count() == 0:
            self._load_sample_meetings()

    def _load_sample_meetings(self):

        folder = "sample_data"

        for index, file_name in enumerate(os.listdir(folder)):

            path = os.path.join(folder, file_name)

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            embedding = self.embedding_model.encode(text).tolist()

            self.collection.add(
                ids=[str(index)],
                documents=[text],
                embeddings=[embedding]
            )

    def retrieve_context(self, transcript):

        embedding = self.embedding_model.encode(transcript).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )

        if results["documents"] and len(results["documents"][0]) > 0:
            return results["documents"][0][0]

        return ""
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text):
        return self.model.encode(text)

    def generate_embeddings(self, texts):
        return self.model.encode(texts)

    def build_user_vector(self, skills):
        embeddings = self.generate_embeddings(skills)

        user_vector = np.mean(embeddings, axis=0)

        return user_vector
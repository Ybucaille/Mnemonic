from typing import List
from sentence_transformers import SentenceTransformer

class LocalEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> List[float]:
        if not text.strip():
            return []
        return self.model.encode(text, convert_to_numpy=False).tolist()
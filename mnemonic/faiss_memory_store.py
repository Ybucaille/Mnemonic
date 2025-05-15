import os
import json
import uuid
import faiss
import numpy as np
from datetime import datetime
from typing import List, Optional
from mnemonic.memory_interface import BaseMemoryStore

class FaissMemoryStore(BaseMemoryStore):
    def __init__(self, memory_path: str, index_path: str, embedder):
        self.memory_path = memory_path
        self.index_path = index_path
        self.embedder = embedder

        os.makedirs(os.path.dirname(memory_path), exist_ok=True)

        self.memories = self._load_memories()
        self.id_map = []
        self.index = None

        self._rebuild_index()
        self._save_index()

    def _load_memories(self) -> List[dict]:
        if not os.path.exists(self.memory_path):
            return []
        with open(self.memory_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def _save_memories(self):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            for m in self.memories:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def _load_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        else:
            dim = len(self.memories[0]["embedding"]) if self.memories else 384
            return faiss.IndexFlatL2(dim)

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)

    def add(self, input: str, output: str, source: str = "unknown", tags: Optional[List[str]] = None, metadata: Optional[dict] = None) -> str:
        memory_id = str(uuid.uuid4())
        text = (input + " " + output).strip()
        embedding = self.embedder.encode(text)

        memory = {
            "id": memory_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input": input,
            "output": output,
            "source": source,
            "tags": tags or [],
            "metadata": metadata or {},
            "embedding": embedding
        }

        self.memories.append(memory)
        self.id_map.append(memory_id)
        self.index.add(np.array([embedding]).astype("float32"))
        self._save_memories()
        self._save_index()

        return memory_id

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        if len(self.memories) == 0 or self.index.ntotal == 0:
            return []

        query_vec = self.embedder.encode(query)
        query_np = np.array([query_vec]).astype("float32")

        top_k = min(top_k, len(self.id_map))

        distances, indices = self.index.search(query_np, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.id_map):
                mem_id = self.id_map[idx]
                match = next((m for m in self.memories if m["id"] == mem_id), None)
                if match:
                    results.append(match)
        return results

    def get(self, memory_id: str) -> Optional[dict]:
        return next((m for m in self.memories if m["id"] == memory_id), None)

    def delete(self, memory_id: str) -> bool:
        if memory_id not in self.id_map:
            return False
        idx = self.id_map.index(memory_id)

        self.memories = [m for m in self.memories if m["id"] != memory_id]
        self.id_map.pop(idx)

        embeddings = [m["embedding"] for m in self.memories if "embedding" in m]
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings).astype("float32"))

        self._save_memories()
        self._save_index()
        return True

    def get_all(self) -> List[dict]:
        return self.memories

    def _rebuild_index(self):
        embeddings = []
        self.id_map = []

        for m in self.memories:
            if "embedding" in m:
                self.id_map.append(m["id"])
                embeddings.append(m["embedding"])

        if embeddings:
            dim = len(embeddings[0])
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(np.array(embeddings).astype("float32"))
        else:
            self.index = faiss.IndexFlatL2(384)

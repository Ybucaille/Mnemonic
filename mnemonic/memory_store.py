import json
import uuid
import os
from datetime import datetime
from typing import List, Optional
import numpy as np
from mnemonic.memory_interface import BaseMemoryStore

class JsonMemoryStore(BaseMemoryStore):
    def __init__(self, filepath: str, embedder):
        self.filepath = filepath
        self.embedder = embedder
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                pass  # Fichier vide

    def _load_memories(self) -> List[dict]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def _write_memory(self, memory: dict):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(memory, ensure_ascii=False) + "\n")

    def add(self, input: str, output: str, source: str = "unknown", tags: Optional[List[str]] = None, metadata: Optional[dict] = None) -> str:
        memory_id = str(uuid.uuid4())
        text_to_embed = (input + " " + output).strip()
        embedding = self.embedder.encode(text_to_embed)

        memory = {
            "id": memory_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input": input,
            "output": output,
            "source": source,
            "tags": tags or [],
            "metadata": metadata or {},
            "embedding": embedding,
        }
        self._write_memory(memory)
        return memory_id

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        a = np.array(a)
        b = np.array(b)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        query_embedding = self.embedder.encode(query)
        memories = self._load_memories()

        scored = []
        for memory in memories:
            mem_embedding = memory.get("embedding")

            if mem_embedding is None:
                text = (memory.get("input", "") + " " + memory.get("output", "")).strip()
                if not text:
                    continue
                mem_embedding = self.embedder.encode(text)

            score = self._cosine_similarity(query_embedding, mem_embedding)
            scored.append((memory, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [m for m, score in scored[:top_k] if score > 0]

    def _score_memory(self, memory: dict, query: str) -> float:
        text = (memory.get("input", "") + " " + memory.get("output", "")).lower()
        return sum(word in text for word in query.lower().split())

    def get(self, memory_id: str) -> Optional[dict]:
        for m in self._load_memories():
            if m["id"] == memory_id:
                return m
        return None

    def delete(self, memory_id: str) -> bool:
        memories = self._load_memories()
        updated = [m for m in memories if m["id"] != memory_id]
        if len(updated) == len(memories):
            return False  # Rien supprimé
        with open(self.filepath, "w", encoding="utf-8") as f:
            for m in updated:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")
        return True

    def get_all(self) -> List[dict]:
        return self._load_memories()

    def migrate_embeddings(self):
        memories = self._load_memories()
        updated = []
        changed = False

        for m in memories:
            if "embedding" not in m:
                text = (m.get("input", "") + " " + m.get("output", "")).strip()
                if text:
                    m["embedding"] = self.embedder.encode(text)
                    changed = True
            updated.append(m)

        if changed:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for m in updated:
                    f.write(json.dumps(m, ensure_ascii=False) + "\n")
            print("✅ Migration des embeddings terminée.")
        else:
            print("⚠️  Tous les souvenirs avaient déjà un embedding.")

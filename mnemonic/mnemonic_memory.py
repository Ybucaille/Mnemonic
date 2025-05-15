from mnemonic.memory_store import JsonMemoryStore
from mnemonic.faiss_memory_store import FaissMemoryStore
from mnemonic.embedding_model import LocalEmbedder
from mnemonic.utils import filter_by_tags, filter_by_date

class MnemonicMemory:
    def __init__(self, backend: str = "auto", threshold: int = 10000):
        self.embedder = LocalEmbedder()

        if backend == "json":
            self.memory = JsonMemoryStore("data/memory.jsonl", self.embedder)

        elif backend == "faiss":
            self.memory = FaissMemoryStore("data/memory.jsonl", "data/index.faiss", self.embedder)

        elif backend == "auto":
            # Compte les souvenirs actuels et choisit
            temp = JsonMemoryStore("data/memory.jsonl", self.embedder)
            nb_memories = len(temp.get_all())
            if nb_memories < threshold:
                self.memory = temp
            else:
                self.memory = FaissMemoryStore("data/memory.jsonl", "data/index.faiss", self.embedder)

        else:
            raise ValueError(f"Backend inconnu : {backend}")

    def add(self, *args, **kwargs):
        return self.memory.add(*args, **kwargs)

    def search(self, query: str, top_k: int = 5, tags=None, after=None, before=None):
        results = self.memory.search(query, top_k=top_k)

        if tags:
            results = filter_by_tags(results, tags)
        if after or before:
            results = filter_by_date(results, after=after, before=before)

        return results

    def get(self, *args, **kwargs):
        return self.memory.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.memory.delete(*args, **kwargs)

    def get_all(self, tags=None, after=None, before=None):
        memories = self.memory.get_all()

        if tags:
            memories = filter_by_tags(memories, tags)
        if after or before:
            memories = filter_by_date(memories, after=after, before=before)

        return memories

from abc import ABC, abstractmethod
from typing import List, Optional

class BaseMemoryStore(ABC):
    @abstractmethod
    def add(self, input: str, output: str, source: str = "unknown", tags: Optional[List[str]] = None, metadata: Optional[dict] = None) -> str:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        pass

    @abstractmethod
    def get(self, memory_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> List[dict]:
        pass

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from core import MnemonicMemory

app = FastAPI()
memory = MnemonicMemory()

class MemoryInput(BaseModel):
    input: str
    output: str
    tags: Optional[List[str]] = []
    source: Optional[str] = "unknown"
    metadata: Optional[dict] = {}

@app.post("/memory/add")
def add_memory(data: MemoryInput):
    memory.add(
        input=data.input,
        output=data.output,
        tags=data.tags,
        source=data.source,
        metadata=data.metadata
    )
    return {"status": "ok"}

@app.delete("/memory/delete")
def delete_memory(id: str):
    success = memory.delete(id)
    return {"deleted": success}

@app.get("/memory/search")
def search_memory(query: str, top_k: int = 5, tags: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None):
    tag_list = tags.split(",") if tags else None
    results = memory.search(query=query, top_k=top_k, tags=tag_list, after=after, before=before)
    return results

@app.get("/memory/all")
def get_all_memories(tags: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None):
    tag_list = tags.split(",") if tags else None
    return memory.get_all(tags=tag_list, after=after, before=before)
from datetime import datetime
from typing import List, Optional

def filter_by_tags(memories: List[dict], required_tags: List[str]) -> List[dict]:
    return [m for m in memories if all(tag in m.get("tags", []) for tag in required_tags)]


def filter_by_date(memories: List[dict], after: Optional[str] = None, before: Optional[str] = None) -> List[dict]:
    def in_range(timestamp: str) -> bool:
        try:
            date = datetime.fromisoformat(timestamp)
        except Exception:
            return False
        if after and date < datetime.fromisoformat(after):
            return False
        if before and date > datetime.fromisoformat(before):
            return False
        return True

    return [m for m in memories if in_range(m.get("timestamp", ""))]

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class News:
    title: str
    url: str
    source: str
    created_at: datetime
    author: Optional[str] = None
    body: Optional[str] = None
    abstract: Optional[str] = None  # arXiv 논문용 
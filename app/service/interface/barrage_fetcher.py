from abc import ABC, abstractmethod
from typing import List, TypedDict

class BarrageField(TypedDict):
    content: str
    offset: int
    style: str
    weight: int

class BarrageFetcher(ABC):
    @abstractmethod
    async def fetch_all(self, duration: int, vid: str, filter: bool) -> List[BarrageField]:
        pass

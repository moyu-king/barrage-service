from abc import ABC, abstractmethod
from typing import List, TypedDict

class EpisodeField(TypedDict):
    vid: str
    union_title: str
    title: str
    duration: int
    season: str

class EpisodeFetcher(ABC):
    @abstractmethod
    async def fetch_all() -> List[EpisodeField]:
        pass

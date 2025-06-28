from abc import ABC, abstractmethod

class BarrageFetcher(ABC):
    @abstractmethod
    async def fetch_all():
        pass

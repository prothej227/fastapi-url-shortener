from abc import ABC, abstractmethod
class ShorteningStrategy(ABC):
    @abstractmethod
    def shorten_url(self, original_url: str, code_length: int = 6) -> str:
        pass
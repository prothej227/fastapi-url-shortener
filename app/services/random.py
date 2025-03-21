from app.services.shortening import ShorteningStrategy
import random
import string

class RandomStrategy(ShorteningStrategy):
    def shorten_url(self, original_url: str, code_length: int = 6) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=code_length))
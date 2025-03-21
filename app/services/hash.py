from app.services.shortening import ShorteningStrategy
import hashlib

class HashStrategy(ShorteningStrategy):
    def shorten_url(self, original_url: str, code_length = 6) -> str:
        hash_code = hashlib.md5(original_url.encode()).hexdigest()[:code_length]
        return hash_code
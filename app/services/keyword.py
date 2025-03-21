from app.services.shortening import ShorteningStrategy

class KeywordBasedStrategy(ShorteningStrategy):
    def shorten_url(self, original_url: str) -> str:
        keywords = original_url.split("/")[-1].split("-")
        return "".join(word[:3] for word in keywords if word)[:6]
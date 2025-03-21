from app.services.shortening import ShorteningStrategy

class CustomAliasStrategy(ShorteningStrategy):
    def shorten_url(self, custom_code: str) -> str:
        if not custom_code:
            raise ValueError("Custom code cannot be NULL.")
        return custom_code
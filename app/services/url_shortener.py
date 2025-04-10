from app.repositories.url_repository import UrlRepository
from app.services.shortening import ShorteningStrategy
from app.services.custom import CustomAliasStrategy
from app.services.keyword import KeywordBasedStrategy
from app.models import Url, User
from typing import Optional

class UrlShortener:
    def __init__(self, repo: UrlRepository, strategy: ShorteningStrategy, code_length: int = 6):
        self.repo = repo
        self.strategy = strategy
        self.code_length = code_length
        
    def shorten_url(self, original_url: str, user: User, custom_code: str = None) -> Optional[str]:
        """  Returns the shortened url """
        if isinstance(self.strategy, CustomAliasStrategy) and custom_code:
            short_code = self.strategy.shorten_url(custom_code)
        elif isinstance(self.strategy, KeywordBasedStrategy):
            short_code = self.strategy.shorten_url(original_url)
        else:
            short_code = self.strategy.shorten_url(original_url, self.code_length)
        # Check if unique, otherwise rerun
        while not self.repo.is_unique_short_code(short_code):
            short_code = self.strategy.shorten_url(original_url, custom_code)
        # Persistence
        exec_persistence = self.repo.save_short_url(original_url, short_code, user)
        if not exec_persistence:
            return None
        return short_code

    def expand_url(self, short_code: str) -> str:
        """ Returns the original url """
        return self.repo.get_original_url(short_code)
    
    def track_url_access(self, short_code: str, ip_address: str, user_agent: str) -> None:
        """ Log details for analytics use """
        self.repo.log_access(short_code, ip_address, user_agent)
    
    def delete_short_code(self, short_code: str) -> bool:
        """ Delete a short code """
        return self.repo.delete_short_url(short_code)

    def get_url_record(self, short_code: str) -> Url | None:
        return self.repo.get_url_record(short_code)
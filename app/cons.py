from app.services.custom import CustomAliasStrategy
from app.services.hash import HashStrategy
from app.services.random import RandomStrategy
from app.services.keyword import KeywordBasedStrategy

STRATEGY_MAP = {
    "random": RandomStrategy(),
    "hash": HashStrategy(),
    "custom": CustomAliasStrategy(),
    "keyword": KeywordBasedStrategy()
}
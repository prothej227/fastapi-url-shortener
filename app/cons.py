from app.services.custom import CustomAliasStrategy
from app.services.hash import HashStrategy
from app.services.random import RandomStrategy
from app.services.keyword import KeywordBasedStrategy
from enum import Enum

class StrategyType(Enum):
    RANDOM = "random"
    HASH = "hash"
    CUSTOM = "custom"
    KEYWORD = "keyword"

STRATEGY_MAP = {
    StrategyType.RANDOM: RandomStrategy(),
    StrategyType.HASH: HashStrategy(),
    StrategyType.CUSTOM: CustomAliasStrategy(),
    StrategyType.KEYWORD: KeywordBasedStrategy()
}
"""麻雀AIの行動決定戦略を定義するモジュール。"""

from .base_strategy import BaseStrategy
from .rule_based import RuleBasedStrategy

__all__ = ["BaseStrategy", "RuleBasedStrategy"]

"""麻雀AIの行動決定戦略を定義するモジュール。"""  # パッケージdocstringを追加

from .base_strategy import BaseStrategy
from .rule_based.rule_based_strategy import RuleBasedStrategy

__all__ = ["BaseStrategy", "RuleBasedStrategy"]

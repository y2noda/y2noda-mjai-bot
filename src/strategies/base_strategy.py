from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bot import MahjongAIBot  # 絶対インポートを使用


class BaseStrategy(ABC):
    """戦略の基底クラス。"""

    @abstractmethod
    def decide_action(self, bot: "MahjongAIBot") -> str:
        """与えられたボットの状態に基づいて、実行すべきアクションを決定します。

        Args:
            bot (MahjongAIBot): 現在のボットの状態。

        Returns:
            str: mjaiプロトコルに従ったアクション文字列。

        """
        raise NotImplementedError

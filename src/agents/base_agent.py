from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.game_state = {}

    @abstractmethod
    def think(self) -> str:
        """
        現在の状態から次のアクションを決定する
        Returns:
            str: 選択されたアクション
        """
        pass

    def update_state(self, state: Dict[str, Any]) -> None:
        """
        ゲーム状態を更新する
        Args:
            state: 新しいゲーム状態
        """
        self.game_state = state

    @property
    def can_tsumo_agari(self) -> bool:
        """ツモ和了可能かどうか"""
        # TODO: 実装
        return False

    @property
    def can_ron_agari(self) -> bool:
        """ロン和了可能かどうか"""
        # TODO: 実装
        return False

    @property
    def can_riichi(self) -> bool:
        """リーチ可能かどうか"""
        # TODO: 実装
        return False

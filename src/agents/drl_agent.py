from typing import Any, Dict

import numpy as np

from ..models.network import DRLNetwork
from .base_agent import BaseAgent


class DRLAgent(BaseAgent):
    def __init__(self, player_id: int, model_path: str = None):
        super().__init__(player_id)
        self.network = DRLNetwork()
        if model_path:
            self.network.load(model_path)

    def think(self) -> str:
        """
        深層強化学習モデルを使用して次のアクションを決定する
        Returns:
            str: 選択されたアクション
        """
        # 状態を特徴量に変換
        state_features = self._extract_features()

        # モデルで行動を予測
        action_probs = self.network.predict(state_features)

        # 行動を選択（ε-greedy等の方策を実装可能）
        action = self._select_action(action_probs)

        return action

    def _extract_features(self) -> np.ndarray:
        """
        現在の状態から特徴量を抽出する
        Returns:
            np.ndarray: 特徴量ベクトル
        """
        # TODO: 特徴量抽出の実装
        return np.array([])

    def _select_action(self, action_probs: np.ndarray) -> str:
        """
        行動確率から実際の行動を選択する
        Args:
            action_probs: 各行動の確率
        Returns:
            str: 選択された行動
        """
        # TODO: 行動選択の実装（ε-greedy等）
        return "pass"  # 仮の実装

import os
from typing import List, Tuple

import torch
import torch.optim as optim

from ..models.network import DRLNetwork


class DRLTrainer:
    def __init__(
        self,
        model: DRLNetwork,
        learning_rate: float = 1e-4,
        gamma: float = 0.99,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
    ):
        self.model = model.to(device)
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.gamma = gamma
        self.device = device

    def update(self, transitions: List[Tuple]) -> float:
        """
        バッチデータを使用してモデルを更新
        Args:
            transitions: (state, action, reward, next_state, done)のタプルのリスト
        Returns:
            float: 損失値
        """
        states, actions, rewards, next_states, dones = zip(*transitions)

        # テンソルに変換
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        # Q値の計算
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.model(next_states).max(1)[0].detach()
        expected_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        # 損失の計算と最適化
        loss = torch.nn.functional.smooth_l1_loss(
            current_q_values.squeeze(), expected_q_values
        )

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def save_checkpoint(
        self, path: str, episode: int, optimizer_state: dict = None
    ) -> None:
        """
        チェックポイントの保存
        Args:
            path: 保存先のパス
            episode: エピソード数
            optimizer_state: オプティマイザの状態
        """
        checkpoint = {
            "episode": episode,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": (
                self.optimizer.state_dict()
                if optimizer_state is None
                else optimizer_state
            ),
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(checkpoint, path)

    def load_checkpoint(self, path: str) -> int:
        """
        チェックポイントの読み込み
        Args:
            path: チェックポイントファイルのパス
        Returns:
            int: 読み込んだエピソード数
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        return checkpoint["episode"]

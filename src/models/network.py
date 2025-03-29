import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class DRLNetwork(nn.Module):
    def __init__(
        self, input_dim: int = 1000, hidden_dim: int = 512, output_dim: int = 100
    ):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        ネットワークの順伝播
        Args:
            x: 入力テンソル
        Returns:
            torch.Tensor: 行動確率
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=-1)
        return x

    def predict(self, state: np.ndarray) -> np.ndarray:
        """
        状態から行動確率を予測
        Args:
            state: 状態の特徴量
        Returns:
            np.ndarray: 行動確率
        """
        with torch.no_grad():
            x = torch.FloatTensor(state)
            out = self.forward(x)
            return out.numpy()

    def save(self, path: str) -> None:
        """
        モデルの保存
        Args:
            path: 保存先のパス
        """
        torch.save(self.state_dict(), path)

    def load(self, path: str) -> None:
        """
        モデルの読み込み
        Args:
            path: モデルファイルのパス
        """
        self.load_state_dict(torch.load(path))

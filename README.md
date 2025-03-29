# y2noda-mjai-bot

麻雀AIボットのPython実装です。[mjai](https://github.com/mjx-project/mjai)プロトコルに準拠しています。

## 概要

このプロジェクトは、以下の機能を提供します：

- ルールベースの麻雀AI実装
- シミュレーション機能
- mjaiプロトコルとの互換性

## 必要条件

- Python 3.12以上
- uv（高速なPythonパッケージマネージャー）

## セットアップ手順

1. uvのインストール
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. リポジトリのクローン
```bash
git clone [repository-url]
cd y2noda-mjai-bot
```

3. 環境のセットアップ
```bash
uv sync
```

4. 仮想環境の有効化
```bash
source .venv/bin/activate  # Unix/macOS
# または
.venv\Scripts\activate  # Windows（未検証）
```

## 主要な依存パッケージ

- mjai >= 0.2.1: 麻雀AIのインターフェース
- numpy >= 2.2.3: 数値計算ライブラリ
- torch >= 2.6.0: 機械学習フレームワーク

## 使用方法

### シミュレーションの実行

```bash
uv run python scripts/simulate.py
```

### ユーティリティスクリプト

#### 提出用ZIPファイルの作成

```bash
uv run python scripts/create_submission.py
```

このスクリプトは、大会提出用のZIPファイル（`submission.zip`）を作成します。ZIPファイルには以下のファイルが含まれます：
- `bot.py`: メインのボットの実装

## プロジェクト構造

```
.
├── bot.py          # メインのボットの実装
├── simulate.py     # シミュレーション用スクリプト
├── src/            # ソースコード
├── scripts/        # ユーティリティスクリプト
├── examples/       # 使用例
├── logs/           # ログファイル
└── terraform/      # インフラストラクチャコード
```

## ライセンス

このプロジェクトのライセンスについては、リポジトリのルートディレクトリにあるLICENSEファイルを参照してください。

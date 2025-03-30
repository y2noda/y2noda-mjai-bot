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

#### 対話型シェルでデバッグする

自動でボットを実行するには、以下のコマンドを実行します。
```bash
./run_bot.sh
```

対話的に実行するには、以下のコマンドを実行します。
```bash
./run_bot.sh -i
```

ゲームをスタートするには、
```bash
[{"type":"start_game","id":0}]
```
というメッセージを送信します。

局を進めるには、
```bash
[{"type":"start_kyoku","bakaze":"E","dora_marker":"2s","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"scores":[25000,25000,25000,25000],"tehais":[["E","6p","9m","8m","C","2s","7m","S","6m","1m","S","3s","8m"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"]]},{"type":"tsumo","actor":0,"pai":"1m"}]
```
のようなメッセージを送信します。









このスクリプトは、対話型シェルでデバッグするためのものです。

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

### srcの詳細

srcディレクトリの中身は以下のようになっています。

```
.
├── src/
│   ├── __init__.py
│   ├── bot.py              # MahjongAIBotクラス (Mjaiとのインターフェース)
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── thinking_engine.py  # ThinkingEngineクラス (戦略の選択と実行)
│   │   └── interfaces.py     # IThinkingStrategyのような戦略インターフェース定義 (任意)
│   ├── strategies/         # 各思考戦略の実装
│   │   ├── __init__.py
│   │   ├── base_strategy.py  # 戦略の基底クラスや共通インターフェース
│   │   ├── rule_based/       # ルールベース戦略関連
│   │   │   ├── __init__.py
│   │   │   └── rule_based_strategy.py
│   │   ├── ml_based/         # (将来用) MLベース戦略関連
│   │   │   ├── __init__.py
│   │   │   └── ml_strategy.py
│   │   └── common/           # 戦略間で共通のロジック (例: 評価関数、探索アルゴリズム)
│   │       ├── __init__.py
│   │       └── evaluation.py
│   ├── domain/             # 麻雀のドメインモデル (DDD)
│   │   ├── __init__.py
│   │   ├── tile.py           # 牌 (Tile)
│   │   ├── hand.py           # 手牌 (Hand)
│   │   ├── meld.py           # 面子 (Meld)
│   │   ├── game_state.py     # ゲーム状態 (GameState: 場況、局、点数など)
│   │   ├── action.py         # 行動 (Action: 打牌、ポン、チーなど)
│   │   └── yaku.py           # 役 (Yaku)
│   ├── utils/              # 汎用ユーティリティ
│   │   ├── __init__.py
│   │   └── shanten.py        # 向聴数計算など
│   └── main.py             # (任意) スクリプト実行のエントリーポイント (bot.py内でも可)
└── tests/                  # テストコード
    ├── strategies/
    │   └── test_rule_based_strategy.py
    ├── domain/
    │   └── test_hand.py
    └── ...
```

## ライセンス

このプロジェクトのライセンスについては、リポジトリのルートディレクトリにあるLICENSEファイルを参照してください。

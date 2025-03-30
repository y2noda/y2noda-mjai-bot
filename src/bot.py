#!/usr/bin/env python3

import sys

from loguru import logger
from mjai import Bot

# Import the ThinkingEngine (relative import)
from engine.thinking_engine import ThinkingEngine

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> <level>{level} {message}</level>",
    level="DEBUG",
)


class MahjongAIBot(Bot):
    """Main bot class. Delegates thinking logic to ThinkingEngine."""

    def __init__(self, player_id: int) -> None:
        """MahjongAIBotを初期化します。

        Args:
            player_id (int): プレイヤーID。

        """
        super().__init__(player_id)
        # Instantiate the thinking engine
        # The engine itself will choose the strategy internally for now
        self.engine = ThinkingEngine()
        # その他の必要な状態変数
        self.can_riichi: bool = False
        self.can_pon: bool = False
        self.can_chi: bool = False
        self.can_kan: bool = False  # 大明槓、暗槓、加槓を含む
        self.can_hora: bool = False  # 和了可能か
        self.can_discard: bool = False  # 打牌可能か
        self.tehai: list[str] = []  # 手牌
        self.kawa: list[str] = []  # 河
        self.furo: list[list[str]] = []  # 副露面子
        self.dora_markers: list[str] = []  # ドラ表示牌
        self.forbidden_tiles: dict[str, bool] = {}  # フリテンなどで捨てられない牌
        self.last_kawa_tile: str | None = None  # 最後に捨てられた牌 (鳴き判定用)
        # ... 他の状態変数 ...
        logger.info("MahjongAIBot が初期化されました。")

    def think(self) -> str:
        """現在の状況に基づいて思考し、アクション文字列を返します。"""
        logger.debug(f"--- MahjongAIBot.think をプレイヤー {self.player_id} で開始 ---")
        # Delegate the decision making to the engine
        # The engine will need access to the bot's state (self)
        try:
            logger.debug("engine.decide_action を呼び出しています...")
            action_str = self.engine.decide_action(self)
            logger.info(f"プレイヤー {self.player_id} がアクションを選択: {action_str}")
            logger.debug(f"--- MahjongAIBot.think 終了、アクションを返します: {action_str} ---")
            return action_str
        except Exception as e:
            logger.error(
                f"bot.think での思考プロセス中にエラーが発生しました: {e}",
                exc_info=True,
            )
            # エラー発生時はデフォルトのアクション (例: 打牌) や安全なアクションを返す
            # ここでは仮に最も安全な discard アクション (手牌の最後の牌) を選択
            # 実際のゲームでは、より適切なフォールバックが必要
            if self.can_discard:
                fallback_action = self.action_discard(self.tehai[-1])
                logger.warning(f"エラー発生、フォールバックアクション: {fallback_action}")
                return fallback_action
            # 打牌できない状況でのエラーは、さらに別の処理が必要かもしれない
            logger.error("打牌可能な状況ではないため、フォールバックアクションを実行できません。")
            # mjaiプロトコルに従った 'none' アクションなどを返す必要があるかもしれない
            return self.action_nothing()  # 仮の何もしないアクション
        else:  # TRY300: 例外が発生しなかった場合に実行
            logger.debug(f"--- MahjongAIBot.think 終了、アクションを返します: {action_str} ---")
            return action_str  # return文をelseブロックに移動

    def is_yakuhai(self, tile: str) -> bool:
        """指定された牌が役牌 (場風、自風、三元牌) かどうかを判定します。"""  # RUF002: 全角括弧を半角に
        # ... 既存のコード ...

    def find_improving_tiles(self) -> list[dict]:
        """手牌を改善する可能性のある打牌候補を見つけます。

        向聴数を減らす、またはより良い待ちにつながる打牌を優先します。
        現在は単純化のため、最も孤立している牌を返す例を示します。
        """  # D205: 概要行と説明の間に空行を挿入
        # ... 既存のコード ...


if __name__ == "__main__":
    MahjongAIBot(player_id=int(sys.argv[1])).start()

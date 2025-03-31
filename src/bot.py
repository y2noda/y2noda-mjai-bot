#!/usr/bin/env python3

import sys

from loguru import logger
from mjai import Bot

from engine import ThinkingEngine

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
        # ThinkingEngineのインスタンス化
        self.engine = ThinkingEngine()
        logger.info("MahjongAIBot が初期化されました。")

    def think(self) -> str:
        """現在の状況に基づいて思考し、アクション文字列を返します。"""
        logger.debug(f"--- MahjongAIBot.think をプレイヤー {self.player_id} で開始 ---")
        try:
            logger.debug("engine.decide_action を呼び出しています...")
            action_str = self.engine.decide_action(self)
            logger.info(f"プレイヤー {self.player_id} がアクションを選択: {action_str}")

        except Exception as e:
            logger.error(
                f"bot.think での思考プロセス中にエラーが発生しました: {e}",
                exc_info=True,
            )
            if self.can_discard:
                if not self.tehai_mjai:
                    logger.error("手牌が空のため、フォールバック打牌ができません。")
                    fallback_action = self.action_nothing()
                else:
                    fallback_action = self.action_discard(self.tehai_mjai[-1])
                logger.warning(f"エラー発生、フォールバックアクション: {fallback_action}")
                return fallback_action
            logger.error("打牌可能な状況ではないため、フォールバックアクションを実行できません。")
            return self.action_nothing()
        else:
            logger.debug(f"--- MahjongAIBot.think 終了、アクションを返します: {action_str} ---")
            return action_str


if __name__ == "__main__":
    MahjongAIBot(player_id=int(sys.argv[1])).start()

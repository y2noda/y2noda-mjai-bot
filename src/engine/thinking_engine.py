from typing import TYPE_CHECKING

from loguru import logger

from strategies import RuleBasedStrategy

if TYPE_CHECKING:
    from bot import MahjongAIBot
    from strategies import BaseStrategy


class ThinkingEngine:
    """Delegates thinking logic to a selected strategy."""

    def __init__(self) -> None:
        """ThinkingEngineを初期化します。"""
        self.strategy: BaseStrategy = RuleBasedStrategy()
        logger.info(f"思考エンジンが初期化され、戦略として {type(self.strategy).__name__} を使用します。")

    def decide_action(self, bot: "MahjongAIBot") -> str:
        """選択された戦略に基づいてアクションを決定します。

        Args:
            bot (MahjongAIBot): 現在のボットの状態。

        Returns:
            str: mjaiプロトコルに従ったアクション文字列。

        """
        logger.debug(f"--- エンジンが {type(self.strategy).__name__} 戦略で思考を開始 ---")
        try:
            # Pass the bot instance (which includes game state access) to the strategy
            action_str = self.strategy.decide_action(bot)
        except Exception as e:  # BLE001: 可能であればより具体的な例外を検討
            logger.error(f"戦略の実行中にエラーが発生しました: {e}", exc_info=True)
            logger.warning("戦略実行エラーのため、フォールバックアクションを試みます。")
            if bot.can_discard:
                if not bot.tehai_mjai:
                    logger.error("戦略エラーのフォールバック: 手牌が空のため打牌できません。")
                    fallback_action = bot.action_nothing()
                else:
                    fallback_action = bot.action_discard(bot.tehai_mjai[-1])
                    logger.warning(f"フォールバックアクション: {fallback_action}")
                return fallback_action
            logger.error("打牌可能な状況ではないため、フォールバックアクションを実行できません。")
            return bot.action_nothing()
        else:
            logger.debug(f"戦略がアクションを返しました: {action_str}")
            logger.debug(f"--- エンジンがアクションを決定しました: {action_str} ---")
            return action_str

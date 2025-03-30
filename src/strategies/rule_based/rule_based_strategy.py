from typing import TYPE_CHECKING

from loguru import logger

from src.strategies.base_strategy import BaseStrategy

if TYPE_CHECKING:
    from src.bot import MahjongAIBot


class RuleBasedStrategy(BaseStrategy):
    """基本的なルールに基づいてアクションを決定する戦略。"""

    def decide_action(self, bot: "MahjongAIBot") -> str:
        """ルールに基づいてアクションを決定します。"""
        current_situation = "自分のツモ番 (打牌可能)" if bot.can_discard else "他家の打牌・槓への応答"
        logger.debug(f"--- ルールベース戦略: アクション決定開始 ({current_situation}) ---")

        logger.debug(f"プレイヤー: {bot.player_id}, 手牌: {bot.tehai}, 最終ツモ牌: {bot.last_self_tsumo}")

        # アガリ可能ならアガる
        logger.debug("アガリ可能かチェック中...")
        if bot.can_hora:
            action = bot.action_hora()
            logger.info(f"アガリ可能! アクション: {action}")
            return action
        logger.debug("アガリはできません。")

        # リーチ可能ならリーチする
        logger.debug("リーチ可能かチェック中...")
        if bot.can_riichi:
            action = bot.action_riichi()
            logger.info(f"リーチ可能! アクション: {action}")
            return action
        logger.debug("リーチ条件を満たさないか、リーチできません。")

        # 副露 (鳴き) の判断
        logger.debug("鳴き (ポン/チー) 可能かチェック中...")
        # 役牌のポン
        if bot.can_pon and bot.last_kawa_tile and bot.is_yakuhai(bot.last_kawa_tile):
            logger.debug(f"役牌 ({bot.last_kawa_tile}) のポンが可能か検討中...")
            action = bot.action_pon()
            logger.info(f"役牌 ({bot.last_kawa_tile}) をポンします。 アクション: {action}")
            return action
        # 例:
        # if bot.can_pon:
        #     logger.debug("Checking for other Pon...")
        #     pons = bot.find_pon_candidates()
        #     # ... ポン判断ロジック ...
        # if bot.can_chi:
        #     logger.debug("Checking for Chi...")
        #     chis = bot.find_chi_candidates()
        #     # ... チー判断ロジック ...
        logger.debug("現時点では他の鳴き条件を満たしません。")

        # 打牌選択
        logger.debug("打牌可能かチェック中...")
        if bot.can_discard:
            logger.debug(f"打牌選択時の状態: {bot.bakaze}{bot.kyoku}-{bot.honba}: {bot.tehai} | {bot.last_self_tsumo}")

            # リーチ後のツモ切り
            if bot.self_riichi_accepted:
                discard_tile = bot.last_self_tsumo
                action = bot.action_discard(discard_tile)
                logger.debug(f"アクション決定: リーチ後の打牌 (ツモ切り) -> {action}")
                return action

            # TODO: より洗練された打牌選択ロジックを実装する
            logger.debug("手牌改善につながる打牌候補を探索中...")
            candidates = bot.find_improving_tiles()
            logger.debug(f"改善牌候補: {candidates}")
            for candidate in candidates:
                discard_tile = candidate["discard_tile"]
                # フリテンでないかチェック (簡易版)
                is_forbidden = bot.forbidden_tiles.get(discard_tile[:2], False)
                logger.debug(f"候補 {discard_tile} をチェック中。 フリテン: {is_forbidden}")
                if not is_forbidden:
                    action = bot.action_discard(discard_tile)
                    logger.info(f"手牌改善: {discard_tile} を打牌します。")
                    return action

            # 上記で見つからなければ、ツモ切りまたは手牌の最初の牌を捨てる (仮)
            discard_tile = bot.last_self_tsumo or bot.tehai_mjai[0]
            action = bot.action_discard(discard_tile)
            logger.debug(f"適切な改善牌が見つかりませんでした。デフォルト打牌: {discard_tile}")
            logger.debug(f"アクション決定: デフォルト打牌 -> {action}")
            return action
        logger.debug("打牌できません。")

        if bot.can_discard:
            logger.warning(
                "自分のツモ番なのに有効な打牌アクションが見つかりませんでした。"
                "これはバグの可能性があります。action_nothingにフォールバックします。"
            )
        else:
            logger.debug("他家の打牌等に対してアガリ/鳴きを行わず見送ります。")

        action = bot.action_nothing()
        logger.debug(f"アクション決定: 何もしない -> {action}")
        return action

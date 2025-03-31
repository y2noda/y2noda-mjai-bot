from typing import TYPE_CHECKING

from loguru import logger

from strategies import BaseStrategy

if TYPE_CHECKING:
    from bot import MahjongAIBot


class RuleBasedStrategy(BaseStrategy):
    """基本的なルールに基づいてアクションを決定する戦略。"""

    def decide_action(self, bot: "MahjongAIBot") -> str:
        """ルールに基づいてアクションを決定します。"""
        current_situation = "自分のツモ番 (打牌可能)" if bot.can_discard else "他家の打牌・槓への応答"
        logger.debug(f"--- ルールベース戦略: アクション決定開始 ({current_situation}) ---")

        logger.debug(f"プレイヤー: {bot.player_id}, 手牌: {bot.tehai_mjai}, 最終ツモ牌: {bot.last_self_tsumo}")

        # アガリ可能ならアガる
        logger.debug("アガリ可能かチェック中...")
        if bot.can_agari:
            if bot.can_tsumo_agari:
                action = bot.action_tsumo_agari()
                logger.info(f"ツモアガリ可能! アクション: {action}")
            elif bot.can_ron_agari:
                action = bot.action_ron_agari()
                logger.info(f"ロンアガリ可能! アクション: {action}")
            else:
                logger.warning("アガリ可能ですが、ツモ/ロンの区別がつきません。action_nothingを返します。")
                action = bot.action_nothing()
            return action
        logger.debug("アガリはできません。")

        # リーチ可能ならリーチする
        logger.debug("リーチ可能かチェック中...")
        if bot.can_riichi:
            riichi_discard_candidates = bot.discardable_tiles_riichi_declaration
            if riichi_discard_candidates:
                action_reach = bot.action_riichi()
                logger.info(f"リーチ可能! 宣言します。アクション: {action_reach}")
                return action_reach
            logger.warning("リーチ可能ですが、打牌可能な牌がありません。")

        logger.debug("リーチ条件を満たさないか、リーチできません。")

        # 副露 (鳴き) の判断
        logger.debug("鳴き (ポン/チー) 可能かチェック中...")
        if bot.can_pon and bot.last_kawa_tile and bot.is_yakuhai(bot.last_kawa_tile):
            logger.debug(f"役牌 ({bot.last_kawa_tile}) のポンが可能か検討中...")
            pon_candidates = bot.find_pon_candidates()
            if pon_candidates:
                consumed = pon_candidates[0]["consumed"]
                action = bot.action_pon(consumed=consumed)
                logger.info(f"役牌 ({bot.last_kawa_tile}) をポンします。 アクション: {action}")
                return action
            logger.warning(f"役牌 ({bot.last_kawa_tile}) のポンが可能と判定されましたが、候補が見つかりません。")

        logger.debug("現時点では他の鳴き条件を満たしません。")

        # 打牌選択
        logger.debug("打牌可能かチェック中...")
        if bot.can_discard:
            logger.debug(
                f"打牌選択時の状態: {bot.bakaze}{bot.kyoku}-{bot.honba}: {bot.tehai_mjai} | {bot.last_self_tsumo}"
            )

            logger.debug("手牌改善につながる打牌候補を探索中...")
            candidates = bot.find_improving_tiles()
            logger.debug(f"改善牌候補: {candidates}")
            for candidate in candidates:
                discard_tile = candidate["discard_tile"]
                if not discard_tile:
                    continue
                is_forbidden = bot.forbidden_tiles.get(discard_tile[:2], False)
                logger.debug(f"候補 {discard_tile} をチェック中。 フリテン: {is_forbidden}")
                if not is_forbidden:
                    action = bot.action_discard(discard_tile)
                    logger.info(f"手牌改善: {discard_tile} を打牌します。")
                    return action

            discard_tile = bot.last_self_tsumo
            if discard_tile and not bot.forbidden_tiles.get(discard_tile[:2], False):
                logger.debug(f"改善牌が見つからず、ツモ切りします: {discard_tile}")
                action = bot.action_discard(discard_tile)
            elif bot.tehai_mjai:
                safe_discards = [tile for tile in bot.tehai_mjai if not bot.forbidden_tiles.get(tile[:2], False)]
                if safe_discards:
                    discard_tile = safe_discards[0]
                    logger.debug(f"改善牌が見つからず、手牌から安全牌を打牌します: {discard_tile}")
                    action = bot.action_discard(discard_tile)
                elif bot.tehai_mjai:
                    discard_tile = bot.tehai_mjai[0]
                    logger.warning(
                        f"改善牌も安全牌も見つからず、手牌の最初の牌を打牌します (フリテン注意): {discard_tile}"
                    )
                    action = bot.action_discard(discard_tile)
                else:
                    logger.error("打牌選択: 手牌が空です。action_nothingを返します。")
                    action = bot.action_nothing()
            else:
                logger.error("打牌選択: ツモ牌も手牌もありません。action_nothingを返します。")
                action = bot.action_nothing()

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

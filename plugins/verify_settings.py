# plugins/verify_settings.py
# Verify settings toggler (robust + debug)
# Accessible only to OWNER_ID

import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message
)
from config import OWNER_ID, get_verify_mode_value, set_verify_mode_value

log = logging.getLogger(__name__)


@Client.on_message(filters.command("verifysettings") & filters.private & filters.user(OWNER_ID))
async def verify_settings_cmd(client: Client, message: Message):
    try:
        mode = get_verify_mode_value()
        kb = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Turn OFF" if mode else "Turn ON", callback_data="toggle_verify")],
                [InlineKeyboardButton("Close", callback_data="close")]
            ]
        )
        await message.reply_text(
            f"🔐 VERIFY MODE is currently: <b>{'ON' if mode else 'OFF'}</b>",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        log.info("verifysettings: sent status (owner).")
    except Exception as e:
        log.exception("verifysettings_cmd failed")
        try:
            await message.reply_text("❌ An error occurred while showing verify settings.")
        except:
            pass


@Client.on_callback_query(filters.regex("^toggle_verify$"))
async def toggle_verify_cb(client: Client, query: CallbackQuery):
    """Toggle verify mode. Only OWNER_ID allowed to change."""
    try:
        caller_id = query.from_user.id if query.from_user else None
        log.info("toggle_verify_cb invoked by %s", caller_id)

        # Immediately acknowledge callback (avoids spinner)
        await query.answer()  

        # ensure only owner can toggle
        if caller_id != OWNER_ID:
            log.warning("Unauthorized toggle attempt by %s", caller_id)
            await query.message.answer_text("🔒 Only the bot owner can change this setting.")
            return

        # read, toggle, save
        current = get_verify_mode_value()
        new = not current
        ok = set_verify_mode_value(new)
        log.info("set_verify_mode_value returned: %s (from %s to %s)", ok, current, new)

        # update UI
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Turn OFF" if new else "Turn ON", callback_data="toggle_verify")]]
        )

        # edit the original message to reflect new state
        await query.message.edit_text(
            f"✅ VERIFY MODE updated to: <b>{'ON' if new else 'OFF'}</b>",
            reply_markup=kb,
            parse_mode=ParseMode.HTML
        )
        log.info("verify mode toggled by owner -> %s", new)

    except Exception as e:
        log.exception("toggle_verify_cb failed")
        # try to notify owner
        try:
            await query.message.reply_text("❌ Failed to toggle VERIFY MODE. Check logs.")
        except:
            pass

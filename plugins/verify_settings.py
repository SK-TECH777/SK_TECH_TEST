from bot import Bot
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID, get_verify_mode_value, set_verify_mode_value


TOGGLE = "verify_toggle_239487"
CLOSE = "verify_close_239487"


@Bot.on_message(filters.command("verifysettings") & filters.private & filters.user(OWNER_ID))
async def verify_settings_cmd(client, message):
    mode = get_verify_mode_value()

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if mode else "Turn ON", callback_data=TOGGLE)],
        [InlineKeyboardButton("Close", callback_data=CLOSE)]
    ])

    await message.reply_text(
        f"🔐 VERIFY MODE is currently: <b>{'ON' if mode else 'OFF'}</b>",
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )


@Bot.on_callback_query(filters.regex(f"^{TOGGLE}$"))
async def toggle_cb(client, query: CallbackQuery):
    await query.answer()

    mode = get_verify_mode_value()
    new = not mode
    set_verify_mode_value(new)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if new else "Turn ON", callback_data=TOGGLE)]
    ])

    await query.message.edit_text(
        f"✅ VERIFY MODE updated to: <b>{'ON' if new else 'OFF'}</b>",
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )


@Bot.on_callback_query(filters.regex(f"^{CLOSE}$"))
async def close_cb(client, query: CallbackQuery):
    await query.answer()
    await query.message.delete()

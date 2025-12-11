from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import OWNER_ID, get_verify_mode_value, set_verify_mode_value

TOGGLE = "verify_toggle_982734"
CLOSE = "verify_close_982734"


@Client.on_message(filters.command("verifysettings") & filters.private & filters.user(OWNER_ID))
async def verify_settings_cmd(client, message):
    mode = get_verify_mode_value()

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if mode else "Turn ON", callback_data=TOGGLE)],
        [InlineKeyboardButton("Close", callback_data=CLOSE)],
    ])

    await message.reply_text(
        f"🔐 VERIFY MODE is currently: <b>{'ON' if mode else 'OFF'}</b>",
        reply_markup=btn
    )


@Client.on_callback_query(filters.regex(f"^{TOGGLE}$"))
async def toggle_verify_cb(client, query: CallbackQuery):
    await query.answer()

    if query.from_user.id != OWNER_ID:
        return await query.answer("Owner only!", show_alert=True)

    mode = get_verify_mode_value()
    new = not mode
    set_verify_mode_value(new)

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if new else "Turn ON", callback_data=TOGGLE)],
        [InlineKeyboardButton("Close", callback_data=CLOSE)],
    ])

    await query.message.edit_text(
        f"🔐 VERIFY MODE updated to: <b>{'ON' if new else 'OFF'}</b>",
        reply_markup=btn
    )


@Client.on_callback_query(filters.regex(f"^{CLOSE}$"))
async def close_cb(client, query: CallbackQuery):
    await query.answer()
    await query.message.delete()
